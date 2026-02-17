"""Tests for input validation module."""

import pytest
from pathlib import Path
from datetime import datetime

from gmail_to_notebooklm.validation import (
    ValidationError,
    PathValidator,
    EmailValidator,
    GmailValidator,
    DateValidator,
    SizeValidator,
)


class TestPathValidator:
    """Test path validation functionality."""
    
    def test_validate_output_directory_valid(self, tmp_path):
        """Test validating valid output directory."""
        result = PathValidator.validate_output_directory(str(tmp_path))
        assert result == tmp_path
    
    def test_validate_output_directory_with_tilde(self):
        """Test validating directory with tilde."""
        result = PathValidator.validate_output_directory("~/test")
        assert "~" not in str(result)  # Should be expanded
    
    def test_validate_output_directory_traversal(self):
        """Test rejecting directory traversal."""
        with pytest.raises(ValidationError, match="directory traversal"):
            PathValidator.validate_output_directory("../../../etc")
    
    def test_validate_output_directory_empty(self):
        """Test rejecting empty directory."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            PathValidator.validate_output_directory("")
    
    def test_validate_output_directory_with_base(self, tmp_path):
        """Test validating directory within base."""
        base_dir = tmp_path
        sub_dir = base_dir / "subdir"
        
        result = PathValidator.validate_output_directory(str(sub_dir), str(base_dir))
        assert result == sub_dir.resolve()
    
    def test_validate_output_directory_outside_base(self, tmp_path):
        """Test rejecting directory outside base."""
        base_dir = tmp_path / "base"
        outside_dir = tmp_path / "outside"
        
        with pytest.raises(ValidationError, match="outside allowed directory"):
            PathValidator.validate_output_directory(str(outside_dir), str(base_dir))
    
    def test_validate_file_path_valid(self, tmp_path):
        """Test validating valid file path."""
        result = PathValidator.validate_file_path("test.txt", str(tmp_path))
        assert result == (tmp_path / "test.txt").resolve()
    
    def test_validate_file_path_with_subdirs(self, tmp_path):
        """Test validating file path with subdirectories."""
        result = PathValidator.validate_file_path("sub/dir/test.txt", str(tmp_path))
        assert result == (tmp_path / "sub" / "dir" / "test.txt").resolve()
    
    def test_validate_file_path_absolute(self, tmp_path):
        """Test rejecting absolute file path."""
        with pytest.raises(ValidationError, match="escapes base directory"):
            PathValidator.validate_file_path("/etc/passwd", str(tmp_path))
    
    def test_validate_file_path_traversal(self, tmp_path):
        """Test rejecting file path with traversal."""
        with pytest.raises(ValidationError, match="Invalid path"):
            PathValidator.validate_file_path("../../../etc/passwd", str(tmp_path))
    
    def test_validate_file_path_starts_with_slash(self, tmp_path):
        """Test rejecting path starting with slash."""
        with pytest.raises(ValidationError, match="escapes base directory"):
            PathValidator.validate_file_path("/test.txt", str(tmp_path))
    
    def test_validate_file_path_empty(self, tmp_path):
        """Test rejecting empty file path."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            PathValidator.validate_file_path("", str(tmp_path))
    
    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization."""
        result = PathValidator.sanitize_filename("Test File.txt")
        assert result == "Test_File.txt"
    
    def test_sanitize_filename_special_chars(self):
        """Test sanitizing special characters."""
        result = PathValidator.sanitize_filename("File: Name <test>")
        assert result == "File_Name_test_"  # Trailing underscore from '>'
        assert "/" not in result
        assert ":" not in result
        assert "<" not in result
        assert ">" not in result
    
    def test_sanitize_filename_long(self):
        """Test truncating long filename."""
        long_name = "a" * 300
        result = PathValidator.sanitize_filename(long_name, max_length=255)
        assert len(result) <= 255
    
    def test_sanitize_filename_reserved_windows(self):
        """Test handling Windows reserved names."""
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"]
        for name in reserved_names:
            result = PathValidator.sanitize_filename(name)
            assert result.startswith("file_")
            assert name in result
    
    def test_sanitize_filename_empty(self):
        """Test sanitizing empty filename."""
        result = PathValidator.sanitize_filename("")
        assert result == "unnamed"
    
    def test_sanitize_filename_only_special_chars(self):
        """Test sanitizing filename with only special characters."""
        result = PathValidator.sanitize_filename("///:::")
        assert result == "_"  # All special chars become underscores, then collapsed to one
    
    def test_sanitize_filename_with_extension(self):
        """Test sanitizing filename preserves extension."""
        result = PathValidator.sanitize_filename("Test: File.txt", max_length=10)
        assert result.endswith(".txt")
        assert len(result) <= 10


class TestEmailValidator:
    """Test email validation functionality."""
    
    def test_validate_email_valid(self):
        """Test validating valid email addresses."""
        valid_emails = [
            "user@example.com",
            "test.user@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
        ]
        for email in valid_emails:
            result = EmailValidator.validate_email(email)
            assert result == email
    
    def test_validate_email_invalid(self):
        """Test rejecting invalid email addresses."""
        invalid_emails = [
            "not-an-email",
            "@example.com",
            "user@",
            "user @example.com",
            "user@example",
        ]
        for email in invalid_emails:
            with pytest.raises(ValidationError, match="Invalid email"):
                EmailValidator.validate_email(email)
    
    def test_validate_email_empty(self):
        """Test rejecting empty email."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            EmailValidator.validate_email("")
    
    def test_validate_email_too_long(self):
        """Test rejecting too long email."""
        long_email = "a" * 250 + "@example.com"
        with pytest.raises(ValidationError, match="too long"):
            EmailValidator.validate_email(long_email)
    
    def test_validate_email_strips_whitespace(self):
        """Test that validation strips whitespace."""
        result = EmailValidator.validate_email("  user@example.com  ")
        assert result == "user@example.com"


