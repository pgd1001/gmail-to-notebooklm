"""Utility functions for file operations and text sanitization."""

import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Optional

from .validation import PathValidator, ValidationError
from .audit import get_audit_logger


def sanitize_filename(text: str, max_length: int = 200) -> str:
    """
    Sanitize text for use as filename.

    Removes or replaces characters that are invalid in filenames.

    Args:
        text: Text to sanitize
        max_length: Maximum filename length (excluding extension)

    Returns:
        Sanitized filename string

    Example:
        >>> sanitize_filename("Project: Update (Q4)")
        'Project_Update_Q4'
    """
    # Use PathValidator for comprehensive sanitization
    return PathValidator.sanitize_filename(text, max_length=max_length)


def create_filename(subject: str, email_id: str, extension: str = ".md") -> str:
    """
    Create filename from email subject and ID.

    Args:
        subject: Email subject line
        email_id: Gmail message ID
        extension: File extension (default: .md)

    Returns:
        Sanitized filename

    Example:
        >>> create_filename("Project Update", "abc123def456")
        'Project_Update_abc123de.md'
    """
    # Sanitize subject
    clean_subject = sanitize_filename(subject, max_length=180)

    # Shorten email ID (first 8 characters)
    short_id = email_id[:8] if email_id else "unknown"

    # Combine
    filename = f"{clean_subject}_{short_id}{extension}"

    return filename


def ensure_directory(path: Path) -> None:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        path: Directory path

    Raises:
        OSError: If directory cannot be created
        ValidationError: If path is invalid
    """
    path = Path(path)
    
    # Validate path for security
    try:
        PathValidator.validate_output_directory(str(path))
    except ValidationError as e:
        raise OSError(f"Invalid directory path: {e}")
    
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")


def write_markdown_file(
    output_dir: Path, filename: str, content: str, overwrite: bool = False
) -> Path:
    """
    Write Markdown content to file.

    Args:
        output_dir: Output directory path
        filename: File name
        content: Markdown content
        overwrite: Whether to overwrite existing files

    Returns:
        Path to created file

    Raises:
        FileExistsError: If file exists and overwrite is False
        OSError: If file cannot be written
        ValidationError: If path is invalid
    """
    output_dir = Path(output_dir)
    audit_logger = get_audit_logger()
    
    # Validate output directory
    try:
        validated_dir = PathValidator.validate_output_directory(str(output_dir))
        output_dir = validated_dir
    except ValidationError as e:
        error_msg = f"Invalid output directory: {e}"
        if audit_logger:
            audit_logger.log_validation_error('output_dir', str(output_dir), error_msg)
        raise OSError(error_msg)
    
    # Sanitize filename
    filename = PathValidator.sanitize_filename(filename)
    
    ensure_directory(output_dir)

    file_path = output_dir / filename
    
    # Validate final file path
    try:
        PathValidator.validate_file_path(filename, str(output_dir))
    except ValidationError as e:
        error_msg = f"Invalid file path: {e}"
        if audit_logger:
            audit_logger.log_validation_error('file_path', filename, error_msg)
        raise OSError(error_msg)

    # Check if file exists
    if file_path.exists() and not overwrite:
        # Add counter to filename
        counter = 1
        base_name = file_path.stem
        while file_path.exists():
            new_name = f"{base_name}_{counter}{file_path.suffix}"
            file_path = output_dir / new_name
            counter += 1
            if counter > 1000:  # Safety limit
                raise FileExistsError(
                    f"Too many files with similar names: {base_name}"
                )

    # Write file
    try:
        file_path.write_text(content, encoding="utf-8")
        return file_path
    except Exception as e:
        error_msg = f"Failed to write file {file_path}: {e}"
        if audit_logger:
            audit_logger.log_file_error('write', str(file_path), error_msg)
        raise OSError(error_msg)


def format_size(size_bytes: int) -> str:
    """
    Format byte size as human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")

    Example:
        >>> format_size(1536)
        '1.5 KB'
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text

    Example:
        >>> truncate_text("This is a very long email subject", 20)
        'This is a very lo...'
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def count_emails_by_label(labels: list[str]) -> dict[str, int]:
    """
    Count emails for multiple labels.

    Args:
        labels: List of label names

    Returns:
        Dictionary mapping label names to counts

    Note:
        This is a placeholder - actual implementation would
        query Gmail API for each label.
    """
    # This would be implemented with actual Gmail API calls
    return {label: 0 for label in labels}


