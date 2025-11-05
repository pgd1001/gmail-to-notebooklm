"""Utility functions for file operations and text sanitization."""

import re
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
