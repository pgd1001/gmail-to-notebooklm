"""
Audit logging for security monitoring and compliance.

This module provides structured audit logging for all security-relevant
events including exports, authentication, and configuration changes.
"""

import json
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import os


class AuditLogger:
    """Handles audit logging with rotation and structured format."""
    
    def __init__(
        self,
        log_file: Optional[Path] = None,
        log_level: str = "INFO",
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        backup_count: int = 30,  # 30 days
        json_format: bool = True
    ):
        """
        Initialize audit logger.
        
        Args:
            log_file: Path to log file (default: ~/.gmail-to-notebooklm/audit.log)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            max_bytes: Maximum log file size before rotation
            backup_count: Number of backup files to keep
            json_format: Whether to use JSON format (vs human-readable)
        """
        self.json_format = json_format
        
        # Default log file location
        if log_file is None:
            log_dir = Path.home() / '.gmail-to-notebooklm'
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / 'audit.log'
        
        self.log_file = Path(log_file)
        
        # Create logger
        self.logger = logging.getLogger('gmail_to_notebooklm.audit')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Add rotating file handler
        handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        
        # Set formatter
        if json_format:
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def _sanitize_value(self, value: Any) -> Any:
        """
        Sanitize sensitive values for logging.
        
        Args:
            value: Value to sanitize
            
        Returns:
            Sanitized value
        """
        if isinstance(value, str):
            # Replace home directory with ~
            home = str(Path.home())
            if home in value:
                value = value.replace(home, '~')
        
        return value
    
    def _create_log_entry(
        self,
        event_type: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create structured log entry.
        
        Args:
            event_type: Type of event
            message: Human-readable message
            **kwargs: Additional fields
            
        Returns:
            Dict containing log entry
        """
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event_type': event_type,
            'message': message,
        }
        
        # Add additional fields, sanitizing sensitive data
        for key, value in kwargs.items():
            entry[key] = self._sanitize_value(value)
        
        return entry
    
    def _log(self, level: str, entry: Dict[str, Any]):
        """
        Log entry at specified level.
        
        Args:
            level: Log level (info, warning, error)
            entry: Log entry dict
        """
        if self.json_format:
            message = json.dumps(entry)
        else:
            message = f"{entry['event_type']}: {entry['message']}"
            if len(entry) > 3:  # More than timestamp, event_type, message
                details = {k: v for k, v in entry.items() 
                          if k not in ['timestamp', 'event_type', 'message']}
                message += f" | {json.dumps(details)}"
        
        log_method = getattr(self.logger, level.lower())
        log_method(message)
    
    # Export Operations
    
    def log_export_started(
        self,
        operation_id: str,
        label: str,
        query: Optional[str] = None,
        output_dir: Optional[str] = None
    ):
        """Log export operation start."""
        entry = self._create_log_entry(
            'export_started',
            f'Export started for label: {label}',
            operation_id=operation_id,
            label=label,
            query=query,
            output_dir=output_dir
        )
        self._log('info', entry)
    
    def log_export_completed(
        self,
        operation_id: str,
        files_created: int,
        duration_seconds: float,
        success: bool = True
    ):
        """Log export operation completion."""
        entry = self._create_log_entry(
            'export_completed',
            f'Export completed: {files_created} files in {duration_seconds:.2f}s',
            operation_id=operation_id,
            files_created=files_created,
            duration_seconds=duration_seconds,
            success=success
        )
        self._log('info', entry)
    
    def log_export_failed(
        self,
        operation_id: str,
        error_message: str,
        error_type: Optional[str] = None
    ):
        """Log export operation failure."""
        entry = self._create_log_entry(
            'export_failed',
            f'Export failed: {error_message}',
            operation_id=operation_id,
            error_message=error_message,
            error_type=error_type
        )
        self._log('error', entry)
    
    # Authentication Events
    
    def log_auth_started(self, method: str = 'oauth2'):
        """Log authentication start."""
        entry = self._create_log_entry(
            'auth_started',
            f'Authentication started: {method}',
            method=method
        )
        self._log('info', entry)
    
    def log_auth_succeeded(self, user_email: Optional[str] = None, scopes: Optional[list] = None):
        """Log successful authentication."""
        entry = self._create_log_entry(
            'auth_succeeded',
            f'Authentication succeeded for user: {user_email or "unknown"}',
            user_email=user_email,
            scopes=scopes
        )
        self._log('info', entry)
    
    def log_auth_failed(self, error_message: str):
        """Log authentication failure."""
        entry = self._create_log_entry(
            'auth_failed',
            f'Authentication failed: {error_message}',
            error_message=error_message
        )
        self._log('warning', entry)
    
    def log_token_refreshed(self, success: bool = True):
        """Log token refresh."""
        entry = self._create_log_entry(
            'token_refreshed',
            f'Token refresh {"succeeded" if success else "failed"}',
            success=success
        )
        self._log('info' if success else 'warning', entry)
    
    # Configuration Events
    
    def log_config_loaded(self, config_file: str, validation_status: str = 'valid'):
        """Log configuration file load."""
        entry = self._create_log_entry(
            'config_loaded',
            f'Configuration loaded from: {config_file}',
            config_file=config_file,
            validation_status=validation_status
        )
        self._log('info', entry)
    
    def log_config_changed(
        self,
        parameter: str,
        old_value: Optional[Any] = None,
        new_value: Optional[Any] = None
    ):
        """Log configuration change."""
        # Sanitize sensitive values
        if 'password' in parameter.lower() or 'token' in parameter.lower():
            old_value = '***' if old_value else None
            new_value = '***' if new_value else None
        
        entry = self._create_log_entry(
            'config_changed',
            f'Configuration changed: {parameter}',
            parameter=parameter,
            old_value=old_value,
            new_value=new_value
        )
        self._log('info', entry)
    
    # Error Events
    
    def log_api_error(
        self,
        endpoint: str,
        error_code: Optional[int] = None,
        error_message: Optional[str] = None
    ):
        """Log API error."""
        entry = self._create_log_entry(
            'api_error',
            f'API error on {endpoint}: {error_message or "unknown"}',
            endpoint=endpoint,
            error_code=error_code,
            error_message=error_message
        )
        self._log('error', entry)
    
    def log_file_error(
        self,
        operation: str,
        file_path: str,
        error_message: str
    ):
        """Log file operation error."""
        entry = self._create_log_entry(
            'file_error',
            f'File {operation} error: {error_message}',
            operation=operation,
            file_path=file_path,
            error_message=error_message
        )
        self._log('error', entry)
    
    def log_validation_error(
        self,
        validation_type: str,
        invalid_value: str,
        error_message: str
    ):
        """Log validation error."""
        # Sanitize potentially sensitive values
        if len(invalid_value) > 100:
            invalid_value = invalid_value[:100] + '...'
        
        entry = self._create_log_entry(
            'validation_error',
            f'Validation error ({validation_type}): {error_message}',
            validation_type=validation_type,
            invalid_value=invalid_value,
            error_message=error_message
        )
        self._log('warning', entry)
    
    # Rate Limiting Events
    
    def log_rate_limit_hit(self, endpoint: str, retry_after: Optional[int] = None):
        """Log rate limit hit."""
        entry = self._create_log_entry(
            'rate_limit_hit',
            f'Rate limit hit on {endpoint}',
            endpoint=endpoint,
            retry_after=retry_after
        )
        self._log('warning', entry)
    
    def log_rate_limit_recovered(self, endpoint: str):
        """Log rate limit recovery."""
        entry = self._create_log_entry(
            'rate_limit_recovered',
            f'Recovered from rate limit on {endpoint}',
            endpoint=endpoint
        )
        self._log('info', entry)


# Global audit logger instance
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger(
    enabled: bool = True,
    **kwargs
) -> Optional[AuditLogger]:
    """
    Get global audit logger instance.
    
    Args:
        enabled: Whether audit logging is enabled
        **kwargs: Arguments to pass to AuditLogger constructor
        
    Returns:
        AuditLogger instance or None if disabled
    """
    global _audit_logger
    
    if not enabled:
        return None
    
    if _audit_logger is None:
        _audit_logger = AuditLogger(**kwargs)
    
    return _audit_logger


def configure_audit_logging(
    enabled: bool = True,
    **kwargs
) -> Optional[AuditLogger]:
    """
    Configure global audit logging.
    
    Args:
        enabled: Whether to enable audit logging
        **kwargs: Arguments to pass to AuditLogger constructor
        
    Returns:
        Configured AuditLogger instance or None
    """
    global _audit_logger
    
    if enabled:
        _audit_logger = AuditLogger(**kwargs)
    else:
        _audit_logger = None
    
    return _audit_logger