def validate_label_name(label: str) -> bool:
    """
    Validate Gmail label name format.

    Args:
        label: Label name to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_label_name("Client/Project A")
        True
        >>> validate_label_name("")
        False
    """
    if not label or not label.strip():
        return False

    # Gmail labels can contain most characters
    # Just check it's not empty and doesn't have leading/trailing whitespace
    return label == label.strip()


def get_env_or_default(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable or default value.

    Args:
        key: Environment variable name
        default: Default value if not set

    Returns:
        Environment variable value or default

    Example:
        >>> get_env_or_default("GMAIL_TO_NBL_OUTPUT_DIR", "./output")
        './output'
    """
    import os

    return os.environ.get(key, default)


def validate_date(date_str: str) -> str:
    """
    Validate and normalize date string for Gmail query.

    Accepts YYYY-MM-DD or YYYY/MM/DD format.

    Args:
        date_str: Date string to validate

    Returns:
        Normalized date string in YYYY/MM/DD format

    Raises:
        ValueError: If date format is invalid

    Example:
        >>> validate_date("2024-01-15")
        '2024/01/15'
        >>> validate_date("2024/01/15")
        '2024/01/15'
    """
    # Try parsing with different formats
    for fmt in ["%Y-%m-%d", "%Y/%m/%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            # Return in Gmail-compatible format (YYYY/MM/DD)
            return dt.strftime("%Y/%m/%d")
        except ValueError:
            continue

    raise ValueError(
        f"Invalid date format: '{date_str}'. Use YYYY-MM-DD or YYYY/MM/DD"
    )


def build_date_query(after: Optional[str] = None, before: Optional[str] = None) -> str:
    """
    Build Gmail query string from date filters.

    Args:
        after: Filter emails after this date (YYYY-MM-DD or YYYY/MM/DD)
        before: Filter emails before this date (YYYY-MM-DD or YYYY/MM/DD)

    Returns:
        Gmail query string for date filtering

    Raises:
        ValueError: If date format is invalid

    Example:
        >>> build_date_query(after="2024-01-01")
        'after:2024/01/01'
        >>> build_date_query(after="2024-01-01", before="2024-12-31")
        'after:2024/01/01 before:2024/12/31'
    """
    parts = []

    if after:
        normalized_date = validate_date(after)
        parts.append(f"after:{normalized_date}")

    if before:
        normalized_date = validate_date(before)
        parts.append(f"before:{normalized_date}")

    return " ".join(parts)


def build_sender_query(
    from_: Optional[str] = None,
    to: Optional[str] = None,
    exclude_from: Optional[str] = None,
) -> str:
    """
    Build Gmail query string from sender/recipient filters.

    Args:
        from_: Filter emails from sender(s) (comma-separated)
        to: Filter emails to recipient(s) (comma-separated)
        exclude_from: Exclude emails from sender(s) (comma-separated)

    Returns:
        Gmail query string for sender/recipient filtering

    Example:
        >>> build_sender_query(from_="john@example.com")
        'from:john@example.com'
        >>> build_sender_query(from_="john@example.com,jane@example.com")
        '(from:john@example.com OR from:jane@example.com)'
        >>> build_sender_query(from_="john@example.com", exclude_from="spam@example.com")
        'from:john@example.com -from:spam@example.com'
    """
    parts = []

    # Handle from filter
    if from_:
        senders = [s.strip() for s in from_.split(",") if s.strip()]
        if len(senders) == 1:
            parts.append(f"from:{senders[0]}")
        elif len(senders) > 1:
            from_parts = " OR ".join([f"from:{s}" for s in senders])
            parts.append(f"({from_parts})")

    # Handle to filter
    if to:
        recipients = [r.strip() for r in to.split(",") if r.strip()]
        if len(recipients) == 1:
            parts.append(f"to:{recipients[0]}")
        elif len(recipients) > 1:
            to_parts = " OR ".join([f"to:{r}" for r in recipients])
            parts.append(f"({to_parts})")

    # Handle exclude_from filter
    if exclude_from:
        excludes = [e.strip() for e in exclude_from.split(",") if e.strip()]
        for exclude in excludes:
            parts.append(f"-from:{exclude}")

    return " ".join(parts)


def generate_index_file(
    output_dir: Path, emails: list[tuple[str, dict]], filenames: dict[str, str]
) -> Path:
    """
    Generate index markdown file with table of contents.

    Args:
        output_dir: Output directory path
        emails: List of (email_id, email_data) tuples
        filenames: Dictionary mapping email_id to filename

    Returns:
        Path to created index file

    Example index structure:
        # Email Export Index

        Total emails: 42

        ## Emails by Date

        | Date | From | Subject | File |
        |------|------|---------|------|
        | 2024-01-15 | john@example.com | Project Update | [Link](./file.md) |
    """
    output_dir = Path(output_dir)
    ensure_directory(output_dir)

    # Sort emails by date (newest first)
    sorted_emails = sorted(
        emails, key=lambda x: x[1].get("date", ""), reverse=True
    )

    # Build index content
    lines = [
        "# Email Export Index",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total emails: {len(emails)}",
        "",
        "## Emails by Date",
        "",
        "| Date | From | Subject | File |",
        "|------|------|---------|------|",
    ]

    for email_id, email_data in sorted_emails:
        # Extract email metadata
        date_str = email_data.get("date", "Unknown")
        # Parse and format date if possible
        try:
            # Try to parse date string and format as YYYY-MM-DD
            from email.utils import parsedate_to_datetime

            date_obj = parsedate_to_datetime(date_str)
            date_display = date_obj.strftime("%Y-%m-%d")
        except (ValueError, TypeError, AttributeError):
            date_display = date_str[:10] if len(date_str) > 10 else date_str

        from_addr = email_data.get("from", "Unknown")
        subject = email_data.get("subject", "No Subject")

        # Truncate long values for table
        from_display = truncate_text(from_addr, 30)
        subject_display = truncate_text(subject, 50)

        # Get filename
        filename = filenames.get(email_id, "unknown.md")

        # Create markdown link
        link = f"[{filename}](./{filename})"

        # Add row
        lines.append(
            f"| {date_display} | {from_display} | {subject_display} | {link} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by [Gmail to NotebookLM](https://github.com/pgd1001/gmail-to-notebooklm)*")

    # Write index file
    index_content = "\n".join(lines)
    index_path = output_dir / "INDEX.md"

    try:
        index_path.write_text(index_content, encoding="utf-8")
        return index_path
    except Exception as e:
        raise OSError(f"Failed to write index file {index_path}: {e}")


def get_date_subdirectory(email_data: dict, date_format: str = "YYYY/MM") -> str:
    """
    Get date-based subdirectory path from email data.

    Args:
        email_data: Parsed email data dictionary
        date_format: Date format for subdirectory (YYYY/MM, YYYY-MM, YYYY/MM/DD, YYYY-MM-DD)

    Returns:
        Subdirectory path string (e.g., "2024/01" or "2024-01")

    Example:
        >>> email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        >>> get_date_subdirectory(email_data, "YYYY/MM")
        '2024/01'
        >>> get_date_subdirectory(email_data, "YYYY-MM")
        '2024-01'
    """
    date_str = email_data.get("date", "")

    try:
        # Parse email date
        date_obj = parsedate_to_datetime(date_str)

        # Format based on specified format
        if date_format == "YYYY/MM":
            return f"{date_obj.year}/{date_obj.month:02d}"
        elif date_format == "YYYY-MM":
            return f"{date_obj.year}-{date_obj.month:02d}"
        elif date_format == "YYYY/MM/DD":
            return f"{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}"
        elif date_format == "YYYY-MM-DD":
            return f"{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d}"
        else:
            # Default to YYYY/MM
            return f"{date_obj.year}/{date_obj.month:02d}"

    except (ValueError, TypeError, AttributeError):
        # If date parsing fails, use "Unknown" subdirectory
        return "Unknown"


def generate_anchor_id(
    email_data: dict,
    id_length: int = 16,
    include_subject: bool = True,
) -> str:
    """
    Generate a unique anchor ID for an email in consolidated documents.

    Creates NotebookLM-compatible anchor IDs using email metadata.

    Args:
        email_data: Parsed email data dictionary
        id_length: Length of Gmail ID to use (default: 16, max: 64)
        include_subject: Include sanitized subject in anchor (default: True)

    Returns:
        Anchor ID string suitable for HTML/Markdown anchors (alphanumeric + hyphens)

    Example:
        >>> email = {"subject": "Project Update", "id": "abc123def456xyz"}
        >>> generate_anchor_id(email)
        'project-update-abc123def456xy'
        >>> generate_anchor_id(email, include_subject=False)
        'email-abc123def456xy'
    """
    # Get full Gmail ID
    email_id = email_data.get("id", "unknown")

    # Use specified length (capped at actual ID length)
    short_id = email_id[:min(id_length, len(email_id))]

    if include_subject:
        # Sanitize subject for anchor
        subject = email_data.get("subject", "untitled")
        subject_slug = sanitize_filename(subject, max_length=40)

        # Build anchor with subject and ID
        anchor = f"{subject_slug}-{short_id}".lower()
    else:
        # Build anchor with just ID
        anchor = f"email-{short_id}".lower()

    # Ensure only alphanumeric and hyphens
    anchor = re.sub(r"[^a-z0-9-]", "", anchor)

    # Remove leading/trailing hyphens
    anchor = anchor.strip("-")

    # Ensure not empty
    if not anchor:
        anchor = f"email-{email_id[:8]}"

    return anchor


def group_emails_by(
    emails: list[dict],
    group_by: str = "all",
) -> dict[str, list[dict]]:
    """
    Group emails by specified criteria.

    Organizes emails for consolidated export.

    Args:
        emails: List of parsed email data dictionaries
        group_by: Grouping strategy:
            - "all": Single group (consolidate all)
            - "thread": Group by thread_id (conversations)
            - "date": Group by date (YYYY-MM)
            - "sender": Group by "from" address
            - "recipient": Group by "to" address

    Returns:
        Dictionary mapping group key to list of emails

    Example:
        >>> emails = [
        ...     {"id": "1", "thread_id": "t1", "from": "a@x.com", "date": "2024-01-15"},
        ...     {"id": "2", "thread_id": "t1", "from": "a@x.com", "date": "2024-01-15"},
        ... ]
        >>> groups = group_emails_by(emails, "thread")
        >>> len(groups["t1"])
        2
    """
    groups: dict[str, list[dict]] = {}

    for email in emails:
        if group_by == "all":
            key = "all"
        elif group_by == "thread":
            key = email.get("thread_id", "unknown_thread")
        elif group_by == "date":
            # Extract YYYY-MM from date
            try:
                date_obj = parsedate_to_datetime(email.get("date", ""))
                key = f"{date_obj.year}-{date_obj.month:02d}"
            except (ValueError, TypeError, AttributeError):
                key = "unknown_date"
        elif group_by == "sender":
            # Extract email address from "From" field
            from_str = email.get("from", "unknown")
            # Try to extract email address from "Name <email@domain>" format
            match = re.search(r"<(.+?)>", from_str)
            key = match.group(1) if match else from_str
        elif group_by == "recipient":
            # Extract email address from "To" field
            to_str = email.get("to", "unknown")
            # Try to extract email address from "Name <email@domain>" format
            match = re.search(r"<(.+?)>", to_str)
            key = match.group(1) if match else to_str
        else:
            # Default to grouping by thread if unknown strategy
            key = email.get("thread_id", "unknown_thread")

        if key not in groups:
            groups[key] = []
        groups[key].append(email)

    return groups
