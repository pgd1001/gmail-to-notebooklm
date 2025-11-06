"""Tests for configuration loading and validation."""

import pytest
from pathlib import Path
from gmail_to_notebooklm.config import Config, load_config, ConfigError


def test_config_defaults():
    """Test that default configuration values are loaded."""
    config = Config()

    assert config.get("output_dir") == "./output"
    assert config.get("max_results") is None
    assert config.get("verbose") is False
    assert config.get("overwrite") is False
    assert config.get("create_index") is False
    assert config.get("organize_by_date") is False
    assert config.get("date_format") == "YYYY/MM"


def test_config_get_with_default():
    """Test getting config value with default fallback."""
    config = Config()

    assert config.get("nonexistent_key", "default_value") == "default_value"
    assert config.get("output_dir", "fallback") == "./output"


def test_config_get_all():
    """Test getting all configuration values."""
    config = Config()
    all_config = config.get_all()

    assert isinstance(all_config, dict)
    assert "output_dir" in all_config
    assert "max_results" in all_config
    assert "verbose" in all_config


def test_config_validation_output_dir():
    """Test validation of output_dir field."""
    config = Config()
    config.config_data["output_dir"] = 123  # Invalid type

    with pytest.raises(ConfigError, match="output_dir must be a string"):
        config.validate()


def test_config_validation_max_results():
    """Test validation of max_results field."""
    config = Config()
    config.config_data["max_results"] = -5  # Invalid value

    with pytest.raises(ConfigError, match="max_results must be a positive integer"):
        config.validate()


def test_config_validation_boolean_fields():
    """Test validation of boolean fields."""
    config = Config()
    config.config_data["verbose"] = "yes"  # Invalid type

    with pytest.raises(ConfigError, match="verbose must be a boolean"):
        config.validate()


def test_config_validation_date_format():
    """Test validation of date_format field."""
    config = Config()
    config.config_data["date_format"] = "INVALID"

    with pytest.raises(ConfigError, match="date_format must be one of"):
        config.validate()


def test_config_merge_with_cli_args():
    """Test merging configuration with CLI arguments."""
    config = Config()

    cli_args = {
        "label": "Test Label",
        "verbose": True,
        "output_dir": None,  # Should not override
    }

    merged = config.merge_with_cli_args(cli_args)

    assert merged["label"] == "Test Label"
    assert merged["verbose"] is True
    assert merged["output_dir"] == "./output"  # From config default


def test_load_config_function():
    """Test the load_config convenience function."""
    config = load_config()

    assert isinstance(config, Config)
    assert config.get("output_dir") is not None
