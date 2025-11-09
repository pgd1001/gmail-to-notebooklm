# Gmail to NotebookLM Converter

Convert Gmail emails from a specific label into Markdown files formatted for Google NotebookLM.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This tool automates the extraction of emails from Gmail labels and converts them into clean, readable Markdown files. Each file includes essential email headers (From, To, Subject, Date) and the converted email body, making them ideal for use as knowledge sources in Google NotebookLM.

## Key Features

- **Flexible Email Search**: Use Gmail query syntax or label-based extraction
- **Advanced Filtering**: Filter by date range, sender, or recipient
- **Rich metadata**: Includes From, To, Cc, Subject, and Date headers in each file
- **Smart HTML conversion**: Converts HTML email bodies to clean Markdown while preserving formatting
- **Date-Based Organization**: Automatically organize emails into date-based subdirectories
- **Index Generation**: Create a table of contents with all exported emails
- **YAML Configuration**: Store settings in a config file with CLI override support
- **Rich Progress Bars**: Beautiful progress visualization for long operations
- **OAuth 2.0 security**: Secure, read-only access to your Gmail account
- **Batch processing**: Efficiently process multiple emails at once
- **UTF-8 encoding**: Full support for international characters

## Quick Start

```bash
# Install
pip install -r requirements.txt
pip install -e .

# Configure (see OAUTH_SETUP.md for detailed instructions)
# Place credentials.json in project root

# Run
gmail-to-notebooklm --label "Client A" --output-dir "./output"
```

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for a complete 5-minute setup guide.

## Download

### Windows Users (No Python Required)

