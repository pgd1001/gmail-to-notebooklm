"""Configuration file loading and validation."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from .validation import PathValidator, SizeValidator, ValidationError
from .audit import get_audit_logger


class ConfigError(Exception):
    """Raised when configuration loading or validation fails."""
    pass


class Config:
    """
    Configuration loader for YAML config files.

    Loads settings from .gmail-to-notebooklm.yaml file and provides
    validation and default values.
    """

    DEFAULT_CONFIG_FILENAME = ".gmail-to-notebooklm.yaml"

    # Default configuration values
    DEFAULTS = {
        "output_dir": "./output",
        "max_results": None,
        "verbose": False,
        "overwrite": False,
        "credentials_path": "credentials.json",
        "token_path": "token.json",
        "create_index": False,
        "organize_by_date": False,
        "date_format": "YYYY/MM",
        # Security settings
        "use_encryption": True,
        "enable_audit_logging": True,
        "enable_rate_limiting": True,
        "requests_per_second": 10.0,
        "max_email_size_mb": 50,
        "max_batch_size_mb": 500,
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to config file. If None, looks for default file.
        """
        self.config_path = config_path
        self.config_data: Dict[str, Any] = {}
        self._load_config()

    def _find_config_file(self) -> Optional[Path]:
        """
        Find configuration file in standard locations.

        Search order:
        1. Explicit path (if provided)
        2. Current directory (./.gmail-to-notebooklm.yaml)
        3. Home directory (~/.gmail-to-notebooklm.yaml)

        Returns:
            Path to config file if found, None otherwise
        """
        # If explicit path provided, use it
        if self.config_path:
            path = Path(self.config_path)
            if path.exists():
                return path
            raise ConfigError(f"Config file not found: {self.config_path}")

        # Check current directory
        current_dir_config = Path.cwd() / self.DEFAULT_CONFIG_FILENAME
        if current_dir_config.exists():
            return current_dir_config

        # Check home directory
        home_config = Path.home() / self.DEFAULT_CONFIG_FILENAME
        if home_config.exists():
            return home_config

        # No config file found
        return None

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        config_file = self._find_config_file()
        
        # Get audit logger
        audit_logger = get_audit_logger()

        if not config_file:
            # No config file found, use defaults
            self.config_data = self.DEFAULTS.copy()
            return

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded_config = yaml.safe_load(f)

            if loaded_config is None:
                loaded_config = {}

            if not isinstance(loaded_config, dict):
                raise ConfigError(
                    f"Invalid config file format: expected dictionary, got {type(loaded_config)}"
                )

            # Merge with defaults (loaded config takes precedence)
            self.config_data = {**self.DEFAULTS, **loaded_config}
            
            # Sanitize environment variables if present
            self._sanitize_env_vars()

            print(f"Loaded configuration from {config_file}")
            
            # Log configuration load
            if audit_logger:
                audit_logger.log_config_loaded(str(config_file), validation_status='pending')

        except yaml.YAMLError as e:
            error_msg = f"Failed to parse YAML config: {e}"
            if audit_logger:
                audit_logger.log_validation_error('config_yaml', str(config_file), error_msg)
            raise ConfigError(error_msg)
        except Exception as e:
            error_msg = f"Failed to load config file: {e}"
            if audit_logger:
                audit_logger.log_file_error('read', str(config_file), error_msg)
            raise ConfigError(error_msg)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config_data.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            Dictionary of all configuration values
        """
        return self.config_data.copy()

    def validate(self) -> None:
        """
        Validate configuration values.

        Raises:
            ConfigError: If configuration is invalid
        """
        audit_logger = get_audit_logger()
        
        try:
            # Validate output_dir
            if "output_dir" in self.config_data:
                output_dir = self.config_data["output_dir"]
                if not isinstance(output_dir, str):
                    raise ConfigError(f"output_dir must be a string, got {type(output_dir)}")
                
                # Validate path safety
                try:
                    PathValidator.validate_output_directory(output_dir)
                except ValidationError as e:
                    raise ConfigError(f"Invalid output_dir: {e}")

            # Validate max_results
            if "max_results" in self.config_data:
                max_results = self.config_data["max_results"]
                if max_results is not None and (not isinstance(max_results, int) or max_results < 1):
                    raise ConfigError(f"max_results must be a positive integer or null, got {max_results}")

            # Validate boolean fields
            boolean_fields = ["verbose", "overwrite", "create_index", "organize_by_date", 
                            "use_encryption", "enable_audit_logging", "enable_rate_limiting"]
            for field in boolean_fields:
                if field in self.config_data:
                    value = self.config_data[field]
                    if not isinstance(value, bool):
                        raise ConfigError(f"{field} must be a boolean, got {type(value)}")

            # Validate date_format
            if "date_format" in self.config_data:
                date_format = self.config_data["date_format"]
                if not isinstance(date_format, str):
                    raise ConfigError(f"date_format must be a string, got {type(date_format)}")

                valid_formats = ["YYYY/MM", "YYYY-MM", "YYYY/MM/DD", "YYYY-MM-DD"]
                if date_format not in valid_formats:
                    raise ConfigError(
                        f"date_format must be one of {valid_formats}, got '{date_format}'"
                    )
            
            # Validate requests_per_second
            if "requests_per_second" in self.config_data:
                rps = self.config_data["requests_per_second"]
                if not isinstance(rps, (int, float)) or rps < 0:
                    raise ConfigError(f"requests_per_second must be a non-negative number, got {rps}")
            
            # Validate email size limits
            if "max_email_size_mb" in self.config_data:
                size_mb = self.config_data["max_email_size_mb"]
                if not isinstance(size_mb, (int, float)) or size_mb < 1 or size_mb > 1024:
                    raise ConfigError(f"max_email_size_mb must be between 1 and 1024, got {size_mb}")
            
            if "max_batch_size_mb" in self.config_data:
                size_mb = self.config_data["max_batch_size_mb"]
                if not isinstance(size_mb, (int, float)) or size_mb < 1 or size_mb > 10240:
                    raise ConfigError(f"max_batch_size_mb must be between 1 and 10240, got {size_mb}")
            
            # Validate file paths
            path_fields = ["credentials_path", "token_path"]
            for field in path_fields:
                if field in self.config_data:
                    path = self.config_data[field]
                    if not isinstance(path, str):
                        raise ConfigError(f"{field} must be a string, got {type(path)}")
                    
                    # Check for suspicious patterns
                    if ".." in path or "\0" in path:
                        raise ConfigError(f"{field} contains invalid characters")
            
            # Log successful validation
            if audit_logger:
                audit_logger.log_config_loaded(
                    self.config_path or "default",
                    validation_status='valid'
                )
                
        except ConfigError as e:
            if audit_logger:
                audit_logger.log_validation_error('config', str(self.config_data), str(e))
            raise

    def merge_with_cli_args(self, cli_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge configuration with CLI arguments.

        CLI arguments take precedence over config file values.

        Args:
            cli_args: Dictionary of CLI arguments

        Returns:
            Merged configuration dictionary
        """
        merged = self.config_data.copy()

        # CLI args override config file
        for key, value in cli_args.items():
            if value is not None:  # Only override if explicitly set
                merged[key] = value

        return merged
    
    def _sanitize_env_vars(self) -> None:
        """Sanitize environment variables used in configuration."""
        # List of environment variables that may be used
        env_vars = [
            'GMAIL_CREDENTIALS_PATH',
            'GMAIL_TOKEN_PATH',
            'GMAIL_OUTPUT_DIR',
            'GMAIL_CONFIG_FILE',
            'GMAIL_LOG_LEVEL',
            'GMAIL_MAX_EMAIL_SIZE',
        ]
        
        for var in env_vars:
            value = os.environ.get(var)
            if value:
                # Validate length
                if len(value) > 1000:
                    raise ConfigError(f"Environment variable {var} is too long (max 1000 characters)")
                
                # Check for null bytes
                if '\0' in value:
                    raise ConfigError(f"Environment variable {var} contains null bytes")
                
                # Path-specific validation
                if 'PATH' in var or 'DIR' in var:
                    if '..' in value:
                        raise ConfigError(f"Environment variable {var} contains '..' (directory traversal)")
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value and log the change.
        
        Args:
            key: Configuration key
            value: New value
        """
        audit_logger = get_audit_logger()
        old_value = self.config_data.get(key)
        
        self.config_data[key] = value
        
        # Log configuration change
        if audit_logger and old_value != value:
            audit_logger.log_config_changed(key, old_value, value)

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """
        Load configuration from file.

        Args:
            config_path: Optional path to config file

        Returns:
            Config instance

        Raises:
            ConfigError: If config loading or validation fails
        """
        config = cls(config_path)
        config.validate()
        return config


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Convenience function to load configuration.

    Args:
        config_path: Optional path to config file

    Returns:
        Config instance with loaded configuration

    Example:
        >>> config = load_config()
        >>> output_dir = config.get("output_dir")
        >>> all_settings = config.get_all()
    """
    return Config.load(config_path)
