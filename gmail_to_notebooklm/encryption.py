"""
Token encryption utilities for secure credential storage.

This module provides encryption/decryption functionality for OAuth tokens
using Fernet (symmetric encryption) with system-derived keys.
"""

import base64
import hashlib
import os
import socket
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class TokenEncryption:
    """Handles encryption and decryption of OAuth tokens."""
    
    def __init__(self):
        """Initialize encryption with system-derived key."""
        self._fernet = self._create_fernet()
    
    def _derive_key(self) -> bytes:
        """
        Derive encryption key from system information.
        
        Uses hostname and user home directory as salt to ensure
        different keys per user/machine.
        
        Returns:
            bytes: Derived encryption key
        """
        # Create salt from system-specific information
        hostname = socket.gethostname()
        home_dir = str(Path.home())
        salt_string = f"{hostname}:{home_dir}"
        salt = hashlib.sha256(salt_string.encode()).digest()
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        # Use a fixed password combined with salt
        password = b"gmail-to-notebooklm-v1"
        key = base64.urlsafe_b64encode(kdf.derive(password))
        
        return key
    
    def _create_fernet(self) -> Fernet:
        """
        Create Fernet cipher with derived key.
        
        Returns:
            Fernet: Initialized Fernet cipher
        """
        key = self._derive_key()
        return Fernet(key)
    
    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data using Fernet.
        
        Args:
            data: Raw bytes to encrypt
            
        Returns:
            bytes: Encrypted data
        """
        return self._fernet.encrypt(data)
    
    def decrypt(self, encrypted_data: bytes) -> Optional[bytes]:
        """
        Decrypt data using Fernet.
        
        Args:
            encrypted_data: Encrypted bytes to decrypt
            
        Returns:
            bytes: Decrypted data, or None if decryption fails
        """
        try:
            return self._fernet.decrypt(encrypted_data)
        except InvalidToken:
            return None
    
    def encrypt_file(self, file_path: Path, backup: bool = True) -> bool:
        """
        Encrypt a file in place.
        
        Args:
            file_path: Path to file to encrypt
            backup: Whether to create a backup before encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read original file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Create backup if requested
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                with open(backup_path, 'wb') as f:
                    f.write(data)
            
            # Encrypt and write
            encrypted_data = self.encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception:
            return False
    
    def decrypt_file(self, file_path: Path) -> Optional[bytes]:
        """
        Decrypt a file and return its contents.
        
        Args:
            file_path: Path to encrypted file
            
        Returns:
            bytes: Decrypted file contents, or None if decryption fails
        """
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            return self.decrypt(encrypted_data)
        except Exception:
            return None
    
    @staticmethod
    def is_encrypted(data: bytes) -> bool:
        """
        Check if data appears to be Fernet-encrypted.
        
        Fernet tokens start with a version byte (0x80) followed by
        a timestamp, so we can do a basic check.
        
        Args:
            data: Data to check
            
        Returns:
            bool: True if data appears encrypted
        """
        # Fernet tokens are base64-encoded and start with specific bytes
        # This is a heuristic check
        if len(data) < 10:
            return False
        
        try:
            # Try to decode as base64
            decoded = base64.urlsafe_b64decode(data)
            # Fernet version byte is 0x80
            return decoded[0] == 0x80
        except Exception:
            return False


# Global instance for convenience
_encryption = None


def get_encryption() -> TokenEncryption:
    """
    Get global TokenEncryption instance.
    
    Returns:
        TokenEncryption: Global encryption instance
    """
    global _encryption
    if _encryption is None:
        _encryption = TokenEncryption()
    return _encryption
