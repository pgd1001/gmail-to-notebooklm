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

This is a Python-based tool to convert Gmail emails from a specific label into Markdown files formatted for Google NotebookLM. The tool extracts email headers (From, To, Cc, Subject, Date) and body content, converting HTML to Markdown while preserving formatting.

**Current Status:** Early development stage - only requirements documentation exists. No implementation code yet.

## Architecture

The tool follows a modular design with these key components:

1. **Authentication Module**: OAuth 2.0 flow for Gmail API access using `google-auth-oauthlib`
2. **Gmail API Integration**: Fetches emails by label using `google-api-python-client`
3. **Email Parser**: MIME parsing to extract headers and body content
4. **Markdown Converter**: HTML-to-Markdown conversion with header metadata prepended
5. **File Writer**: UTF-8 encoded output with sanitized filenames

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

**Installation:**
```bash
pip install -r requirements.txt
```

**Expected Dependencies:**
- `google-api-python-client` - Gmail API interaction
- `google-auth-oauthlib` - OAuth 2.0 authentication
- `beautifulsoup4` or `lxml` - HTML parsing
- `html2text` or `markdownify` - HTML to Markdown conversion

**Running the tool (expected CLI):**
```bash
python main.py --label "Client A" --output-dir "output"
```

**Authentication:**
Requires `credentials.json` from Google Cloud Platform in the root directory. First run will open a browser for OAuth authorization.

## Key Implementation Requirements

- **Security**: Use OAuth 2.0 for authentication; store refresh tokens securely; never store credentials directly
- **HTML Processing**: Prioritize HTML body over plain text; ignore headers within HTML content itself
- **Error Handling**: Handle API failures, network issues, and malformed email content gracefully
- **Encoding**: All output files must be UTF-8 encoded
- **API Calls**: Use `users.messages.list` for label-based queries and `users.messages.get` with `format='full'` for content

## Out of Scope

- Email attachments (body content only)
- Direct NotebookLM upload integration (manual upload by user)
- AI summarization or content extraction
- Two-way Gmail synchronization
- Email deletion or modification
