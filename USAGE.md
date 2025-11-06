# Usage Guide

Comprehensive guide to using the Gmail to NotebookLM converter.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Command-Line Options](#command-line-options)
- [Examples](#examples)
- [Output Format](#output-format)
- [Workflow Guide](#workflow-guide)
- [Advanced Usage](#advanced-usage)
- [Tips & Best Practices](#tips--best-practices)

## Basic Usage

The simplest way to use the tool:

```bash
gmail-to-notebooklm --label "Your Label Name" --output-dir "./output"
```

This will:
1. Authenticate with Gmail (first run only)
2. Find all emails under "Your Label Name"
3. Convert each email to a Markdown file
4. Save files to the `./output` directory

## Command-Line Options

### Search Options

- `--label` or `-l`: The Gmail label to export (case-sensitive, optional if using --query)
  ```bash
  gmail-to-notebooklm --label "Client A"
  ```

- `--query` or `-q`: Gmail search query (optional, can be combined with --label)
  ```bash
  gmail-to-notebooklm --query "is:unread after:2024/01/01"
  ```

### Filtering Options

- `--after`: Filter emails after this date (YYYY-MM-DD or YYYY/MM/DD)
  ```bash
  gmail-to-notebooklm --label "Archive" --after "2024-01-01"
  ```

- `--before`: Filter emails before this date (YYYY-MM-DD or YYYY/MM/DD)
  ```bash
  gmail-to-notebooklm --label "Archive" --before "2024-12-31"
  ```

- `--from`: Filter emails from specific sender(s) (comma-separated)
  ```bash
  gmail-to-notebooklm --label "Work" --from "boss@company.com,colleague@company.com"
  ```

- `--to`: Filter emails to specific recipient(s) (comma-separated)
  ```bash
  gmail-to-notebooklm --label "Sent" --to "client@example.com"
  ```

- `--exclude-from`: Exclude emails from specific sender(s) (comma-separated)
  ```bash
  gmail-to-notebooklm --label "Inbox" --exclude-from "spam@example.com,noreply@example.com"
  ```

### Organization Options

- `--organize-by-date`: Organize output files into date-based subdirectories
  ```bash
  gmail-to-notebooklm --label "Archive" --organize-by-date
  ```

- `--date-format`: Date format for subdirectories (YYYY/MM, YYYY-MM, YYYY/MM/DD, YYYY-MM-DD)
  ```bash
  gmail-to-notebooklm --label "Archive" --organize-by-date --date-format "YYYY-MM"
  ```

- `--create-index`: Generate INDEX.md file with table of contents
  ```bash
  gmail-to-notebooklm --label "Archive" --create-index
  ```

### General Options

- `--output-dir` or `-o`: Output directory for Markdown files (default: `./output`)
  ```bash
  gmail-to-notebooklm --label "Work" --output-dir "./exports/work"
  ```

- `--help` or `-h`: Show help message
  ```bash
  gmail-to-notebooklm --help
  ```

- `--version` or `-v`: Show version information
  ```bash
  gmail-to-notebooklm --version
  ```

- `--max-results` or `-m`: Maximum number of emails to process (default: unlimited)
  ```bash
  gmail-to-notebooklm --label "Archive" --max-results 100
  ```

- `--verbose`: Enable verbose output for debugging
  ```bash
  gmail-to-notebooklm --label "Test" --verbose
  ```

## Examples

### Example 1: Export Client Emails

```bash
gmail-to-notebooklm --label "Client ABC" --output-dir "./clients/abc"
```

**Result**: All emails labeled "Client ABC" are saved as Markdown files in `./clients/abc/`

### Example 2: Export Limited Number of Emails

```bash
gmail-to-notebooklm --label "Newsletter" --output-dir "./newsletters" --max-results 50
```

**Result**: Only the 50 most recent emails from "Newsletter" are exported

### Example 3: Export with Verbose Logging

```bash
gmail-to-notebooklm --label "Project X" --output-dir "./projects/x" --verbose
```

**Result**: Detailed progress information is displayed during processing

### Example 4: First-Time Authentication

```bash
gmail-to-notebooklm --label "Test"
```

On first run:
1. Browser opens automatically
2. Sign in to Google
3. Grant permissions

### Example 5: Using Gmail Query Syntax (v0.2.0+)

```bash
gmail-to-notebooklm --query "is:unread from:john@example.com"
```

**Result**: Exports all unread emails from john@example.com

### Example 6: Filter by Date Range (v0.2.0+)

```bash
gmail-to-notebooklm --label "Archive" --after "2024-01-01" --before "2024-03-31"
```

**Result**: Exports emails from Q1 2024 only

### Example 7: Filter by Sender (v0.2.0+)

```bash
gmail-to-notebooklm --label "Work" --from "boss@company.com" --output-dir "./boss-emails"
```

**Result**: Exports only emails from your boss

### Example 8: Exclude Specific Senders (v0.2.0+)

```bash
gmail-to-notebooklm --label "Inbox" --exclude-from "noreply@,newsletter@" --max-results 100
```

**Result**: Exports 100 emails, excluding automated messages

### Example 9: Organize by Date with Index (v0.2.0+)

```bash
gmail-to-notebooklm --label "Archive" --organize-by-date --create-index --output-dir "./organized"
```

**Result**:
- Emails organized into `./organized/2024/01/`, `./organized/2024/02/`, etc.
- INDEX.md file created with sortable table of all emails

### Example 10: Complete Advanced Export (v0.2.0+)

```bash
gmail-to-notebooklm \
  --label "Client ABC" \
  --after "2024-01-01" \
  --from "client@abc.com,team@abc.com" \
  --organize-by-date \
  --date-format "YYYY-MM" \
  --create-index \
  --output-dir "./clients/abc/2024"
```

**Result**: Comprehensive export with:
- Date filtering (2024 only)
- Sender filtering (specific contacts only)
- Date-based organization (YYYY-MM format)
- Automatic index generation

## Output Format

### File Naming

Each email is saved with a descriptive filename:

```
Format: [Sanitized_Subject]_[Email_ID].md

Examples:
- Project_Update_Q4_18a3f2b1.md
- Meeting_Notes_Jan_15_c7d9e4a2.md
- Quarterly_Review_9f1b2c3d.md
```

**Sanitization Rules**:
- Special characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) are removed
- Spaces are replaced with underscores
- Maximum filename length: 200 characters
- Email ID is truncated to 8 characters

### File Content Structure

Each Markdown file contains:

```markdown
---
From: Sender Name <sender@example.com>
To: Recipient Name <recipient@example.com>
Cc: CC Name <cc@example.com>
Date: Mon, 15 Jan 2024 10:30:00 -0800
Subject: Email Subject Line
---

Email body content converted to Markdown.

**Bold text** and *italic text* are preserved.

- Lists are maintained
- Links work: [Example](https://example.com)

> Quoted text is formatted as blockquotes

Tables and other formatting are converted appropriately.
```

### Directory Structure

```
output/
├── Project_Update_Q4_18a3f2b1.md
├── Meeting_Notes_Jan_15_c7d9e4a2.md
├── Quarterly_Review_9f1b2c3d.md
└── ...
```

## Workflow Guide

### Step 1: Organize Emails in Gmail

Before exporting, organize emails with labels:

1. Open Gmail
2. Select emails you want to export
3. Click the label icon
4. Create or select a label (e.g., "Client A", "Project X")

### Step 2: Run the Export

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run export
gmail-to-notebooklm --label "Your Label" --output-dir "./output"
```

### Step 3: Review Output

```bash
# Check the output directory
ls ./output

# Preview a file
cat ./output/First_Email_File.md
```

### Step 4: Upload to NotebookLM

1. Go to [NotebookLM](https://notebooklm.google.com/)
2. Create a new notebook or open existing one
3. Click "Add Sources"
4. Select "Upload"
5. Choose the Markdown files from your output directory
6. NotebookLM will process them with full context from headers

## Advanced Usage

### Processing Multiple Labels

To export multiple labels, run the command multiple times:

```bash
# Export each label to separate directories
gmail-to-notebooklm --label "Client A" --output-dir "./exports/client_a"
gmail-to-notebooklm --label "Client B" --output-dir "./exports/client_b"
gmail-to-notebooklm --label "Internal" --output-dir "./exports/internal"
```

### Batch Processing Script

Create a shell script for regular exports:

**export_all.sh** (macOS/Linux):
```bash
#!/bin/bash
source .venv/bin/activate

gmail-to-notebooklm --label "Client A" --output-dir "./exports/client_a"
gmail-to-notebooklm --label "Client B" --output-dir "./exports/client_b"
gmail-to-notebooklm --label "Archive" --output-dir "./exports/archive" --max-results 100

echo "All exports completed!"
```

**export_all.bat** (Windows):
```batch
@echo off
call .venv\Scripts\activate

gmail-to-notebooklm --label "Client A" --output-dir ".\exports\client_a"
gmail-to-notebooklm --label "Client B" --output-dir ".\exports\client_b"
gmail-to-notebooklm --label "Archive" --output-dir ".\exports\archive" --max-results 100

echo All exports completed!
```

Make executable and run:
```bash
chmod +x export_all.sh
./export_all.sh
```

### Environment Variables

Set environment variables for default behavior:

```bash
# Set default output directory
export GMAIL_TO_NBL_OUTPUT_DIR="./my_exports"

# Run without specifying output dir
gmail-to-notebooklm --label "Test"
# Output goes to ./my_exports
```

## Tips & Best Practices

### Email Organization

- **Use descriptive labels**: "Client_ABC_2024" is better than "ABC"
- **Avoid nested labels**: The tool works with top-level labels
- **Keep labels specific**: Smaller, focused labels are easier to manage

### Output Management

- **Separate directories per label**: Keep exports organized
- **Date-stamped folders**: Use `./exports/2024-01-15/client_a` for versioning
- **Regular cleanup**: Remove old exports you no longer need

### Performance Optimization

- **Limit batch size**: For large labels, use `--max-results` to process in chunks
- **Run during off-hours**: Gmail API has rate limits
- **Avoid re-exporting**: Keep track of what you've already exported

### NotebookLM Integration

- **Consistent naming**: Use clear, descriptive filenames
- **Context-rich headers**: The From/To/Date headers help NotebookLM understand relationships
- **Logical grouping**: Upload related emails together for better context

### Security Best Practices

- **Keep credentials secure**: Never share `credentials.json` or `token.json`
- **Use read-only scope**: The tool only needs `gmail.readonly`
- **Regular audits**: Periodically review OAuth permissions in Google Account settings
- **Separate accounts**: Consider using a dedicated Google account for automation

### Troubleshooting Tips

- **Check label names**: Gmail labels are case-sensitive
- **Verify permissions**: Ensure your account is a test user
- **Monitor API quotas**: Google has daily limits on API calls
- **Test with small labels**: Start with a small label to verify setup

## Common Workflows

### Workflow 1: Weekly Client Updates

```bash
# Every Monday, export last week's client emails
gmail-to-notebooklm --label "Client Updates" \
  --output-dir "./exports/$(date +%Y-%m-%d)"
```

### Workflow 2: Project Documentation

```bash
# Export all project-related emails for documentation
gmail-to-notebooklm --label "Project Alpha" \
  --output-dir "./projects/alpha/emails"

# Upload to NotebookLM
# Now ask NotebookLM: "Summarize all project decisions made"
```

### Workflow 3: Research Archive

```bash
# Export research emails with context
gmail-to-notebooklm --label "Research Papers" \
  --output-dir "./research/papers" \
  --max-results 500
```

## Error Handling

### "Label not found"

```bash
# List available labels first (feature to be implemented)
gmail-to-notebooklm --list-labels

# Then use exact label name
gmail-to-notebooklm --label "The/Exact/Label/Name"
```

### "Rate limit exceeded"

Wait a few minutes and try again. Gmail API has quotas:
- 1 billion quota units per day
- Most operations cost 5-10 units

### "Token expired"

Delete `token.json` and re-authenticate:
```bash
rm token.json
gmail-to-notebooklm --label "Test"
# Browser will open for re-authentication
```

## Next Steps

- Review [CONFIGURATION.md](CONFIGURATION.md) for advanced configuration
- See [DEVELOPMENT.md](DEVELOPMENT.md) to contribute features
- Check [TROUBLESHOOTING.md](INSTALLATION.md#troubleshooting) for common issues

---

For questions or issues, see the [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues) page.
