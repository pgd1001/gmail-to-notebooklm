"""Utility functions for file operations and text sanitization."""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional


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
    # Remove or replace invalid characters
    # Invalid: / \\ : * ? " < > |
    text = re.sub(r'[/<>:"|?*\\]', "", text)

    # Replace spaces and multiple underscores with single underscore
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text)

    # Remove leading/trailing underscores and dots
    text = text.strip("_.")

    # Truncate to max length
    if len(text) > max_length:
        text = text[:max_length].rstrip("_.")

    # Ensure not empty
    if not text:
        text = "untitled"

    return text


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
    """
    path = Path(path)
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
    """
    output_dir = Path(output_dir)
    ensure_directory(output_dir)

    file_path = output_dir / filename

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
        raise OSError(f"Failed to write file {file_path}: {e}")


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