class TestGmailValidator:
    """Test Gmail-specific validation."""
    
    def test_validate_label_valid(self):
        """Test validating valid Gmail labels."""
        valid_labels = [
            "Inbox",
            "Work/Projects",
            "Client: ABC Corp",
            "Label with spaces",
        ]
        for label in valid_labels:
            result = GmailValidator.validate_label(label)
            assert result == label
    
    def test_validate_label_empty(self):
        """Test rejecting empty label."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            GmailValidator.validate_label("")
    
    def test_validate_label_invalid_chars(self):
        """Test rejecting labels with invalid characters."""
        with pytest.raises(ValidationError, match="invalid characters"):
            GmailValidator.validate_label("Label\x00WithNull")
        
        with pytest.raises(ValidationError, match="invalid characters"):
            GmailValidator.validate_label("Label\nWithNewline")
    
    def test_validate_label_too_long(self):
        """Test rejecting too long label."""
        long_label = "a" * 300
        with pytest.raises(ValidationError, match="too long"):
            GmailValidator.validate_label(long_label)
    
    def test_validate_query_valid(self):
        """Test validating valid Gmail queries."""
        valid_queries = [
            "from:user@example.com",
            "subject:important",
            "has:attachment",
            'subject:"exact phrase"',
            "from:user@example.com subject:test",
        ]
        for query in valid_queries:
            result = GmailValidator.validate_query(query)
            assert result == query
    
    def test_validate_query_empty(self):
        """Test that empty query is valid."""
        result = GmailValidator.validate_query("")
        assert result == ""
    
    def test_validate_query_unbalanced_quotes(self):
        """Test rejecting unbalanced quotes."""
        with pytest.raises(ValidationError, match="Unbalanced quotes"):
            GmailValidator.validate_query('subject:"test')
    
    def test_validate_query_null_bytes(self):
        """Test rejecting query with null bytes."""
        with pytest.raises(ValidationError, match="null bytes"):
            GmailValidator.validate_query("query\x00with null")
    
    def test_validate_query_too_long(self):
        """Test rejecting too long query."""
        long_query = "a" * 15000
        with pytest.raises(ValidationError, match="too long"):
            GmailValidator.validate_query(long_query)


class TestDateValidator:
    """Test date validation functionality."""
    
    def test_validate_date_range_valid(self):
        """Test validating valid date range."""
        start, end = DateValidator.validate_date_range("2024-01-01", "2024-12-31")
        assert start.year == 2024
        assert start.month == 1
        assert end.year == 2024
        assert end.month == 12
    
    def test_validate_date_range_none(self):
        """Test validating with None dates."""
        start, end = DateValidator.validate_date_range(None, None)
        assert start is None
        assert end is None
    
    def test_validate_date_range_invalid_format(self):
        """Test rejecting invalid date format."""
        with pytest.raises(ValidationError, match="Invalid start date"):
            DateValidator.validate_date_range("not-a-date", None)
        
        with pytest.raises(ValidationError, match="Invalid end date"):
            DateValidator.validate_date_range(None, "invalid")
    
    def test_validate_date_range_start_after_end(self):
        """Test rejecting start date after end date."""
        with pytest.raises(ValidationError, match="Start date must be before end date"):
            DateValidator.validate_date_range("2024-12-31", "2024-01-01")
    
    def test_validate_date_range_same_date(self):
        """Test validating same start and end date."""
        start, end = DateValidator.validate_date_range("2024-06-15", "2024-06-15")
        assert start == end


class TestSizeValidator:
    """Test size validation functionality."""
    
    def test_validate_size_limit_valid(self):
        """Test validating valid size."""
        result = SizeValidator.validate_size_limit(1024 * 1024)  # 1MB
        assert result == 1024 * 1024
    
    def test_validate_size_limit_too_small(self):
        """Test rejecting too small size."""
        with pytest.raises(ValidationError, match="Size too small"):
            SizeValidator.validate_size_limit(100, min_size=1024)
    
    def test_validate_size_limit_too_large(self):
        """Test rejecting too large size."""
        with pytest.raises(ValidationError, match="Size too large"):
            SizeValidator.validate_size_limit(2 * 1024 * 1024 * 1024, max_size=1024 * 1024 * 1024)
    
    def test_validate_size_limit_not_integer(self):
        """Test rejecting non-integer size."""
        with pytest.raises(ValidationError, match="must be an integer"):
            SizeValidator.validate_size_limit("not a number")
    
    def test_parse_size_string_bytes(self):
        """Test parsing size string in bytes."""
        assert SizeValidator.parse_size_string("100B") == 100
        assert SizeValidator.parse_size_string("100") == 100
    
    def test_parse_size_string_kilobytes(self):
        """Test parsing size string in kilobytes."""
        assert SizeValidator.parse_size_string("1KB") == 1024
        assert SizeValidator.parse_size_string("10KB") == 10 * 1024
    
    def test_parse_size_string_megabytes(self):
        """Test parsing size string in megabytes."""
        assert SizeValidator.parse_size_string("1MB") == 1024 * 1024
        assert SizeValidator.parse_size_string("50MB") == 50 * 1024 * 1024
    
    def test_parse_size_string_gigabytes(self):
        """Test parsing size string in gigabytes."""
        assert SizeValidator.parse_size_string("1GB") == 1024 * 1024 * 1024
    
    def test_parse_size_string_with_decimal(self):
        """Test parsing size string with decimal."""
        assert SizeValidator.parse_size_string("1.5MB") == int(1.5 * 1024 * 1024)
    
    def test_parse_size_string_with_spaces(self):
        """Test parsing size string with spaces."""
        assert SizeValidator.parse_size_string("10 MB") == 10 * 1024 * 1024
    
    def test_parse_size_string_invalid(self):
        """Test rejecting invalid size string."""
        with pytest.raises(ValidationError, match="Invalid size format"):
            SizeValidator.parse_size_string("invalid")
        
        with pytest.raises(ValidationError, match="Invalid size format"):
            SizeValidator.parse_size_string("10XB")