**Recommended**: Download the standalone installer:
- [gmail-to-notebooklm-setup-0.3.0.exe](https://github.com/yourusername/gmail-to-notebooklm/releases) (35 MB)
  - Includes both CLI and GUI
  - One-click installation
  - Optional PATH integration
  - No Python required

**Portable**: Download the portable executables:
- [gmail-to-notebooklm-portable-0.3.0.zip](https://github.com/yourusername/gmail-to-notebooklm/releases) (70 MB)
  - No installation needed
  - Extract and run
  - Includes `g2n.exe` (CLI) and `g2n-gui.exe` (GUI)

### Python Users

```bash
pip install gmail-to-notebooklm
```

## Installation

### Windows Standalone

1. Download `gmail-to-notebooklm-setup-0.3.0.exe`
2. Run the installer
3. Launch from Start Menu or desktop shortcut
4. Run the Setup Wizard to configure OAuth

See [SETUP_WINDOWS.md](SETUP_WINDOWS.md) for detailed Windows installation instructions.

### Python Installation

#### Prerequisites

- Python 3.9 or higher
- Google account with Gmail
- Google Cloud Project with Gmail API enabled

### Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

For complete installation instructions, see [INSTALLATION.md](INSTALLATION.md).

### OAuth Setup

**For most users**: If you downloaded the Windows .exe, OAuth credentials are already embedded. See [SIMPLIFIED_SETUP.md](SIMPLIFIED_SETUP.md).

**For advanced users** who want to create their own credentials:

1. Follow the step-by-step guide in [ADVANCED_SETUP.md](ADVANCED_SETUP.md)
2. Download `credentials.json` from Google Cloud Console
3. Place it in the project root directory

## Usage

### Basic Command

```bash
gmail-to-notebooklm --label "My Label" --output-dir "./output"
```

### Common Options

```bash
# Specify output directory
gmail-to-notebooklm --label "Work Emails" --output-dir "./work_exports"

# Use Gmail query syntax
gmail-to-notebooklm --query "is:unread after:2024/01/01"

# Filter by date range
gmail-to-notebooklm --label "Client A" --after "2024-01-01" --before "2024-12-31"

# Filter by sender
gmail-to-notebooklm --label "Projects" --from "john@example.com"

# Organize by date with index
gmail-to-notebooklm --label "Archive" --organize-by-date --create-index

# Show help
gmail-to-notebooklm --help

# Show version
gmail-to-notebooklm --version
```

For comprehensive usage examples, see [USAGE.md](USAGE.md).

## Output Format

Each email is converted to a Markdown file with this structure:

```markdown
---
From: John Doe <john@example.com>
To: Jane Smith <jane@example.com>
Date: Mon, 15 Jan 2024 10:30:00 -0800
Subject: Project Update
---

[Email body converted to Markdown]
```

Files are named using the format: `[Sanitized_Subject]_[Email_ID].md`

## Documentation

📚 **[Complete Documentation](docs/README.md)** - All guides and documentation in one place

### Quick Links

**For End Users**:
- [Simplified Setup Guide](docs/SIMPLIFIED_SETUP.md) - Download .exe and start using (no Python needed) ⭐
- [Quick Start (5 min)](docs/QUICKSTART.md) - Fast setup for Python users
- [Usage Guide](docs/USAGE.md) - All features and examples
- [Beta Testing Program](docs/BETA_ACCESS.md) - Join the beta

**For Developers**:
- [Building with Embedded Credentials](docs/BUILDING_WITH_EMBEDDED_CREDENTIALS.md) - How to build for distribution ⭐
- [Build Installer Guide](docs/BUILD_INSTALLER.md) - Creating Windows executables
- [Development Guide](docs/DEVELOPMENT.md) - Contributing to the project
- [Distribution Strategy](docs/DISTRIBUTION.md) - Release process

**See [docs/README.md](docs/README.md) for complete documentation index**

## Project Structure

```
gmail-to-notebooklm/
├── gmail_to_notebooklm/     # Main package (to be implemented)
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── auth.py              # OAuth authentication
│   ├── gmail_client.py      # Gmail API interaction
│   ├── parser.py            # Email parsing
│   └── converter.py         # HTML to Markdown conversion
├── tests/                   # Test suite
├── examples/                # Example files
├── credentials.json         # OAuth credentials (not in git)
├── requirements.txt         # Dependencies
├── pyproject.toml          # Package configuration
└── README.md               # This file
```

## Security

- **Read-only access**: The tool only requests `gmail.readonly` scope
- **No data storage**: No emails are stored on remote servers
- **Local credentials**: All authentication tokens stay on your machine
- **Gitignore protection**: Credentials and tokens are excluded from version control

**Important**: Never commit `credentials.json` or `token.json` to version control.

## Requirements

### Python Dependencies

- `google-api-python-client` - Gmail API
- `google-auth-oauthlib` - OAuth 2.0
- `beautifulsoup4` - HTML parsing
- `html2text` - Markdown conversion
- `click` - CLI framework
- `rich` - Terminal UI and progress bars
- `pyyaml` - Configuration file support

See [requirements.txt](requirements.txt) for complete list with versions.

### Google Cloud Setup

- Google Cloud Project
- Gmail API enabled
- OAuth 2.0 credentials (Desktop app)
- Test user access configured

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Lint code
flake8
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development instructions.

## Limitations

- Email attachments are not extracted (body text only)
- No direct NotebookLM upload (manual upload required)
- One-way sync only (extraction, not synchronization)
- Gmail API rate limits apply

## Troubleshooting

### "credentials.json not found"

Place the OAuth credentials file in the project root directory. See [OAUTH_SETUP.md](OAUTH_SETUP.md).

### "Access denied" or "Permission denied"

Ensure your Google account is added as a test user in the OAuth consent screen.

### "Module not found" errors

Activate your virtual environment and reinstall dependencies:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

For more troubleshooting, see [INSTALLATION.md](INSTALLATION.md#troubleshooting).

## Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [Google Gmail API](https://developers.google.com/gmail/api)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [html2text](https://github.com/Alir3z4/html2text/)

## Support

- **Documentation**: See the [docs](.) folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues)
- **Gmail API**: [Google Support](https://developers.google.com/gmail/api/support)

## Roadmap

### Version 0.2.0 (Completed) ✅
- [x] Implement core functionality
- [x] Add unit tests (53% coverage)
- [x] Gmail query syntax support
- [x] Date range filtering
- [x] Sender/recipient filtering
- [x] Index file generation
- [x] Date-based organization
- [x] Configuration file support (YAML)
- [x] Rich progress bars

### Future Versions
- [ ] Support for multiple labels in one command
- [ ] Parallel processing for large label folders
- [ ] Optional attachment extraction
- [ ] Docker containerization
- [ ] Email thread reconstruction
- [ ] Custom Markdown templates
