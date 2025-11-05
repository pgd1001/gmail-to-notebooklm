"""Tests for email parser module."""

import pytest
from gmail_to_notebooklm.parser import EmailParser, EmailParseError


class TestEmailParser:
    """Tests for EmailParser class."""

    def test_get_header(self):
        """Test header extraction."""
        parser = EmailParser()
        headers = [
            {"name": "From", "value": "test@example.com"},
            {"name": "Subject", "value": "Test Subject"},
        ]

        assert parser.get_header(headers, "From") == "test@example.com"
        assert parser.get_header(headers, "from") == "test@example.com"  # Case insensitive
        assert parser.get_header(headers, "To") is None

    def test_parse_message(self, sample_gmail_message):
        """Test parsing Gmail API message."""
        parser = EmailParser()
        parsed = parser.parse_message(sample_gmail_message)

        assert parsed["id"] == "abc123def456"
        assert parsed["thread_id"] == "thread789"
        assert parsed["from"] == "John Doe <john@example.com>"
        assert parsed["to"] == "Jane Smith <jane@example.com>"
        assert parsed["cc"] == "Bob Jones <bob@example.com>"
        assert parsed["subject"] == "Test Email Subject"
        assert "2024" in parsed["date"]

    def test_parse_message_no_subject(self, sample_gmail_message):
        """Test parsing message with no subject."""
        # Remove subject header
        sample_gmail_message["payload"]["headers"] = [
            h for h in sample_gmail_message["payload"]["headers"]
            if h["name"] != "Subject"
        ]

        parser = EmailParser()
        parsed = parser.parse_message(sample_gmail_message)

        assert parsed["subject"] == "(No Subject)"

    def test_extract_html_body(self, sample_gmail_message):
        """Test HTML body extraction."""
        parser = EmailParser()
        parsed = parser.parse_message(sample_gmail_message)

        assert parsed["body_html"] is not None
        assert "test" in parsed["body_html"].lower()

    def test_extract_text_body(self, sample_gmail_message):
        """Test plain text body extraction."""
        parser = EmailParser()
        parsed = parser.parse_message(sample_gmail_message)

        assert parsed["body_text"] is not None
        assert "test" in parsed["body_text"].lower()

    def test_decode_body(self):
        """Test base64 body decoding."""
        parser = EmailParser()

        # "Hello World" in base64url
        encoded = "SGVsbG8gV29ybGQ="
        decoded = parser._decode_body(encoded)

        assert decoded == "Hello World"

    def test_parse_messages_batch(self, sample_gmail_message):
        """Test batch parsing."""
        parser = EmailParser()
        messages = [sample_gmail_message, sample_gmail_message]

        parsed = parser.parse_messages_batch(messages)

        assert len(parsed) == 2
        assert all(p["subject"] == "Test Email Subject" for p in parsed)
