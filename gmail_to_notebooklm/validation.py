"""
Input validation utilities for security.

This module provides validators for file paths, email addresses,
labels, queries, and other user inputs to prevent injection attacks
and ensure data integrity.
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class PathValidator:
    """Validates file paths for security."""
    
    @staticmethod
    def validate_output_directory(path: str, base_dir: Optional[str] = None) -> Path:
        """
        Validate output directory path.
        
        Ensures path is safe and within allowed locations.
        
        Args:
            path: Directory path to validate
            base_dir: Optional base directory to restrict to
            
        Returns:
            Path: Validated absolute path
            
        Raises:
            ValidationError: If path is invalid or unsafe
        """
        if not path:
            raise ValidationError("Output directory cannot be empty")
        
        # Convert to Path object
        path_obj = Path(path).expanduser()
        
        # Check for suspicious patterns
        if ".." in str(path_obj):
            raise ValidationError("Path cannot contain '..' (directory traversal)")
        
        # Make absolute
        abs_path = path_obj.resolve()
        
        # If base_dir specified, ensure path is within it
        if base_dir:
            base_abs = Path(base_dir).expanduser().resolve()
            try:
                abs_path.relative_to(base_abs)
            except ValueError:
                raise ValidationError(
                    f"Path {path} is outside allowed directory {base_dir}"
                )
        
        return abs_path
    
    @staticmethod
    def validate_file_path(path: str, base_dir: str) -> Path:
        """
        Validate file path for writing.
        
        Args:
            path: File path to validate
            base_dir: Base directory to restrict to
            
        Returns:
            Path: Validated absolute path
            
        Raises:
            ValidationError: If path is invalid or unsafe
        """
        if not path:
            raise ValidationError("File path cannot be empty")
        
        path_obj = Path(path)
        
        # Check for absolute paths (not allowed)
        if path_obj.is_absolute():
            raise ValidationError("Absolute paths not allowed")
        
        # Check for suspicious patterns
        if ".." in str(path_obj) or str(path_obj).startswith("/"):
            raise ValidationError("Invalid path: contains '..' or starts with '/'")
        
        # Combine with base directory
        full_path = Path(base_dir) / path_obj
        abs_path = full_path.resolve()
        
        # Ensure still within base directory
        base_abs = Path(base_dir).resolve()
        try:
            abs_path.relative_to(base_abs)
        except ValueError:
            raise ValidationError(f"Path {path} escapes base directory")
        
        return abs_path
    
    @staticmethod
    def sanitize_filename(filename: str, max_length: int = 255) -> str:
        """
        Sanitize filename for safe filesystem use.
        
        Args:
            filename: Original filename
            max_length: Maximum filename length
            
        Returns:
            str: Sanitized filename
        """
        if not filename:
            return "unnamed"
        
        # Remove or replace dangerous characters
        # Keep alphanumeric, spaces, hyphens, underscores, periods
        sanitized = re.sub(r'[^\w\s\-\.]', '_', filename)
        
        # Replace multiple spaces/underscores with single
        sanitized = re.sub(r'[\s_]+', '_', sanitized)
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip('. ')
        
        # Handle reserved names on Windows
        reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                   'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                   'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
        
        name_without_ext = sanitized.rsplit('.', 1)[0].upper()
        if name_without_ext in reserved:
            sanitized = f"file_{sanitized}"
        
        # Truncate if too long, preserving extension
        if len(sanitized) > max_length:
            if '.' in sanitized:
                name, ext = sanitized.rsplit('.', 1)
                max_name_len = max_length - len(ext) - 1
                sanitized = f"{name[:max_name_len]}.{ext}"
            else:
                sanitized = sanitized[:max_length]
        
        return sanitized or "unnamed"


class EmailValidator:
    """Validates email addresses."""
    
    # RFC 5322 simplified regex
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email is invalid
        """
        if not email:
            raise ValidationError("Email address cannot be empty")
        
        email = email.strip()
        
        if not EmailValidator.EMAIL_REGEX.match(email):
            raise ValidationError(
                f"Invalid email address: {email}. "
                "Expected format: user@example.com"
            )
        
        if len(email) > 254:  # RFC 5321
            raise ValidationError("Email address too long (max 254 characters)")
        
        return email


