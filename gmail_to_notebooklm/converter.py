"""HTML to Markdown conversion with email headers."""

from typing import Callable, Dict, Optional

import html2text
from bs4 import BeautifulSoup
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn


class ConversionError(Exception):
    """Raised when HTML to Markdown conversion fails."""
    pass


class MarkdownConverter:
    """
    Converter for HTML email content to Markdown format.

    Includes email headers and converts HTML body to clean Markdown.
    """

    def __init__(
        self,
        wrap_width: int = 0,
        include_headers: bool = True,
        body_width: int = 0,
    ):
        """
        Initialize Markdown converter.

        Args:
            wrap_width: Text wrap width (0 = no wrapping)
            include_headers: Include email headers in output
            body_width: Body text wrap width (0 = no wrapping)
        """
        self.wrap_width = wrap_width
        self.include_headers = include_headers
        self.body_width = body_width

        # Configure html2text
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = body_width
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False
        self.h2t.skip_internal_links = True
        self.h2t.inline_links = True
        self.h2t.protect_links = True
        self.h2t.wrap_links = False

    def convert_email(self, email_data: Dict[str, any]) -> str:
        """
        Convert parsed email to Markdown format.

        Args:
            email_data: Parsed email data from EmailParser

        Returns:
            Markdown formatted email with headers and body

        Raises:
            ConversionError: If conversion fails
        """
        try:
            markdown_parts = []

            # Add headers if enabled
            if self.include_headers:
                header_block = self._format_headers(email_data)
                markdown_parts.append(header_block)

            # Convert body to Markdown
            body_md = self._convert_body(email_data)
            markdown_parts.append(body_md)

            return "\n\n".join(markdown_parts)

        except Exception as e:
            raise ConversionError(f"Failed to convert email to Markdown: {e}")

    def _format_headers(self, email_data: Dict) -> str:
        """
        Format email headers as YAML front matter.

        Args:
            email_data: Parsed email data

        Returns:
            YAML formatted header block
        """
        headers = ["---"]

        # From
        if email_data.get("from"):
            headers.append(f"From: {email_data['from']}")

        # To
        if email_data.get("to"):
            headers.append(f"To: {email_data['to']}")

        # Cc (optional)
        if email_data.get("cc"):
            headers.append(f"Cc: {email_data['cc']}")

        # Date
        if email_data.get("date"):
            headers.append(f"Date: {email_data['date']}")

        # Subject
        if email_data.get("subject"):
            # Escape special YAML characters in subject
            subject = email_data["subject"].replace(":", "\\:")
            headers.append(f"Subject: {subject}")

        headers.append("---")

        return "\n".join(headers)

    def _convert_body(self, email_data: Dict) -> str:
        """
        Convert email body to Markdown.

        Prioritizes HTML body over plain text.

        Args:
            email_data: Parsed email data

        Returns:
            Markdown formatted body
        """
        # Prefer HTML body
        if email_data.get("body_html"):
            return self._html_to_markdown(email_data["body_html"])

        # Fall back to plain text
        if email_data.get("body_text"):
            return email_data["body_text"]

        return "[No body content]"

    def _html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML to Markdown.

        Args:
            html_content: HTML string

        Returns:
            Markdown string
        """
        try:
            # Clean HTML with BeautifulSoup first
            soup = BeautifulSoup(html_content, "lxml")

            # Remove script and style elements
            for element in soup(["script", "style"]):
                element.decompose()

            # Get cleaned HTML
            cleaned_html = str(soup)

            # Convert to Markdown
            markdown = self.h2t.handle(cleaned_html)

            # Clean up excessive newlines
            markdown = self._clean_markdown(markdown)

            return markdown

        except Exception as e:
            # If conversion fails, return cleaned plain text
            try:
                soup = BeautifulSoup(html_content, "lxml")
                return soup.get_text(separator="\n", strip=True)
            except Exception:
                return f"[Error converting HTML: {e}]"

    @staticmethod
    def _clean_markdown(markdown: str) -> str:
        """
        Clean up Markdown formatting.

        Args:
            markdown: Raw Markdown string

        Returns:
            Cleaned Markdown string
        """
        # Remove excessive blank lines (more than 2 consecutive)
        lines = markdown.split("\n")
        cleaned_lines = []
        blank_count = 0

        for line in lines:
            if line.strip():
                cleaned_lines.append(line)
                blank_count = 0
            else:
                blank_count += 1
                if blank_count <= 2:
                    cleaned_lines.append(line)

        markdown = "\n".join(cleaned_lines)

        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in markdown.split("\n")]
        markdown = "\n".join(lines)

        # Ensure single trailing newline
        markdown = markdown.rstrip() + "\n"

        return markdown

    def convert_emails_batch(
        self,
        emails: list[Dict],
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> list[tuple[str, str]]:
        """
        Convert multiple emails to Markdown.

        Args:
            emails: List of parsed email data dictionaries
            progress_callback: Optional callback for progress updates (current, total)

        Returns:
            List of tuples (email_id, markdown_content)

        Raises:
            ConversionError: If conversion fails for any email
        """
        converted = []

        # Use callback if provided, otherwise use Rich progress bar
        if progress_callback:
            for i, email in enumerate(emails, 1):
                try:
                    markdown = self.convert_email(email)
                    email_id = email.get("id", f"unknown_{i}")
                    converted.append((email_id, markdown))
                except ConversionError as e:
                    # Note: Warnings are swallowed when using callback
                    continue
                finally:
                    progress_callback(i, len(emails))
        else:
            # Use Rich progress bar for conversion
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                task = progress.add_task(
                    "[cyan]Converting to Markdown...", total=len(emails)
                )

                for i, email in enumerate(emails, 1):
                    try:
                        markdown = self.convert_email(email)
                        email_id = email.get("id", f"unknown_{i}")
                        converted.append((email_id, markdown))
                    except ConversionError as e:
                        progress.console.print(
                            f"[yellow]Warning: Failed to convert email {email.get('id')}: {e}[/yellow]"
                        )
                        continue
                    finally:
                        progress.update(task, advance=1)

        return converted
