# Gmail to NotebookLM Converter

Convert Gmail emails from a specific label into Markdown files formatted for Google NotebookLM.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This tool automates the extraction of emails from Gmail labels and converts them into clean, readable Markdown files. Each file includes essential email headers (From, To, Subject, Date) and the converted email body, making them ideal for use as knowledge sources in Google NotebookLM.

## Key Features

- **Label-based extraction**: Target specific Gmail labels for conversion
- **Rich metadata**: Includes From, To, Cc, Subject, and Date headers in each file
- **Smart HTML conversion**: Converts HTML email bodies to clean Markdown while preserving formatting
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

See [QUICKSTART.md](QUICKSTART.md) for a complete 5-minute setup guide.

## Installation

### Prerequisites

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

You'll need to create OAuth 2.0 credentials to access Gmail:

1. Follow the step-by-step guide in [OAUTH_SETUP.md](OAUTH_SETUP.md)
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

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [INSTALLATION.md](INSTALLATION.md) - Detailed installation instructions
- [OAUTH_SETUP.md](OAUTH_SETUP.md) - Google OAuth 2.0 configuration
- [USAGE.md](USAGE.md) - Comprehensive usage guide
- [CONFIGURATION.md](CONFIGURATION.md) - Configuration options
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide

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

- [ ] Implement core functionality
- [ ] Add unit tests
- [ ] Support for multiple labels
- [ ] Parallel processing for large label folders
- [ ] Optional attachment extraction
- [ ] Configuration file support
- [ ] Docker containerization

---

**Note**: This project is in early development. Implementation is in progress.
