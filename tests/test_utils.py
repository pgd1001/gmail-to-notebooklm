"""Tests for utility functions."""

import pytest
from pathlib import Path
from gmail_to_notebooklm.utils import (
    sanitize_filename,
    create_filename,
    ensure_directory,
    write_markdown_file,
    format_size,
    truncate_text,
    validate_label_name,
)


class TestUtils:
    """Tests for utility functions."""

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        assert sanitize_filename("Normal Text") == "Normal_Text"
        assert sanitize_filename("File: With Colon") == "File_With_Colon"
        assert sanitize_filename("Path/With/Slash") == "PathWithSlash"
        assert sanitize_filename("Test<>:|?*") == "Test"
        assert sanitize_filename("Multiple   Spaces") == "Multiple_Spaces"

    def test_sanitize_filename_max_length(self):
        """Test filename length limit."""
        long_text = "a" * 300
        result = sanitize_filename(long_text, max_length=200)
        assert len(result) == 200

    def test_sanitize_filename_empty(self):
        """Test sanitizing empty string."""
        assert sanitize_filename("") == "untitled"
        assert sanitize_filename("   ") == "untitled"

    def test_create_filename(self):
        """Test filename creation."""
        filename = create_filename("Test Subject", "abc123def456")
        assert filename == "Test_Subject_abc123de.md"
        assert filename.endswith(".md")

    def test_create_filename_long_subject(self):
        """Test filename creation with long subject."""
        long_subject = "a" * 300
        filename = create_filename(long_subject, "abc123")
        assert len(filename) <= 200  # Should be truncated

    def test_ensure_directory(self, tmp_path):
        """Test directory creation."""
        test_dir = tmp_path / "test" / "nested" / "dir"
        ensure_directory(test_dir)
        assert test_dir.exists()
        assert test_dir.is_dir()

    def test_write_markdown_file(self, temp_output_dir):
        """Test writing Markdown file."""
        content = "# Test Content\n\nThis is a test."
        filename = "test.md"

        file_path = write_markdown_file(temp_output_dir, filename, content)

        assert file_path.exists()
        assert file_path.read_text(encoding="utf-8") == content

    def test_write_markdown_file_no_overwrite(self, temp_output_dir):
        """Test writing file without overwriting."""
        content1 = "First content"
        content2 = "Second content"
        filename = "test.md"

        # Write first file
        file1 = write_markdown_file(temp_output_dir, filename, content1)

        # Write second file with same name (should create test_1.md)
        file2 = write_markdown_file(temp_output_dir, filename, content2, overwrite=False)

        assert file1 != file2
        assert file1.exists()
        assert file2.exists()
        assert file1.read_text(encoding="utf-8") == content1
        assert file2.read_text(encoding="utf-8") == content2

    def test_write_markdown_file_overwrite(self, temp_output_dir):
        """Test overwriting existing file."""
        content1 = "First content"
        content2 = "Second content"
        filename = "test.md"

        # Write first file
        file1 = write_markdown_file(temp_output_dir, filename, content1)

        # Overwrite
        file2 = write_markdown_file(temp_output_dir, filename, content2, overwrite=True)

        assert file1 == file2
        assert file2.read_text(encoding="utf-8") == content2

    def test_format_size(self):
        """Test size formatting."""
        assert format_size(512) == "512.0 B"
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(1048576) == "1.0 MB"

    def test_truncate_text(self):
        """Test text truncation."""
        assert truncate_text("Short", 10) == "Short"
        assert truncate_text("This is a long text", 10) == "This is..."
        assert truncate_text("Test", 10, suffix="~") == "Test"

    def test_validate_label_name(self):
        """Test label name validation."""
        assert validate_label_name("Valid Label") is True
        assert validate_label_name("Client/Project A") is True
        assert validate_label_name("") is False
        assert validate_label_name("  ") is False
        assert validate_label_name(" Leading space") is False
        assert validate_label_name("Trailing space ") is False
