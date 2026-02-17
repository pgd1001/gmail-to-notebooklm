"""Email MIME parsing and header extraction."""

import base64
from email.utils import parsedate_to_datetime
from typing import Callable, Dict, List, Optional

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from .audit import get_audit_logger


class EmailParseError(Exception):
    """Raised when email parsing fails."""
    pass


class EmailSizeExceededError(EmailParseError):
    """Raised when email size exceeds limit."""
    pass


class EmailParser:
    """
    Parser for Gmail API message format.

    Extracts headers, body content, and metadata from Gmail messages.
    """
    
    def __init__(self, max_email_size_mb: int = 50):
        """
        Initialize email parser.
        
        Args:
            max_email_size_mb: Maximum email size in MB (default: 50MB)
        """
        self.max_email_size_bytes = max_email_size_mb * 1024 * 1024
        self.audit_logger = get_audit_logger()

    @staticmethod
    def get_header(headers: List[Dict], name: str) -> Optional[str]:
        """
        Extract a specific header value from headers list.

        Args:
            headers: List of header dictionaries from Gmail API
            name: Header name (case-insensitive)

        Returns:
            Header value if found, None otherwise
        """
        name_lower = name.lower()
        for header in headers:
            if header.get("name", "").lower() == name_lower:
                return header.get("value")
        return None

    def parse_message(self, message: Dict) -> Dict[str, any]:
        """
        Parse a Gmail API message into structured format.

        Args:
            message: Raw message from Gmail API

        Returns:
            Dictionary containing:
            - id: Message ID
            - thread_id: Thread ID
            - from: Sender email and name
            - to: Recipient email and name
            - cc: CC recipients (if present)
            - subject: Email subject
            - date: Email date (ISO format)
            - body_html: HTML body content
            - body_text: Plain text body content

        Raises:
            EmailParseError: If parsing fails
            EmailSizeExceededError: If email size exceeds limit
        """
        try:
            # Check email size first
            size_estimate = message.get("sizeEstimate", 0)
            if size_estimate > self.max_email_size_bytes:
                error_msg = (
                    f"Email size ({size_estimate / 1024 / 1024:.2f} MB) exceeds "
                    f"limit ({self.max_email_size_bytes / 1024 / 1024:.0f} MB)"
                )
                if self.audit_logger:
                    self.audit_logger.log_validation_error(
                        'email_size',
                        message.get('id', 'unknown'),
                        error_msg
                    )
                raise EmailSizeExceededError(error_msg)
            
            payload = message.get("payload", {})
            headers = payload.get("headers", [])

            # Extract headers
            parsed = {
                "id": message.get("id"),
                "thread_id": message.get("threadId"),
                "from": self.get_header(headers, "From"),
                "to": self.get_header(headers, "To"),
                "cc": self.get_header(headers, "Cc"),
                "subject": self.get_header(headers, "Subject") or "(No Subject)",
                "date": self.get_header(headers, "Date"),
                "size_bytes": size_estimate,
            }

            # Parse date to ISO format
            if parsed["date"]:
                try:
                    dt = parsedate_to_datetime(parsed["date"])
                    parsed["date_iso"] = dt.isoformat()
                except Exception:
                    parsed["date_iso"] = parsed["date"]
            else:
                parsed["date_iso"] = "Unknown"

            # Extract body content
            body_html, body_text = self._extract_body(payload)
            
            # Check body size after extraction
            body_size = 0
            if body_html:
                body_size += len(body_html.encode('utf-8'))
            if body_text:
                body_size += len(body_text.encode('utf-8'))
            
            if body_size > self.max_email_size_bytes:
                error_msg = (
                    f"Email body size ({body_size / 1024 / 1024:.2f} MB) exceeds "
                    f"limit ({self.max_email_size_bytes / 1024 / 1024:.0f} MB)"
                )
                if self.audit_logger:
                    self.audit_logger.log_validation_error(
                        'email_body_size',
                        message.get('id', 'unknown'),
                        error_msg
                    )
                raise EmailSizeExceededError(error_msg)
            
            parsed["body_html"] = body_html
            parsed["body_text"] = body_text

            return parsed

        except EmailSizeExceededError:
            raise
        except Exception as e:
            error_msg = f"Failed to parse message: {e}"
            if self.audit_logger:
                self.audit_logger.log_validation_error(
                    'email_parse',
                    message.get('id', 'unknown'),
                    error_msg
                )
            raise EmailParseError(error_msg)

    def _extract_body(self, payload: Dict) -> tuple[Optional[str], Optional[str]]:
        """
        Extract HTML and plain text body from message payload.

        Args:
            payload: Message payload from Gmail API

        Returns:
            Tuple of (html_body, text_body)
        """
        html_body = None
        text_body = None

        # Check if body is directly in payload
        if "body" in payload and payload["body"].get("data"):
            mime_type = payload.get("mimeType", "")
            body_data = payload["body"]["data"]
            decoded = self._decode_body(body_data)

            if "html" in mime_type.lower():
                html_body = decoded
            else:
                text_body = decoded

        # Check multipart message
        if "parts" in payload:
            html_body, text_body = self._extract_from_parts(payload["parts"])

        return html_body, text_body

    def _extract_from_parts(
        self, parts: List[Dict]
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Recursively extract body from multipart message.

        Args:
            parts: List of message parts

        Returns:
            Tuple of (html_body, text_body)
        """
        html_body = None
        text_body = None

        for part in parts:
            mime_type = part.get("mimeType", "")

            # Recursively process nested parts
            if "parts" in part:
                nested_html, nested_text = self._extract_from_parts(part["parts"])
                if nested_html:
                    html_body = nested_html
                if nested_text:
                    text_body = nested_text
                continue

            # Extract body data
            if "body" in part and part["body"].get("data"):
                body_data = part["body"]["data"]
                decoded = self._decode_body(body_data)

                if "text/html" in mime_type:
                    html_body = decoded
                elif "text/plain" in mime_type:
                    text_body = decoded

        return html_body, text_body

    @staticmethod
    def _decode_body(data: str) -> str:
        """
        Decode base64url encoded body data.

        Args:
            data: Base64url encoded string

        Returns:
            Decoded string
        """
        try:
            # Gmail uses base64url encoding (- and _ instead of + and /)
            decoded_bytes = base64.urlsafe_b64decode(data)
            return decoded_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            return f"[Error decoding body: {e}]"

    def parse_messages_batch(
        self,
        messages: List[Dict],
        progress_callback: Optional[Callable[[int, int], None]] = None,
        skip_oversized: bool = True,
    ) -> List[Dict]:
        """
        Parse multiple messages.

        Args:
            messages: List of raw Gmail API messages
            progress_callback: Optional callback for progress updates (current, total)
            skip_oversized: Whether to skip oversized emails (default: True)

        Returns:
            List of parsed message dictionaries

        Raises:
            EmailParseError: If parsing fails for any message (and skip_oversized=False)
        """
        parsed_messages = []
        skipped_count = 0

        # Use callback if provided, otherwise use Rich progress bar
        if progress_callback:
            for i, message in enumerate(messages, 1):
                try:
                    parsed = self.parse_message(message)
                    parsed_messages.append(parsed)
                except EmailSizeExceededError as e:
                    if skip_oversized:
                        skipped_count += 1
                        continue
                    else:
                        raise
                except EmailParseError as e:
                    # Note: Warnings are swallowed when using callback
                    continue
                finally:
                    progress_callback(i, len(messages))
        else:
            # Use Rich progress bar for parsing messages
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                task = progress.add_task("[cyan]Parsing messages...", total=len(messages))

                for message in messages:
                    try:
                        parsed = self.parse_message(message)
                        parsed_messages.append(parsed)
                    except EmailSizeExceededError as e:
                        if skip_oversized:
                            skipped_count += 1
                            progress.console.print(
                                f"[yellow]Warning: Skipping oversized email {message.get('id')}: {e}[/yellow]"
                            )
                            continue
                        else:
                            raise
                    except EmailParseError as e:
                        progress.console.print(
                            f"[yellow]Warning: Failed to parse message {message.get('id')}: {e}[/yellow]"
                        )
                        continue
                    finally:
                        progress.update(task, advance=1)
                
                if skipped_count > 0:
                    progress.console.print(
                        f"[yellow]Skipped {skipped_count} oversized email(s)[/yellow]"
                    )

        return parsed_messages
