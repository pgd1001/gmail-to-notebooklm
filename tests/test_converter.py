"""Tests for Markdown converter module."""

import pytest
from gmail_to_notebooklm.converter import MarkdownConverter, ConversionError


class TestMarkdownConverter:
    """Tests for MarkdownConverter class."""

    def test_convert_email_with_headers(self, sample_parsed_email):
        """Test converting email with headers."""
        converter = MarkdownConverter(include_headers=True)
        markdown = converter.convert_email(sample_parsed_email)

        assert "---" in markdown
        assert "From: John Doe" in markdown
        assert "To: Jane Smith" in markdown
        assert "Subject: Test Email Subject" in markdown
        assert "test" in markdown.lower()

    def test_convert_email_without_headers(self, sample_parsed_email):
        """Test converting email without headers."""
        converter = MarkdownConverter(include_headers=False)
        markdown = converter.convert_email(sample_parsed_email)

        assert "---" not in markdown
        assert "From:" not in markdown
        assert "test" in markdown.lower()

    def test_format_headers(self, sample_parsed_email):
        """Test header formatting."""
        converter = MarkdownConverter()
        headers = converter._format_headers(sample_parsed_email)

        assert headers.startswith("---")
        assert headers.endswith("---")
        assert "From: John Doe <john@example.com>" in headers
        assert "To: Jane Smith <jane@example.com>" in headers
        assert "Cc: Bob Jones <bob@example.com>" in headers

    def test_html_to_markdown(self, sample_html_email):
        """Test HTML to Markdown conversion."""
        converter = MarkdownConverter()
        markdown = converter._html_to_markdown(sample_html_email)

        assert "**World**" in markdown or "*World*" in markdown
        assert "Item 1" in markdown
        assert "Item 2" in markdown
        assert "example.com" in markdown

    def test_clean_markdown(self):
        """Test Markdown cleaning."""
        converter = MarkdownConverter()

        # Test excessive blank lines
        dirty = "Line 1\n\n\n\n\nLine 2"
        clean = converter._clean_markdown(dirty)

        # Should have at most 2 consecutive blank lines
        assert "\n\n\n\n" not in clean

    def test_convert_html_body_priority(self, sample_parsed_email):
        """Test that HTML body is preferred over plain text."""
        converter = MarkdownConverter()
        markdown = converter.convert_email(sample_parsed_email)

        # HTML version has <strong> tag, plain text doesn't
        assert "**test**" in markdown or "*test*" in markdown

    def test_convert_text_only_email(self, sample_parsed_email):
        """Test converting email with only plain text."""
        sample_parsed_email["body_html"] = None
        sample_parsed_email["body_text"] = "Plain text only email."

        converter = MarkdownConverter()
        markdown = converter.convert_email(sample_parsed_email)

        assert "Plain text only email." in markdown

    def test_convert_emails_batch(self, sample_parsed_email):
        """Test batch conversion."""
        converter = MarkdownConverter()
        emails = [sample_parsed_email, sample_parsed_email]

        converted = converter.convert_emails_batch(emails)

        assert len(converted) == 2
        assert all(isinstance(c[0], str) for c in converted)  # email_id
        assert all(isinstance(c[1], str) for c in converted)  # markdown
        assert all("---" in c[1] for c in converted)
