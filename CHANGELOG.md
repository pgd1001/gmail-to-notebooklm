# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Core functionality implementation
- Gmail API integration
- OAuth 2.0 authentication
- HTML to Markdown conversion
- CLI interface
- Unit test suite
- Integration tests
- Docker containerization
- Configuration file support
- Multiple label support
- Parallel processing

## [0.1.0] - 2024-01-15

### Added
- Initial project structure
- Build documentation suite:
  - `requirements.txt` - Python dependencies
  - `pyproject.toml` - Modern Python packaging configuration
  - `setup.py` - Traditional setup script
  - `.gitignore` - Git exclusions including credentials
  - `MANIFEST.in` - Package distribution manifest
  - `pytest.ini` - Test configuration
  - `.flake8` - Linting configuration
- User documentation:
  - `README.md` - Project overview and quick start
  - `INSTALLATION.md` - Detailed installation guide
  - `OAUTH_SETUP.md` - Google OAuth 2.0 setup instructions
  - `USAGE.md` - Comprehensive usage guide
  - `CONFIGURATION.md` - Configuration options reference
  - `QUICKSTART.md` - 5-minute getting started guide
  - `DEVELOPMENT.md` - Developer contributing guide
  - `CLAUDE.md` - AI assistant guidance
- Project metadata:
  - `LICENSE` - MIT License
  - `CHANGELOG.md` - This file
- Configuration examples:
  - `.env.example` - Environment variables template
  - `Makefile` - Development commands
- Example files:
  - `examples/sample_credentials.json` - OAuth credentials structure

### Documentation
- Comprehensive OAuth 2.0 setup guide with troubleshooting
- Step-by-step installation instructions for Windows, macOS, and Linux
- Detailed usage examples and common workflows
- Configuration reference with environment variables and YAML config
- Development guide with testing, linting, and contribution guidelines

### Infrastructure
- Python 3.9+ support
- Virtual environment setup instructions
- Pre-commit hooks configuration
- CI/CD ready structure (workflows to be added)
- Type checking with mypy
- Code formatting with black and isort
- Linting with flake8

### Security
- Credentials excluded from version control
- Read-only Gmail API scope
- OAuth 2.0 best practices documented
- Token security guidelines

## Release Types

- **Major** (X.0.0): Breaking changes, major new features
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, minor improvements

## Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

---

## Template for Future Releases

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing features

### Deprecated
- Features marked for removal

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security patches
```

[Unreleased]: https://github.com/yourusername/gmail-to-notebooklm/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/gmail-to-notebooklm/releases/tag/v0.1.0
