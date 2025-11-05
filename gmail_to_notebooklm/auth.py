"""OAuth 2.0 authentication for Gmail API."""

import os
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


def authenticate(
    credentials_path: str = "credentials.json",
    token_path: str = "token.json",
    scopes: Optional[list] = None,
) -> Credentials:
    """
    Authenticate with Gmail API using OAuth 2.0.

    On first run, this will open a browser window for the user to authorize
    the application. The authorization token is saved for future use.

    Args:
        credentials_path: Path to credentials.json from Google Cloud Console
        token_path: Path to save/load authentication token
        scopes: List of OAuth scopes (default: gmail.readonly)

    Returns:
        Authenticated Google API credentials

    Raises:
        AuthenticationError: If authentication fails
        FileNotFoundError: If credentials.json is not found

    Example:
        >>> creds = authenticate()
        >>> # First run opens browser for authorization
        >>> # Subsequent runs use saved token
    """
    if scopes is None:
        scopes = SCOPES

    # Verify credentials.json exists
    credentials_file = Path(credentials_path)
    if not credentials_file.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {credentials_path}\n"
            f"Please download credentials.json from Google Cloud Console.\n"
            f"See OAUTH_SETUP.md for instructions."
        )

    creds = None
    token_file = Path(token_path)

    # Load existing token if available
    if token_file.exists():
        try:
            with open(token_file, "rb") as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Warning: Could not load token file: {e}")
            print("Will re-authenticate...")
            creds = None

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing authentication token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Token refresh failed: {e}")
                print("Re-authenticating...")
                creds = None

        if not creds:
            try:
                print("Starting OAuth 2.0 authentication...")
                print("A browser window will open for authorization.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, scopes
                )
                creds = flow.run_local_server(port=0)

                # Verify we got valid credentials
                if not creds:
                    raise AuthenticationError("No credentials returned from OAuth flow")

                print("Authentication successful!")
            except AuthenticationError:
                raise
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                raise AuthenticationError(
                    f"Authentication failed: {e}\n"
                    f"Error details: {error_details}\n"
                    f"Please verify:\n"
                    f"1. credentials.json is valid\n"
                    f"2. Your Google account is added as a test user\n"
                    f"3. Gmail API is enabled in Google Cloud Console"
                )

        # Save the credentials for future use
        try:
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)
            print(f"Authentication token saved to {token_path}")
        except Exception as e:
            import traceback
            print(f"Warning: Could not save token: {e}")
            print(f"Details: {traceback.format_exc()}")

    return creds


def revoke_token(token_path: str = "token.json") -> None:
    """
    Revoke and delete the saved authentication token.

    Use this to force re-authentication on next run.

    Args:
        token_path: Path to the token file to delete

    Example:
        >>> revoke_token()
        >>> # Next authentication will require browser authorization
    """
    token_file = Path(token_path)
    if token_file.exists():
        try:
            os.remove(token_file)
            print(f"Token revoked: {token_path}")
        except Exception as e:
            print(f"Error revoking token: {e}")
    else:
        print(f"No token file found at {token_path}")
