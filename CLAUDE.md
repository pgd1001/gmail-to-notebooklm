<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a mature, production-ready Python application that converts Gmail emails from specific labels into Markdown files formatted for Google NotebookLM. The tool extracts email headers (From, To, Cc, Subject, Date) and body content, converting HTML to Markdown while preserving formatting.

**Current Status:** Production Beta (v0.3.0) - Fully implemented with both CLI and GUI interfaces, comprehensive documentation, and Windows executable distribution.

## Architecture

The application follows a modular design with complete implementations of all components:

### Core Modules (`gmail_to_notebooklm/`)

1. **Authentication Module** (`auth.py` - 209 lines)
   - OAuth 2.0 flow with Google Gmail API
   - Multi-location credential detection (user-provided, user config, embedded default)
   - PyInstaller-compatible credential handling
   - Token refresh and persistence
   - Comprehensive error handling

2. **Gmail API Integration** (`gmail_client.py` - 261 lines)
   - Full Gmail API client with label-based email fetching
   - Gmail query syntax support (advanced search)
   - Batch message retrieval with progress callbacks
   - Label discovery and listing

3. **Email Parser** (`parser.py` - 238 lines)
   - MIME message parsing for multipart content
   - Header extraction (From, To, Cc, Subject, Date, Message-ID)
   - HTML and plain text body handling
   - Base64url decoding for message content
   - Batch parsing with progress tracking

4. **Markdown Converter** (`converter.py` - 272 lines)
   - HTML to Markdown conversion using html2text library
   - BeautifulSoup HTML cleaning and normalization
   - YAML front matter with email metadata
   - Configurable text wrapping and formatting
   - Link and image preservation

5. **Export Engine** (`core.py` - 492 lines)
   - UI-agnostic export orchestration with 5-step workflow
   - Progress callbacks for real-time UI updates
   - Cancellation support mid-export
   - Dry-run validation mode
   - Statistics tracking and error collection

6. **Configuration Management** (`config.py` - 228 lines)
   - YAML configuration file support
   - Default value management and merging
   - CLI argument override system
   - Multi-location config search

7. **Utility Functions** (`utils.py` - 498 lines)
   - Filename sanitization
   - Date range and sender query building
   - Index file generation (INDEX.md)
   - Date-based subdirectory organization
   - Text formatting and truncation

8. **Export History** (`history.py` - 465 lines)
   - SQLite database for tracking exports
   - Metadata storage and retrieval
   - Statistics aggregation
   - Search and filter capabilities

9. **Profile Management** (`profiles.py` - 70 lines)
   - Save/load export configurations
   - JSON-based persistence
   - Quick re-apply of saved settings

### CLI Application (`main.py` - 429 lines)

Complete command-line interface with 25+ options:
- `--label` - Filter by Gmail label
- `--query` - Gmail advanced search syntax
- `--after/--before` - Date range filtering
- `--from/--to/--exclude-from` - Sender/recipient filters
- `--output-dir` - Custom output location
- `--max-results` - Limit email count
- `--organize-by-date` - Date-based subdirectories
- `--create-index` - Generate INDEX.md table of contents
- `--dry-run` - Validate without exporting
- `--list-labels` - List available Gmail labels
- `--json-output` - Machine-readable output
- `--quiet` - CI/CD friendly mode

Entry points: `gmail-to-notebooklm`, `g2n`

### GUI Application (`gmail_to_notebooklm/gui/`)

Full-featured Tkinter desktop application (~2,400 lines) with:

- **Main Window** (`main_window.py`) - Label selection, filter options, export button
- **OAuth Wizard** (`oauth_wizard.py`) - 5-step credential setup wizard
- **Settings Dialog** (`settings_dialog.py`) - Credential management, default settings
- **Export Progress Dialog** (`export_dialog.py`) - Real-time progress tracking, 5-step status
- **History Dialog** (`history_dialog.py`) - Past exports dashboard, statistics, re-export
- **Profiles Dialog** (`profiles_dialog.py`) - Save/load export configurations

Entry points: `gmail-to-notebooklm-gui`, `g2n-gui`

### Windows Distribution

- **Executables**: `g2n.exe` (CLI, 33.5MB), `g2n-gui.exe` (GUI, 36.5MB)
- **Installer**: Inno Setup configuration (`installer.iss`) with one-click installation
- **Embedded Credentials**: Optional credential embedding for simplified setup
- **No Python Required**: Standalone executables work without Python installation