class GmailValidator:
    """Validates Gmail-specific inputs."""
    
    @staticmethod
    def validate_label(label: str) -> str:
        """
        Validate Gmail label name.
        
        Args:
            label: Label name to validate
            
        Returns:
            str: Validated label name
            
        Raises:
            ValidationError: If label is invalid
        """
        if not label:
            raise ValidationError("Label name cannot be empty")
        
        label = label.strip()
        
        # Gmail labels can contain most characters, but check for suspicious ones
        if any(c in label for c in ['\0', '\n', '\r']):
            raise ValidationError("Label contains invalid characters")
        
        if len(label) > 225:  # Gmail limit
            raise ValidationError("Label name too long (max 225 characters)")
        
        return label
    
    @staticmethod
    def validate_query(query: str) -> str:
        """
        Validate Gmail search query.
        
        Basic validation to catch obvious syntax errors.
        
        Args:
            query: Search query to validate
            
        Returns:
            str: Validated query
            
        Raises:
            ValidationError: If query is invalid
        """
        if not query:
            return ""  # Empty query is valid
        
        query = query.strip()
        
        # Check for balanced quotes
        if query.count('"') % 2 != 0:
            raise ValidationError("Unbalanced quotes in search query")
        
        # Check for null bytes
        if '\0' in query:
            raise ValidationError("Query contains null bytes")
        
        if len(query) > 10000:  # Reasonable limit
            raise ValidationError("Query too long (max 10000 characters)")
        
        return query


class DateValidator:
    """Validates date inputs."""
    
    @staticmethod
    def validate_date_range(
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Validate date range.
        
        Args:
            start_date: Start date (ISO 8601 format)
            end_date: End date (ISO 8601 format)
            
        Returns:
            Tuple of parsed datetime objects
            
        Raises:
            ValidationError: If dates are invalid
        """
        start_dt = None
        end_dt = None
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
            except ValueError:
                raise ValidationError(
                    f"Invalid start date: {start_date}. "
                    "Expected ISO 8601 format (YYYY-MM-DD)"
                )
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date)
            except ValueError:
                raise ValidationError(
                    f"Invalid end date: {end_date}. "
                    "Expected ISO 8601 format (YYYY-MM-DD)"
                )
        
        # Check logical consistency
        if start_dt and end_dt and start_dt > end_dt:
            raise ValidationError("Start date must be before end date")
        
        return start_dt, end_dt


class SizeValidator:
    """Validates size limits."""
    
    @staticmethod
    def validate_size_limit(size: int, min_size: int = 1024, max_size: int = 1073741824) -> int:
        """
        Validate size limit value.
        
        Args:
            size: Size in bytes
            min_size: Minimum allowed size (default 1KB)
            max_size: Maximum allowed size (default 1GB)
            
        Returns:
            int: Validated size
            
        Raises:
            ValidationError: If size is invalid
        """
        if not isinstance(size, int):
            raise ValidationError("Size must be an integer")
        
        if size < min_size:
            raise ValidationError(
                f"Size too small: {size} bytes. Minimum: {min_size} bytes"
            )
        
        if size > max_size:
            raise ValidationError(
                f"Size too large: {size} bytes. Maximum: {max_size} bytes"
            )
        
        return size
    
    @staticmethod
    def parse_size_string(size_str: str) -> int:
        """
        Parse size string (e.g., "50MB", "1GB") to bytes.
        
        Args:
            size_str: Size string
            
        Returns:
            int: Size in bytes
            
        Raises:
            ValidationError: If size string is invalid
        """
        size_str = size_str.strip().upper()
        
        # Extract number and unit
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$', size_str)
        if not match:
            raise ValidationError(
                f"Invalid size format: {size_str}. "
                "Expected format: 50MB, 1GB, etc."
            )
        
        number, unit = match.groups()
        number = float(number)
        
        # Convert to bytes
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
        }
        
        multiplier = multipliers.get(unit, 1)
        return int(number * multiplier)
