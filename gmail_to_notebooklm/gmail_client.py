"""Gmail API client for fetching emails."""

from typing import Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn


class GmailAPIError(Exception):
    """Raised when Gmail API operations fail."""
    pass


class GmailClient:
    """
    Client for interacting with Gmail API.

    Provides methods to list and fetch emails from Gmail labels.
    """

    def __init__(self, credentials: Credentials):
        """
        Initialize Gmail API client.

        Args:
            credentials: Authenticated Google API credentials

        Raises:
            GmailAPIError: If client initialization fails
        """
        try:
            self.service = build("gmail", "v1", credentials=credentials)
            self.user_id = "me"
        except Exception as e:
            raise GmailAPIError(f"Failed to initialize Gmail client: {e}")

    def get_label_id(self, label_name: str) -> Optional[str]:
        """
        Get label ID from label name.

        Args:
            label_name: Name of the Gmail label

        Returns:
            Label ID if found, None otherwise

        Raises:
            GmailAPIError: If API call fails
        """
        try:
            results = self.service.users().labels().list(userId=self.user_id).execute()
            labels = results.get("labels", [])

            for label in labels:
                if label["name"] == label_name:
                    return label["id"]

            return None
        except HttpError as e:
            raise GmailAPIError(f"Failed to fetch labels: {e}")

    def list_messages(
        self,
        label_name: Optional[str] = None,
        max_results: Optional[int] = None,
        query: Optional[str] = None,
    ) -> List[str]:
        """
        List message IDs for a given label and/or query.

        Args:
            label_name: Name of the Gmail label (optional if query provided)
            max_results: Maximum number of messages to return (None = all)
            query: Gmail search query string (optional)

        Returns:
            List of message IDs

        Raises:
            GmailAPIError: If API call fails, label not found, or neither label nor query provided
        """
        # Validate inputs
        if not label_name and not query:
            raise GmailAPIError("Either label_name or query must be provided")

        # Get label ID if label specified
        label_id = None
        if label_name:
            label_id = self.get_label_id(label_name)
            if label_id is None:
                available_labels = self.list_labels()
                raise GmailAPIError(
                    f"Label '{label_name}' not found.\n"
                    f"Available labels: {', '.join(available_labels)}\n"
                    f"Note: Label names are case-sensitive."
                )

        message_ids = []
        page_token = None

        try:
            while True:
                # Build request parameters
                params = {
                    "userId": self.user_id,
                }

                # Add label filter if provided
                if label_id:
                    params["labelIds"] = [label_id]

                # Add query if provided
                if query:
                    # Combine with label if both present
                    if label_id:
                        params["q"] = f"label:{label_name} {query}"
                    else:
                        params["q"] = query

                if page_token:
                    params["pageToken"] = page_token

                if max_results:
                    remaining = max_results - len(message_ids)
                    params["maxResults"] = min(remaining, 500)

                # Fetch messages
                results = (
                    self.service.users().messages().list(**params).execute()
                )

                messages = results.get("messages", [])
                message_ids.extend([msg["id"] for msg in messages])

                # Check if we should continue
                page_token = results.get("nextPageToken")
                if not page_token:
                    break

                if max_results and len(message_ids) >= max_results:
                    break

            return message_ids[: max_results] if max_results else message_ids

        except HttpError as e:
            raise GmailAPIError(f"Failed to list messages: {e}")

    def get_message(self, message_id: str) -> Dict:
        """
        Get full message content including headers and body.

        Args:
            message_id: Gmail message ID

        Returns:
            Dictionary containing message data with keys:
            - id: Message ID
            - threadId: Thread ID
            - labelIds: List of label IDs
            - snippet: Message snippet
            - payload: Full message payload with headers and parts

        Raises:
            GmailAPIError: If API call fails
        """
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId=self.user_id, id=message_id, format="full")
                .execute()
            )
            return message
        except HttpError as e:
            raise GmailAPIError(f"Failed to fetch message {message_id}: {e}")

    def list_labels(self) -> List[str]:
        """
        List all available Gmail labels.

        Returns:
            List of label names

        Raises:
            GmailAPIError: If API call fails
        """
        try:
            results = self.service.users().labels().list(userId=self.user_id).execute()
            labels = results.get("labels", [])
            return [label["name"] for label in labels]
        except HttpError as e:
            raise GmailAPIError(f"Failed to list labels: {e}")

    def get_messages_batch(
        self,
        label_name: Optional[str] = None,
        max_results: Optional[int] = None,
        query: Optional[str] = None,
    ) -> List[Dict]:
        """
        Get multiple messages with full content.

        This is a convenience method that combines list_messages and get_message.

        Args:
            label_name: Name of the Gmail label (optional if query provided)
            max_results: Maximum number of messages to return
            query: Gmail search query string (optional)

        Returns:
            List of message dictionaries

        Raises:
            GmailAPIError: If API calls fail
        """
        message_ids = self.list_messages(label_name, max_results, query)

        messages = []

        # Use Rich progress bar for fetching messages
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task(
                "[cyan]Fetching messages...", total=len(message_ids)
            )

            for msg_id in message_ids:
                try:
                    message = self.get_message(msg_id)
                    messages.append(message)
                except GmailAPIError as e:
                    progress.console.print(
                        f"[yellow]Warning: Failed to fetch message {msg_id}: {e}[/yellow]"
                    )
                    continue
                finally:
                    progress.update(task, advance=1)

        return messages