### Output Format

Each generated Markdown file includes a YAML-style header block followed by the converted email body:

```markdown
---
From: [Sender Name <sender@example.com>]
To: [Recipient Name <recipient@example.com>]
Cc: [CC Name <cc@example.com>] (Optional)
Date: [Full Date and Time]
Subject: [Email Subject Line]
---

[Converted Email Body in Markdown]
```

File naming convention: `[Sanitized_Subject_Line]_[Shortened_Email_ID].md`

## Development Commands

### Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
pytest

# Run tests with coverage
pytest --cov=gmail_to_notebooklm

# Format code
black gmail_to_notebooklm tests

# Lint code
flake8 gmail_to_notebooklm tests

# Type check
mypy gmail_to_notebooklm
```

### Running the Application

```bash
# CLI mode - using installed entry point
g2n --label "Client A" --output-dir "output"

# CLI mode - using Python module
python -m gmail_to_notebooklm.main --label "Client A" --output-dir "output"

# GUI mode - using installed entry point
g2n-gui

# GUI mode - using Python module
python -m gmail_to_notebooklm.gui.main

# List available labels
g2n --list-labels

# Dry-run to validate without exporting
g2n --label "Inbox" --dry-run
```

### Building Executables

```bash
# CLI executable
python -m PyInstaller g2n.spec

# GUI executable
python -m PyInstaller g2n-gui.spec

# Windows installer
# (Requires Inno Setup - see docs/BUILD_INSTALLER.md)
```

### Dependencies

**Production** (8 packages):
- `google-api-python-client` - Gmail API interaction
- `google-auth-oauthlib` - OAuth 2.0 authentication
- `beautifulsoup4` - HTML parsing
- `html2text` - HTML to Markdown conversion
- `click` - CLI framework
- `rich` - Terminal UI and progress bars
- `PyYAML` - Configuration file support
- `python-dateutil` - Date parsing and handling

**Development** (6 packages):
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting
- `isort` - Import sorting
- `mypy` - Type checking

### Authentication

The application supports three credential methods:

1. **Interactive OAuth** (Recommended for first-time users)
   - Application opens browser for authorization
   - Tokens stored in `~/.config/gmail_to_notebooklm/tokens.pickle`
   - Automatic token refresh on expiration

2. **Custom credentials.json**
   - Place `credentials.json` in project root or `~/.config/gmail_to_notebooklm/`
   - Created from Google Cloud Console OAuth 2.0 credentials
   - Supports both user and service account credentials

3. **Embedded Credentials** (For distribution)
   - Pre-configured credentials built into executable
   - Simplified setup for end users
   - See `docs/BUILDING_WITH_EMBEDDED_CREDENTIALS.md` for build process

## Implementation Status

### Completed Features
- ✅ OAuth 2.0 authentication with token management
- ✅ Gmail API integration with label filtering
- ✅ MIME-based email parsing
- ✅ HTML to Markdown conversion
- ✅ YAML metadata in export files
- ✅ UTF-8 output encoding
- ✅ CLI application with 25+ options
- ✅ GUI application with dialogs and wizards
- ✅ Export history tracking
- ✅ Configuration profiles
- ✅ Index file generation
- ✅ Date-based file organization
- ✅ Windows executables and installer
- ✅ Comprehensive test suite (67 tests, 53% coverage)
- ✅ Full documentation (20+ guides)

### Key Implementation Details

- **Security**: OAuth 2.0 with secure token storage; no credentials in source code
- **HTML Processing**: Prioritizes HTML body over plain text; cleans and normalizes with BeautifulSoup
- **Error Handling**: Graceful handling of API failures, network issues, and malformed content
- **Encoding**: All output guaranteed UTF-8
- **API Calls**: Uses `users.messages.list` for queries, `users.messages.get` with `format='full'` for content
- **Progress Tracking**: Real-time callbacks for UI updates during export
- **Cancellation**: Support for stopping exports mid-process
- **Batch Operations**: Efficient batch processing with progress indication

## Out of Scope

- Email attachments (body content only)
- Direct NotebookLM upload integration (manual upload by user)
- AI summarization or content extraction
- Two-way Gmail synchronization
- Email deletion or modification
