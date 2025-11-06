# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Email preview before export
- Multiple label support in one command
- Scheduled exports (Task Scheduler integration)
- Integration tests
- Docker containerization
- Parallel processing
- Email thread reconstruction
- Custom Markdown templates

## [0.3.0] - 2025-11-06

### Added - Phase 2 & 3: Desktop GUI + Advanced Features

#### Windows Desktop GUI (Phase 2A)
- **Complete Tkinter GUI Application**: Zero-dependency desktop interface
- **Main Window**: Label selection, all Phase 1 filters, real-time auth status
- **OAuth Setup Wizard**: 5-step guided setup for first-time users
- **Settings Dialog**: Tabbed interface for credentials, defaults, and advanced options
- **Export Progress Dialog**: Real-time progress with cancel support
- **Menu Bar**: Easy access to Setup, Settings, Profiles, and History

#### Enhanced DevOps CLI (Phase 2B)
- **--dry-run**: Validate settings without creating files
- **--quiet**: Suppress output except errors (CI/CD friendly)
- **--json-output**: Machine-readable JSON for scripting
- **--list-labels**: Quick label discovery
- **Proper Exit Codes**: 0-5, 130 for automation
- **ExportEngine Integration**: Unified behavior with GUI

#### Advanced Features (Phase 3)
- **Export History System**: SQLite database tracking all exports
- **Export Profiles**: Save/load common configurations
- **History Dialog**: View past exports with statistics
- **Profiles Dialog**: Manage saved configurations
- **Statistics Dashboard**: Success rates, average duration, usage patterns
- **Profile Loading**: One-click application of saved settings

### Technical

#### Core Architecture
- **UI-Agnostic Core** (core.py): ExportEngine with callback support
- **History Tracking** (history.py): SQLite with search and statistics
- **Profile Management** (profiles.py): JSON-based configuration storage
- **Callback Pattern**: Progress and status updates for any UI
- **Optional Dependencies**: Graceful degradation if features unavailable

#### New Entry Points
- `gmail-to-notebooklm-gui`: Launch desktop application
- `python -m gmail_to_notebooklm.gui.main`: Alternative GUI launch

#### Exit Codes
- 0: Success
- 1: Configuration error
- 2: Authentication error
- 3: API error
- 4: No results found
- 5: Export error
- 130: User cancelled

### Code Statistics
- **Total Lines Added**: ~4,000
- **New Files**: 13
- **Modified Files**: 10
- **GUI Code**: ~2,400 lines
- **CLI Code**: ~450 lines
- **History/Profiles**: ~570 lines
- **Core Engine**: ~465 lines

## [0.2.0] - 2025-11-06

### Added
- **Gmail Query Syntax Support** (#1): Use Gmail search queries with `--query` flag
- **YAML Configuration** (#2): Store settings in `.gmail-to-notebooklm.yaml` file
- **Date Range Filtering** (#3): Filter emails with `--after` and `--before` flags
- **Sender/Recipient Filtering** (#4): Filter by sender (`--from`), recipient (`--to`), or exclude senders (`--exclude-from`)
- **Rich Progress Bars** (#5): Beautiful progress visualization with spinners and completion percentages
- **Index File Generation** (#6): Create INDEX.md table of contents with `--create-index` flag
- **Date-Based Organization** (#7): Organize emails into date subdirectories with `--organize-by-date` flag
- **Date Format Options**: Support for YYYY/MM, YYYY-MM, YYYY/MM/DD, YYYY-MM-DD formats via `--date-format` flag
- **Comprehensive Test Suite** (#8): 67 tests with 53% code coverage
- **Full Documentation** (#9): Updated all documentation with new features and examples

### Changed
- `--label` flag is now optional when using `--query`
- Progress output now uses Rich library for better visualization
- Email fetching, parsing, and conversion now show detailed progress
- Warnings now displayed in color-coded format

### Technical
- Added `rich` library for terminal UI
- Added `pyyaml` library for configuration files
- Improved error handling in query building
- Enhanced utils module with date validation and query building functions
- Config module with validation and CLI argument merging
- Version bumped from 0.1.0 to 0.2.0

### Documentation
- Updated README.md with new features
- Updated USAGE.md with comprehensive examples
- Updated CONFIGURATION.md with YAML format
- Updated QUICKSTART.md with new options
- Added PHASE1_ISSUES.md and PHASE1_ROADMAP.md for development tracking

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

[Unreleased]: https://github.com/pgd1001/gmail-to-notebooklm/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/pgd1001/gmail-to-notebooklm/releases/tag/v0.2.0
[0.1.0]: https://github.com/pgd1001/gmail-to-notebooklm/releases/tag/v0.1.0
