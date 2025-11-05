"""Tests for authentication module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from gmail_to_notebooklm.auth import authenticate, revoke_token, AuthenticationError


class TestAuthentication:
    """Tests for OAuth 2.0 authentication."""

    def test_authenticate_missing_credentials(self, tmp_path):
        """Test authentication with missing credentials file."""
        fake_creds_path = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError) as exc_info:
            authenticate(credentials_path=str(fake_creds_path))

        assert "Credentials file not found" in str(exc_info.value)
        assert "OAUTH_SETUP.md" in str(exc_info.value)

    @patch("gmail_to_notebooklm.auth.InstalledAppFlow")
    @patch("gmail_to_notebooklm.auth.pickle")
    def test_authenticate_first_run(
        self, mock_pickle, mock_flow, tmp_path, mock_credentials
    ):
        """Test first-time authentication flow."""
        # Create fake credentials file
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text('{"installed": {}}')

        token_file = tmp_path / "token.json"

        # Mock the flow
        flow_instance = Mock()
        flow_instance.run_local_server.return_value = mock_credentials
        mock_flow.from_client_secrets_file.return_value = flow_instance

        # Mock pickle dump
        mock_pickle.dump = Mock()

        # Authenticate
        with patch("builtins.open", mock_open()):
            creds = authenticate(
                credentials_path=str(creds_file), token_path=str(token_file)
            )

        assert creds == mock_credentials
        mock_flow.from_client_secrets_file.assert_called_once()

    def test_revoke_token(self, tmp_path):
        """Test token revocation."""
        token_file = tmp_path / "token.json"
        token_file.write_text("token_data")

        revoke_token(token_path=str(token_file))

        assert not token_file.exists()

    def test_revoke_nonexistent_token(self, tmp_path, capsys):
        """Test revoking non-existent token."""
        token_file = tmp_path / "nonexistent.json"

        revoke_token(token_path=str(token_file))

        captured = capsys.readouterr()
        assert "No token file found" in captured.out
