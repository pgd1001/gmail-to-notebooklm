"""Core export orchestration layer.

This module provides a UI-agnostic interface for exporting Gmail emails to Markdown.
It orchestrates the authentication, fetching, parsing, and conversion workflow with
optional callbacks for progress reporting and status updates.

Both CLI and GUI interfaces use this core engine.
"""

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from gmail_to_notebooklm.auth import authenticate
from gmail_to_notebooklm.config import Config, ConfigError
from gmail_to_notebooklm.converter import ConversionError, MarkdownConverter
from gmail_to_notebooklm.gmail_client import GmailAPIError, GmailClient
from gmail_to_notebooklm.parser import EmailParseError, EmailParser
from gmail_to_notebooklm.utils import (
    build_date_query,
    build_sender_query,
    create_filename,
    generate_index_file,
    get_date_subdirectory,
    write_markdown_file,
)

# Optional history tracking
try:
    from gmail_to_notebooklm.history import ExportHistory
    HISTORY_AVAILABLE = True
except ImportError:
    HISTORY_AVAILABLE = False


@dataclass
class ProgressUpdate:
    """Progress information for UI updates.

    Attributes:
        step: Current step number (1-5)
        total_steps: Total number of steps (5)
        message: Description of current step
        current: Current item number within step (e.g., email 5)
        total: Total items in current step (e.g., 100 emails)
        percent: Completion percentage of current step (0-100)
    """

    step: int
    total_steps: int
    message: str
    current: int = 0
    total: int = 0
    percent: float = 0.0


@dataclass
class ExportResult:
    """Result of export operation.

    Attributes:
        success: Whether export completed successfully
        files_created: Number of markdown files created
        output_dir: Path to output directory
        errors: List of error messages encountered
        duration_seconds: Total time taken for export
        stats: Dictionary of statistics (email counts, sizes, etc.)
    """

    success: bool
    files_created: int
    output_dir: Path
    errors: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    stats: Dict = field(default_factory=dict)


