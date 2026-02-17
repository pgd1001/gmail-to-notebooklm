"""Tests for token encryption module."""

import pytest
from pathlib import Path
import pickle

from gmail_to_notebooklm.encryption import TokenEncryption, get_encryption


class TestTokenEncryption:
    """Test token encryption functionality."""
    
    def test_encryption_initialization(self):
        """Test encryption instance creation."""
        encryption = TokenEncryption()
        assert encryption is not None
        assert encryption._fernet is not None
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption and decryption round-trip."""
        encryption = TokenEncryption()
        original_data = b"test token data"
        
        # Encrypt
        encrypted = encryption.encrypt(original_data)
        assert encrypted != original_data
        assert len(encrypted) > len(original_data)
        
        # Decrypt
        decrypted = encryption.decrypt(encrypted)
        assert decrypted == original_data
    
    def test_encrypt_decrypt_with_unicode(self):
        """Test encryption with unicode characters."""
        encryption = TokenEncryption()
        original_data = "Hello 世界 🌍".encode('utf-8')
        
        encrypted = encryption.encrypt(original_data)
        decrypted = encryption.decrypt(encrypted)
        
        assert decrypted == original_data
        assert decrypted.decode('utf-8') == "Hello 世界 🌍"
    
    def test_decrypt_invalid_data(self):
        """Test decryption with invalid data."""
        encryption = TokenEncryption()
        invalid_data = b"not encrypted data"
        
        result = encryption.decrypt(invalid_data)
        assert result is None
    
    def test_decrypt_corrupted_data(self):
        """Test decryption with corrupted encrypted data."""
        encryption = TokenEncryption()
        original_data = b"test data"
        
        encrypted = encryption.encrypt(original_data)
        # Corrupt the data
        corrupted = encrypted[:-5] + b"xxxxx"
        
        result = encryption.decrypt(corrupted)
        assert result is None
    
    def test_is_encrypted_detection(self):
        """Test encrypted data detection."""
        encryption = TokenEncryption()
        
        # Test with encrypted data
        encrypted = encryption.encrypt(b"test")
        assert TokenEncryption.is_encrypted(encrypted) is True
        
        # Test with unencrypted data
        unencrypted = b"plain text"
        assert TokenEncryption.is_encrypted(unencrypted) is False
        
        # Test with pickle data (common for tokens)
        pickled = pickle.dumps({"token": "value"})
        assert TokenEncryption.is_encrypted(pickled) is False
    
    def test_is_encrypted_with_short_data(self):
        """Test encrypted detection with short data."""
        # Very short data should return False
        assert TokenEncryption.is_encrypted(b"x") is False
        assert TokenEncryption.is_encrypted(b"") is False
    
    def test_encrypt_file(self, tmp_path):
        """Test file encryption."""
        encryption = TokenEncryption()
        
        # Create test file
        test_file = tmp_path / "test.txt"
        test_data = b"test file content"
        test_file.write_bytes(test_data)
        
        # Encrypt file
        result = encryption.encrypt_file(test_file, backup=True)
        assert result is True
        
        # Check backup was created
        backup_file = test_file.with_suffix(test_file.suffix + '.backup')
        assert backup_file.exists()
        assert backup_file.read_bytes() == test_data
        
        # Check file is encrypted
        encrypted_data = test_file.read_bytes()
        assert encrypted_data != test_data
        assert TokenEncryption.is_encrypted(encrypted_data)
    
    def test_encrypt_file_without_backup(self, tmp_path):
        """Test file encryption without backup."""
        encryption = TokenEncryption()
        
        test_file = tmp_path / "test.txt"
        test_data = b"test content"
        test_file.write_bytes(test_data)
        
        result = encryption.encrypt_file(test_file, backup=False)
        assert result is True
        
        # Check no backup was created
        backup_file = test_file.with_suffix(test_file.suffix + '.backup')
        assert not backup_file.exists()
    
    def test_decrypt_file(self, tmp_path):
        """Test file decryption."""
        encryption = TokenEncryption()
        
        # Create and encrypt file
        test_file = tmp_path / "test.txt"
        test_data = b"test file content"
        test_file.write_bytes(test_data)
        
        encryption.encrypt_file(test_file, backup=False)
        
        # Decrypt file
        decrypted = encryption.decrypt_file(test_file)
        assert decrypted == test_data
    
    def test_decrypt_nonexistent_file(self, tmp_path):
        """Test decrypting non-existent file."""
        encryption = TokenEncryption()
        
        nonexistent = tmp_path / "nonexistent.txt"
        result = encryption.decrypt_file(nonexistent)
        assert result is None
    
    def test_key_derivation_consistency(self):
        """Test that key derivation is consistent."""
        encryption1 = TokenEncryption()
        encryption2 = TokenEncryption()
        
        # Same system should derive same key
        test_data = b"test data"
        encrypted1 = encryption1.encrypt(test_data)
        
        # Should be able to decrypt with second instance
        decrypted = encryption2.decrypt(encrypted1)
        assert decrypted == test_data
    
    def test_large_data_encryption(self):
        """Test encryption of large data."""
        encryption = TokenEncryption()
        
        # Create 1MB of data
        large_data = b"x" * (1024 * 1024)
        
        encrypted = encryption.encrypt(large_data)
        decrypted = encryption.decrypt(encrypted)
        
        assert decrypted == large_data
    
    def test_get_encryption_singleton(self):
        """Test global encryption instance."""
        enc1 = get_encryption()
        enc2 = get_encryption()
        
        # Should return same instance
        assert enc1 is enc2
        
        # Should work correctly
        test_data = b"test"
        encrypted = enc1.encrypt(test_data)
        decrypted = enc2.decrypt(encrypted)
        assert decrypted == test_data


class TestEncryptionEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_data_encryption(self):
        """Test encrypting empty data."""
        encryption = TokenEncryption()
        
        empty_data = b""
        encrypted = encryption.encrypt(empty_data)
        decrypted = encryption.decrypt(encrypted)
        
        assert decrypted == empty_data
    
    def test_binary_data_encryption(self):
        """Test encrypting binary data."""
        encryption = TokenEncryption()
        
        # Test with various binary patterns
        binary_data = bytes(range(256))
        encrypted = encryption.encrypt(binary_data)
        decrypted = encryption.decrypt(encrypted)
        
        assert decrypted == binary_data
    
    def test_encrypt_file_permission_error(self, tmp_path):
        """Test file encryption with permission error."""
        encryption = TokenEncryption()
        
        # Create read-only file
        test_file = tmp_path / "readonly.txt"
        test_file.write_bytes(b"test")
        test_file.chmod(0o444)
        
        try:
            result = encryption.encrypt_file(test_file)
            # On some systems this might succeed, on others it fails
            # Just ensure it doesn't crash
            assert result in [True, False]
        finally:
            # Restore permissions for cleanup
            test_file.chmod(0o644)
    
    def test_multiple_encryption_rounds(self):
        """Test encrypting already encrypted data."""
        encryption = TokenEncryption()
        
        original = b"test data"
        encrypted1 = encryption.encrypt(original)
        encrypted2 = encryption.encrypt(encrypted1)
        
        # Should be able to decrypt in reverse order
        decrypted1 = encryption.decrypt(encrypted2)
        assert decrypted1 == encrypted1
        
        decrypted2 = encryption.decrypt(decrypted1)
        assert decrypted2 == original
