"""
Tests for audit logging functionality.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from gmail_to_notebooklm.audit import (
    AuditLogger,
    get_audit_logger,
)


class TestAuditLogger:
    """Test audit logger functionality."""
    
    def test_audit_logger_initialization(self, tmp_path):
        """Test audit logger initializes correctly."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        assert logger.log_file == Path(log_file)
    
    def test_log_export_started(self, tmp_path):
        """Test logging export started event."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        logger.log_export_started(
            operation_id="test123",
            label="INBOX",
            query="test query"
        )
        
        # Read log file
        with open(log_file) as f:
            content = f.read()
        
        # Check that event was logged
        assert "export_started" in content
        assert "test123" in content
    
    def test_log_auth_succeeded(self, tmp_path):
        """Test logging authentication success."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        logger.log_auth_succeeded("user@example.com", scopes=["gmail.readonly"])
        
        with open(log_file) as f:
            content = f.read()
        
        assert "auth_succeeded" in content
        assert "user@example.com" in content
    
    def test_log_config_loaded(self, tmp_path):
        """Test logging configuration load."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        logger.log_config_loaded("config.yaml", validation_status="valid")
        
        with open(log_file) as f:
            content = f.read()
        
        assert "config_loaded" in content
        assert "config.yaml" in content
    
    def test_log_config_changed(self, tmp_path):
        """Test logging configuration change."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        logger.log_config_changed("max_results", old_value="100", new_value="200")
        
        with open(log_file) as f:
            content = f.read()
        
        assert "config_changed" in content
        assert "max_results" in content
    
    def test_log_api_error(self, tmp_path):
        """Test logging API error."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        logger.log_api_error("gmail.messages.list", error_code=429, error_message="Rate limit exceeded")
        
        with open(log_file) as f:
            content = f.read()
        
        assert "api_error" in content
        assert "gmail.messages.list" in content
    
    def test_get_audit_logger_singleton(self, tmp_path):
        """Test get_audit_logger returns singleton."""
        log_file = tmp_path / "audit.log"
        
        logger1 = get_audit_logger(str(log_file))
        logger2 = get_audit_logger(str(log_file))
        
        assert logger1 is logger2


