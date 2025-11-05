"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def sample_gmail_message():
    """Sample Gmail API message for testing."""
    return {
        "id": "abc123def456",
        "threadId": "thread789",
        "labelIds": ["Label_1", "INBOX"],
        "snippet": "This is a test email...",
        "payload": {
            "headers": [
                {"name": "From", "value": "John Doe <john@example.com>"},
                {"name": "To", "value": "Jane Smith <jane@example.com>"},
                {"name": "Cc", "value": "Bob Jones <bob@example.com>"},
                {"name": "Subject", "value": "Test Email Subject"},
                {"name": "Date", "value": "Mon, 15 Jan 2024 10:30:00 -0800"},
            ],
            "mimeType": "multipart/alternative",
            "parts": [
                {
                    "mimeType": "text/plain",
                    "body": {
                        "data": "VGhpcyBpcyBhIHRlc3QgZW1haWwgYm9keS4="  # "This is a test email body."
                    },
                },
                {
                    "mimeType": "text/html",
                    "body": {
                        "data": "PHA-VGhpcyBpcyBhIDxzdHJvbmc-dGVzdDwvc3Ryb25nPiBlbWFpbCBib2R5LjwvcD4="  # "<p>This is a <strong>test</strong> email body.</p>"
                    },
                },
            ],
        },
    }


@pytest.fixture
def sample_parsed_email():
    """Sample parsed email data for testing."""
    return {
        "id": "abc123def456",
        "thread_id": "thread789",
        "from": "John Doe <john@example.com>",
        "to": "Jane Smith <jane@example.com>",
        "cc": "Bob Jones <bob@example.com>",
        "subject": "Test Email Subject",
        "date": "Mon, 15 Jan 2024 10:30:00 -0800",
        "date_iso": "2024-01-15T10:30:00-08:00",
        "body_html": "<p>This is a <strong>test</strong> email body.</p>",
        "body_text": "This is a test email body.",
    }


@pytest.fixture
def sample_html_email():
    """Sample HTML email content for testing."""
    return """
    <html>
        <head><title>Test Email</title></head>
        <body>
            <p>Hello <strong>World</strong>!</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
            <a href="https://example.com">Link</a>
        </body>
    </html>
    """


@pytest.fixture
def mock_gmail_service():
    """Mock Gmail API service."""
    service = Mock()

    # Mock users().labels().list()
    labels_list = Mock()
    labels_list.execute.return_value = {
        "labels": [
            {"id": "Label_1", "name": "Test Label"},
            {"id": "Label_2", "name": "Client A"},
            {"id": "INBOX", "name": "INBOX"},
        ]
    }

    # Mock users().messages().list()
    messages_list = Mock()
    messages_list.execute.return_value = {
        "messages": [{"id": "msg1"}, {"id": "msg2"}],
        "nextPageToken": None,
    }

    # Mock users().messages().get()
    messages_get = Mock()

    # Setup mock chain
    service.users().labels().list.return_value = labels_list
    service.users().messages().list.return_value = messages_list
    service.users().messages().get.return_value = messages_get

    return service


@pytest.fixture
def mock_credentials():
    """Mock Google OAuth credentials."""
    creds = Mock()
    creds.valid = True
    creds.expired = False
    creds.refresh_token = "refresh_token"
    return creds


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for tests."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_markdown_content():
    """Sample Markdown content for testing."""
    return """---
From: John Doe <john@example.com>
To: Jane Smith <jane@example.com>
Date: Mon, 15 Jan 2024 10:30:00 -0800
Subject: Test Email Subject
---

This is a **test** email body.

* Item 1
* Item 2

[Link](https://example.com)
"""