class ExportEngine:
    """Core export orchestration with UI callbacks.

    This class coordinates the entire export workflow:
    1. Authentication with Gmail
    2. Connecting to Gmail API
    3. Fetching email messages
    4. Parsing email content
    5. Converting to Markdown and saving

    Callbacks allow UI (CLI or GUI) to display progress without coupling
    the business logic to any specific UI framework.

    Example:
        >>> def on_progress(update: ProgressUpdate):
        ...     print(f"Step {update.step}/{update.total_steps}: {update.message}")
        ...
        >>> engine = ExportEngine(progress_callback=on_progress)
        >>> settings = {"label": "Work", "output_dir": "./output"}
        >>> result = engine.export(settings)
        >>> print(f"Created {result.files_created} files")
    """

    def __init__(
        self,
        progress_callback: Optional[Callable[[ProgressUpdate], None]] = None,
        status_callback: Optional[Callable[[str], None]] = None,
        error_callback: Optional[Callable[[Exception], bool]] = None,
        enable_history: bool = True,
    ):
        """Initialize export engine with optional callbacks.

        Args:
            progress_callback: Called with ProgressUpdate for each progress change
            status_callback: Called with status message strings
            error_callback: Called when errors occur, returns True to retry
            enable_history: Track exports in history database
        """
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.error_callback = error_callback
        self.enable_history = enable_history and HISTORY_AVAILABLE

        self._cancelled = False
        self._start_time = 0.0

        # Initialize history if enabled
        self.history = ExportHistory() if self.enable_history else None

    def cancel(self):
        """Request cancellation of current export."""
        self._cancelled = True

    def _report_progress(self, update: ProgressUpdate):
        """Report progress to callback if available."""
        if self.progress_callback:
            self.progress_callback(update)

    def _report_status(self, message: str):
        """Report status to callback if available."""
        if self.status_callback:
            self.status_callback(message)

    def _handle_error(self, error: Exception) -> bool:
        """Handle error with callback if available.

        Args:
            error: Exception that occurred

        Returns:
            True if should retry, False otherwise
        """
        if self.error_callback:
            return self.error_callback(error)
        return False

    def export(
        self,
        settings: Dict,
        dry_run: bool = False,
        resume_file: Optional[str] = None,
    ) -> ExportResult:
        """Execute complete export workflow.

        Args:
            settings: Export configuration dictionary with keys:
                - label: Gmail label name (optional if query provided)
                - query: Gmail search query (optional)
                - output_dir: Output directory path
                - max_results: Maximum emails to process
                - credentials_path: Path to credentials.json
                - token_path: Path to token.json
                - after: Filter emails after date
                - before: Filter emails before date
                - from_: Filter by sender
                - to: Filter by recipient
                - exclude_from: Exclude senders
                - organize_by_date: Organize into date subdirectories
                - date_format: Date format for subdirectories
                - create_index: Generate INDEX.md
                - overwrite: Overwrite existing files
            dry_run: If True, simulate export without creating files
            resume_file: Path to resume state file (not yet implemented)

        Returns:
            ExportResult with operation details

        Raises:
            ConfigError: Invalid configuration
            GmailAPIError: Gmail API operation failed
            EmailParseError: Email parsing failed
            ConversionError: Markdown conversion failed
        """
        self._start_time = time.time()
        self._cancelled = False

        errors = []
        output_dir = Path(settings.get("output_dir", "./output"))

        try:
            # Step 1/5: Authenticate
            self._report_progress(
                ProgressUpdate(step=1, total_steps=5, message="Authenticating with Gmail...")
            )

            credentials_path = settings.get("credentials_path", "credentials.json")
            token_path = settings.get("token_path", "token.json")

            # Note: auth.py will be updated to accept status_callback
            creds = authenticate(
                credentials_path=credentials_path,
                token_path=token_path,
                status_callback=self._report_status,
            )

            if self._cancelled:
                return self._create_cancelled_result(output_dir)

            # Step 2/5: Connect to Gmail
            self._report_progress(
                ProgressUpdate(step=2, total_steps=5, message="Connecting to Gmail API...")
            )

            client = GmailClient(creds)

            if self._cancelled:
                return self._create_cancelled_result(output_dir)

            # Build query from filters
            query_parts = []
            if settings.get("query"):
                query_parts.append(settings["query"])

            # Add date filters
            date_query = build_date_query(
                after=settings.get("after"), before=settings.get("before")
            )
            if date_query:
                query_parts.append(date_query)

            # Add sender filters
            sender_query = build_sender_query(
                from_=settings.get("from_"),
                to=settings.get("to"),
                exclude_from=settings.get("exclude_from"),
            )
            if sender_query:
                query_parts.append(sender_query)

            final_query = " ".join(query_parts) if query_parts else None

            # Step 3/5: Fetch messages
            label = settings.get("label")
            max_results = settings.get("max_results")

            def fetch_progress(current: int, total: int):
                if self._cancelled:
                    return
                percent = (current / total * 100) if total > 0 else 0
                self._report_progress(
                    ProgressUpdate(
                        step=3,
                        total_steps=5,
                        message=f"Fetching emails ({current}/{total})...",
                        current=current,
                        total=total,
                        percent=percent,
                    )
                )

            self._report_progress(
                ProgressUpdate(step=3, total_steps=5, message="Fetching emails...")
            )

            # Note: gmail_client.py will be updated to accept progress_callback
            messages = client.get_messages_batch(
                label_name=label,
                max_results=max_results,
                query=final_query,
                progress_callback=fetch_progress,
            )

            if self._cancelled:
                return self._create_cancelled_result(output_dir)

            if not messages:
                return ExportResult(
                    success=True,
                    files_created=0,
                    output_dir=output_dir,
                    errors=["No emails found matching criteria"],
                    duration_seconds=time.time() - self._start_time,
                    stats={"emails_found": 0},
                )

            # Step 4/5: Parse emails
            def parse_progress(current: int, total: int):
                if self._cancelled:
                    return
                percent = (current / total * 100) if total > 0 else 0
                self._report_progress(
                    ProgressUpdate(
                        step=4,
                        total_steps=5,
                        message=f"Parsing emails ({current}/{total})...",
                        current=current,
                        total=total,
                        percent=percent,
                    )
                )

            self._report_progress(
                ProgressUpdate(step=4, total_steps=5, message="Parsing emails...")
            )

            parser = EmailParser()
            # Note: parser.py will be updated to accept progress_callback
            parsed_emails = parser.parse_messages_batch(
                messages, progress_callback=parse_progress
            )

            if self._cancelled:
                return self._create_cancelled_result(output_dir)

            # Step 5/5: Convert and save
            def convert_progress(current: int, total: int):
                if self._cancelled:
                    return
                percent = (current / total * 100) if total > 0 else 0
                self._report_progress(
                    ProgressUpdate(
                        step=5,
                        total_steps=5,
                        message=f"Converting to Markdown ({current}/{total})...",
                        current=current,
                        total=total,
                        percent=percent,
                    )
                )

            self._report_progress(
                ProgressUpdate(step=5, total_steps=5, message="Converting to Markdown...")
            )

            converter = MarkdownConverter()
            # Note: converter.py will be updated to accept progress_callback
            converted = converter.convert_emails_batch(
                parsed_emails, progress_callback=convert_progress
            )

            if self._cancelled:
                return self._create_cancelled_result(output_dir)

            # Save files (if not dry run)
            if dry_run:
                return ExportResult(
                    success=True,
                    files_created=0,
                    output_dir=output_dir,
                    errors=[],
                    duration_seconds=time.time() - self._start_time,
                    stats={
                        "dry_run": True,
                        "emails_found": len(messages),
                        "emails_parsed": len(parsed_emails),
                    },
                )

            # Save files
            saved_count = 0
            filenames: Dict[str, str] = {}
            organize_by_date = settings.get("organize_by_date", False)
            date_format = settings.get("date_format", "YYYY/MM")
            overwrite = settings.get("overwrite", False)

            for email_id, markdown_content in converted:
                if self._cancelled:
                    break

                # Find original email data
                original = next((e for e in parsed_emails if e["id"] == email_id), None)
                if not original:
                    continue

                # Create filename
                subject = original.get("subject", "No Subject")
                filename = create_filename(subject, email_id)

                # Determine output directory
                if organize_by_date and original:
                    date_subdir = get_date_subdirectory(original, date_format)
                    target_dir = output_dir / date_subdir
                    relative_path = f"{date_subdir}/{filename}"
                else:
                    target_dir = output_dir
                    relative_path = filename

                # Write file
                try:
                    write_markdown_file(
                        target_dir, filename, markdown_content, overwrite=overwrite
                    )
                    filenames[email_id] = relative_path
                    saved_count += 1
                except Exception as e:
                    error_msg = f"Failed to write {filename}: {e}"
                    errors.append(error_msg)
                    self._report_status(f"Warning: {error_msg}")

            # Generate index if requested
            if settings.get("create_index", False) and saved_count > 0:
                try:
                    self._report_status("Generating index file...")
                    email_list = [
                        (e["id"], e) for e in parsed_emails if e["id"] in filenames
                    ]
                    generate_index_file(output_dir, email_list, filenames)
                except Exception as e:
                    error_msg = f"Failed to create index: {e}"
                    errors.append(error_msg)
                    self._report_status(f"Warning: {error_msg}")

            # Calculate statistics
            duration = time.time() - self._start_time
            stats = {
                "emails_found": len(messages),
                "emails_parsed": len(parsed_emails),
                "emails_converted": len(converted),
                "files_saved": saved_count,
                "errors": len(errors),
            }

            result = ExportResult(
                success=saved_count > 0 and not self._cancelled,
                files_created=saved_count,
                output_dir=output_dir,
                errors=errors,
                duration_seconds=duration,
                stats=stats,
            )

            # Record in history if enabled and not dry run
            if self.history and not dry_run:
                try:
                    # Prepare file metadata
                    file_metadata = []
                    for email in parsed_emails:
                        if email["id"] in filenames:
                            file_metadata.append({
                                "email_id": email["id"],
                                "filename": filenames[email["id"]],
                                "subject": email.get("subject", ""),
                                "from": email.get("from", ""),
                                "to": email.get("to", ""),
                                "date": email.get("date", ""),
                            })

                    # Add to history
                    self.history.add_export(
                        label=settings.get("label"),
                        query=final_query,
                        files_created=saved_count,
                        duration_seconds=duration,
                        output_dir=str(output_dir.absolute()),
                        settings=settings,
                        success=result.success,
                        error_count=len(errors),
                        files=file_metadata if file_metadata else None,
                    )
                except Exception as e:
                    # Don't fail export if history tracking fails
                    self._report_status(f"Warning: Failed to save to history: {e}")

            return result

        except Exception as e:
            # Try error callback for retry
            if self._handle_error(e):
                return self.export(settings, dry_run, resume_file)

            # Re-raise if not handled
            raise

    def _create_cancelled_result(self, output_dir: Path) -> ExportResult:
        """Create result for cancelled export."""
        return ExportResult(
            success=False,
            files_created=0,
            output_dir=output_dir,
            errors=["Export cancelled by user"],
            duration_seconds=time.time() - self._start_time,
            stats={"cancelled": True},
        )
