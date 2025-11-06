"""OAuth 2.0 authentication for Gmail API."""

import os
import pickle
import sys
from pathlib import Path
from typing import Callable, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def find_credentials_file(credentials_path: str = "credentials.json") -> Optional[Path]:
    """
    Search for credentials file in multiple locations.

    Search order:
    1. User-provided path (current directory or absolute path)
    2. User config directory (~/.gmail-to-notebooklm/credentials.json)
    3. Embedded default credentials (gmail_to_notebooklm/data/default_credentials.json)

    Args:
        credentials_path: Preferred credentials path (default: credentials.json)

    Returns:
        Path to credentials file if found, None otherwise
    """
    # 1. Check user-provided path (current directory or absolute)
    user_creds = Path(credentials_path)
    if user_creds.exists():
        return user_creds

    # 2. Check user config directory
    home_config = Path.home() / ".gmail-to-notebooklm" / "credentials.json"
    if home_config.exists():
        return home_config

    # 3. Check embedded default credentials
    # Handle both normal Python execution and PyInstaller frozen executable
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        bundle_dir = Path(sys._MEIPASS)  # type: ignore
        embedded_creds = bundle_dir / "gmail_to_notebooklm" / "data" / "default_credentials.json"
    else:
        # Running in normal Python
        # Get the directory where this auth.py file is located
        current_file = Path(__file__).resolve()
        package_dir = current_file.parent
        embedded_creds = package_dir / "data" / "default_credentials.json"

    if embedded_creds.exists():
        return embedded_creds

    return None


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


def authenticate(
    credentials_path: str = "credentials.json",
    token_path: str = "token.json",
    scopes: Optional[list] = None,
    status_callback: Optional[Callable[[str], None]] = None,
) -> Credentials:
    """
    Authenticate with Gmail API using OAuth 2.0.

    On first run, this will open a browser window for the user to authorize
    the application. The authorization token is saved for future use.

    Args:
        credentials_path: Path to credentials.json from Google Cloud Console
        token_path: Path to save/load authentication token
        scopes: List of OAuth scopes (default: gmail.readonly)
        status_callback: Optional callback for status messages

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
    def _log(message: str):
        """Log message to callback or print."""
        if status_callback:
            status_callback(message)
        else:
            print(message)

    if scopes is None:
        scopes = SCOPES

    # Find credentials file (searches multiple locations)
    credentials_file = find_credentials_file(credentials_path)
    if not credentials_file:
        raise FileNotFoundError(
            f"Credentials file not found. Searched locations:\n"
            f"1. {credentials_path} (user-provided)\n"
            f"2. ~/.gmail-to-notebooklm/credentials.json (user config)\n"
            f"3. Embedded default credentials (if available)\n\n"
            f"For simplified setup, download the pre-built executable which includes credentials.\n"
            f"For advanced setup, see ADVANCED_SETUP.md for creating your own credentials."
        )

    # Convert to string for use with google-auth-oauthlib
    credentials_path_str = str(credentials_file)
    _log(f"Using credentials from: {credentials_file}")

    creds = None
    token_file = Path(token_path)

    # Load existing token if available
    if token_file.exists():
        try:
            with open(token_file, "rb") as token:
                creds = pickle.load(token)
        except Exception as e:
            _log(f"Warning: Could not load token file: {e}")
            _log("Will re-authenticate...")
            creds = None

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                _log("Refreshing authentication token...")
                creds.refresh(Request())
            except Exception as e:
                _log(f"Token refresh failed: {e}")
                _log("Re-authenticating...")
                creds = None

        if not creds:
            try:
                _log("Starting OAuth 2.0 authentication...")
                _log("A browser window will open for authorization.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path_str, scopes
                )
                creds = flow.run_local_server(port=0)

                # Verify we got valid credentials
                if not creds:
                    raise AuthenticationError("No credentials returned from OAuth flow")

                _log("Authentication successful!")
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
            _log(f"Authentication token saved to {token_path}")
        except Exception as e:
            import traceback
            _log(f"Warning: Could not save token: {e}")
            _log(f"Details: {traceback.format_exc()}")

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
