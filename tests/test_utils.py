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
    validate_date,
    build_date_query,
    build_sender_query,
    generate_index_file,
    get_date_subdirectory,
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


class TestPhase1Utils:
    """Tests for Phase 1 utility functions (date filtering, index generation, etc.)."""

    def test_validate_date_with_hyphen_format(self):
        """Test date validation with YYYY-MM-DD format."""
        result = validate_date("2024-01-15")
        assert result == "2024/01/15"

    def test_validate_date_with_slash_format(self):
        """Test date validation with YYYY/MM/DD format."""
        result = validate_date("2024/01/15")
        assert result == "2024/01/15"

    def test_validate_date_invalid_format(self):
        """Test date validation with invalid format."""
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("2024-13-01")  # Invalid month

        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("01/15/2024")  # Wrong order

        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("not-a-date")

    def test_build_date_query_after_only(self):
        """Test building query with only after date."""
        result = build_date_query(after="2024-01-01")
        assert result == "after:2024/01/01"

    def test_build_date_query_before_only(self):
        """Test building query with only before date."""
        result = build_date_query(before="2024-12-31")
        assert result == "before:2024/12/31"

    def test_build_date_query_both_dates(self):
        """Test building query with both after and before dates."""
        result = build_date_query(after="2024-01-01", before="2024-12-31")
        assert result == "after:2024/01/01 before:2024/12/31"

    def test_build_date_query_neither(self):
        """Test building query with no dates."""
        result = build_date_query()
        assert result == ""

    def test_build_sender_query_single_from(self):
        """Test building query with single sender."""
        result = build_sender_query(from_="john@example.com")
        assert result == "from:john@example.com"

    def test_build_sender_query_multiple_from(self):
        """Test building query with multiple senders."""
        result = build_sender_query(from_="john@example.com,jane@example.com")
        assert result == "(from:john@example.com OR from:jane@example.com)"

    def test_build_sender_query_single_to(self):
        """Test building query with single recipient."""
        result = build_sender_query(to="recipient@example.com")
        assert result == "to:recipient@example.com"

    def test_build_sender_query_multiple_to(self):
        """Test building query with multiple recipients."""
        result = build_sender_query(to="alice@example.com,bob@example.com")
        assert result == "(to:alice@example.com OR to:bob@example.com)"

    def test_build_sender_query_exclude_from(self):
        """Test building query with excluded sender."""
        result = build_sender_query(exclude_from="spam@example.com")
        assert result == "-from:spam@example.com"

    def test_build_sender_query_multiple_exclude(self):
        """Test building query with multiple excluded senders."""
        result = build_sender_query(exclude_from="spam1@example.com,spam2@example.com")
        assert result == "-from:spam1@example.com -from:spam2@example.com"

    def test_build_sender_query_combined(self):
        """Test building query with from and exclude."""
        result = build_sender_query(from_="john@example.com", exclude_from="spam@example.com")
        assert result == "from:john@example.com -from:spam@example.com"

    def test_build_sender_query_all_parameters(self):
        """Test building query with all parameters."""
        result = build_sender_query(
            from_="john@example.com",
            to="alice@example.com",
            exclude_from="spam@example.com"
        )
        assert "from:john@example.com" in result
        assert "to:alice@example.com" in result
        assert "-from:spam@example.com" in result

    def test_build_sender_query_empty(self):
        """Test building query with no parameters."""
        result = build_sender_query()
        assert result == ""

    def test_generate_index_file(self, tmp_path):
        """Test index file generation."""
        # Create test email data
        emails = [
            ("id1", {
                "date": "Mon, 15 Jan 2024 10:30:00 +0000",
                "from": "john@example.com",
                "subject": "Test Email 1"
            }),
            ("id2", {
                "date": "Tue, 16 Jan 2024 14:20:00 +0000",
                "from": "jane@example.com",
                "subject": "Test Email 2"
            }),
        ]

        filenames = {
            "id1": "Test_Email_1_id1.md",
            "id2": "Test_Email_2_id2.md"
        }

        # Generate index
        index_path = generate_index_file(tmp_path, emails, filenames)

        # Verify file exists
        assert index_path.exists()
        assert index_path.name == "INDEX.md"

        # Verify content
        content = index_path.read_text(encoding="utf-8")
        assert "# Email Export Index" in content
        assert "Total emails: 2" in content
        assert "| Date | From | Subject | File |" in content
        assert "john@example.com" in content
        assert "jane@example.com" in content
        assert "Test Email 1" in content
        assert "Test Email 2" in content
        assert "[Test_Email_1_id1.md](./Test_Email_1_id1.md)" in content

    def test_generate_index_file_with_subdirs(self, tmp_path):
        """Test index file generation with subdirectory paths."""
        emails = [
            ("id1", {
                "date": "Mon, 15 Jan 2024 10:30:00 +0000",
                "from": "john@example.com",
                "subject": "Test Email"
            }),
        ]

        filenames = {
            "id1": "2024/01/Test_Email_id1.md"  # With subdirectory
        }

        index_path = generate_index_file(tmp_path, emails, filenames)
        content = index_path.read_text(encoding="utf-8")

        # Should include subdirectory in link
        assert "[2024/01/Test_Email_id1.md](./2024/01/Test_Email_id1.md)" in content

    def test_generate_index_file_empty_list(self, tmp_path):
        """Test index file generation with empty email list."""
        emails = []
        filenames = {}

        index_path = generate_index_file(tmp_path, emails, filenames)

        assert index_path.exists()
        content = index_path.read_text(encoding="utf-8")
        assert "Total emails: 0" in content

    def test_get_date_subdirectory_yyyy_mm(self):
        """Test date subdirectory with YYYY/MM format."""
        email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        result = get_date_subdirectory(email_data, "YYYY/MM")
        assert result == "2024/01"

    def test_get_date_subdirectory_yyyy_mm_dash(self):
        """Test date subdirectory with YYYY-MM format."""
        email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        result = get_date_subdirectory(email_data, "YYYY-MM")
        assert result == "2024-01"

    def test_get_date_subdirectory_yyyy_mm_dd(self):
        """Test date subdirectory with YYYY/MM/DD format."""
        email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        result = get_date_subdirectory(email_data, "YYYY/MM/DD")
        assert result == "2024/01/15"

    def test_get_date_subdirectory_yyyy_mm_dd_dash(self):
        """Test date subdirectory with YYYY-MM-DD format."""
        email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        result = get_date_subdirectory(email_data, "YYYY-MM-DD")
        assert result == "2024-01-15"

    def test_get_date_subdirectory_invalid_date(self):
        """Test date subdirectory with invalid date."""
        email_data = {"date": "invalid date"}
        result = get_date_subdirectory(email_data, "YYYY/MM")
        assert result == "Unknown"

    def test_get_date_subdirectory_missing_date(self):
        """Test date subdirectory with missing date field."""
        email_data = {}
        result = get_date_subdirectory(email_data, "YYYY/MM")
        assert result == "Unknown"

    def test_get_date_subdirectory_default_format(self):
        """Test date subdirectory with default format."""
        email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        result = get_date_subdirectory(email_data)  # No format specified
        assert result == "2024/01"  # Should default to YYYY/MM

    def test_get_date_subdirectory_invalid_format(self):
        """Test date subdirectory with invalid format string."""
        email_data = {"date": "Mon, 15 Jan 2024 10:30:00 +0000"}
        result = get_date_subdirectory(email_data, "INVALID")
        assert result == "2024/01"  # Should default to YYYY/MM
