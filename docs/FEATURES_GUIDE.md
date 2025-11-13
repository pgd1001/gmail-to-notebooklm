# Features & Settings Guide

This guide covers all user-facing features and how to use them in both the CLI and GUI.

## Overview

Gmail to NotebookLM has two interfaces:
- **GUI** (Windows desktop app) - Recommended for most users
- **CLI** (Command line) - For power users and automation

Both have the same core features with slightly different workflows.

---

## Core Features

### 1. Email Label Selection

**What it does**: Choose which Gmail label to export emails from.

**Examples**:
- `Inbox` - All inbox emails
- `Client A` - Specific client label
- `Archive` - Archived emails
- `Sent Mail` - Emails you sent

**How to use**:

**GUI**:
1. Click label dropdown at top
2. Select from list
3. Or type to search

**CLI**:
```bash
g2n --label "Inbox"
g2n --label "Client A"

# List all available labels first
g2n --list-labels
```

---

### 2. Email Filtering

**Date Range Filtering**

Filter emails by date range.

**GUI**:
- "After (date)" field - Include emails from this date onward
- "Before (date)" field - Include emails before this date

**CLI**:
```bash
# After a date
g2n --label "Inbox" --after "2024-01-01"

# Before a date
g2n --label "Inbox" --before "2024-12-31"

# Date range
g2n --label "Inbox" --after "2024-01-01" --before "2024-12-31"

# Supported formats: YYYY-MM-DD or YYYY/MM/DD
```

**Sender/Recipient Filtering**

Filter by who sent or received emails.

**GUI**:
- "From" field - Emails from these addresses
- "To" field - Emails sent to these addresses
- "Exclude From" field - Exclude emails from these addresses

**CLI**:
```bash
# From a specific sender
g2n --label "Inbox" --from "boss@company.com"

# From multiple senders (comma-separated)
g2n --label "Inbox" --from "boss@company.com, colleague@company.com"

# Sent to a specific recipient
g2n --label "Inbox" --to "project@company.com"

# Exclude emails from someone
g2n --label "Inbox" --exclude-from "spam@example.com"

# Combination
g2n --label "Inbox" --from "boss@company.com" --after "2024-01-01"
```

**Advanced Query**

Use Gmail's search syntax for complex filters.

**GUI**:
- "Query" field - Gmail search syntax

**CLI**:
```bash
# Gmail search syntax examples
g2n --label "Inbox" --query "has:attachment"
g2n --label "Inbox" --query 'subject:"urgent"'
g2n --label "Inbox" --query "from:boss@company.com before:2024-12-31"

# Combine with other filters
g2n --label "Inbox" --query 'subject:"project"' --max-results 50
```

**Common Gmail Query Examples**:
- `has:attachment` - Emails with attachments
- `subject:"keyword"` - Search subject line
- `is:unread` - Unread emails
- `is:starred` - Starred emails
- `larger:10M` - Large attachments
- `filename:pdf` - PDFs specifically

---

### 3. Output Organization

**Basic Export**

Export all matching emails to a single folder.

**GUI**:
- Select "Output Directory"
- Click "Export"

**CLI**:
```bash
g2n --label "Inbox" --output-dir "./exports"

# Full path recommended
g2n --label "Inbox" --output-dir "/full/path/to/exports"
```

**Date-Based Organization**

Automatically organize exported files into subfolders by date.

**GUI**:
- Check "Organize by Date" checkbox
- Choose date format below

**CLI**:
```bash
g2n --label "Inbox" --organize-by-date

# With custom date format
g2n --label "Inbox" --organize-by-date --date-format "YYYY/MM"
```

**Output Structure**:
```
exports/
├── 2024/01/
│   ├── Email_1.md
│   ├── Email_2.md
├── 2024/02/
│   ├── Email_3.md
│   └── Email_4.md
└── 2024/03/
    └── Email_5.md
```

**Date Format Options**:
- `YYYY` - Year only (2024/)
- `YYYY/MM` - Year and month (2024/01/)
- `YYYY/MM/DD` - Full date (2024/01/15/)
- `YYYY-MM` - Year-month dash (2024-01/)
- `YYYY-MM-DD` - Full date dash (2024-01-15/)

---

### 4. Result Limiting

**Limit Number of Emails**

Useful for testing or managing export size.

**GUI**:
- "Max Results" field - Enter number (0 = all)

**CLI**:
```bash
# Export only 10 emails
g2n --label "Inbox" --max-results 10

# Export only 100 emails
g2n --label "Inbox" --max-results 100

# Export all (default)
g2n --label "Inbox" --max-results 0
```

---

### 5. Index File Generation

**What it does**: Automatically create an `INDEX.md` file with a table of contents of all exported emails.

**Example INDEX.md**:
```markdown
# Email Index

Generated: 2024-11-13 14:23:45
Total emails: 45

## Emails

| # | Subject | From | Date |
|---|---------|------|------|
| 1 | Project Update | boss@company.com | 2024-11-13 |
| 2 | Meeting Notes | colleague@company.com | 2024-11-12 |
...
```

**How to use**:

**GUI**:
- Check "Create Index" checkbox

**CLI**:
```bash
g2n --label "Inbox" --create-index
```

---

### 6. Dry Run Mode

**What it does**: Preview what would be exported WITHOUT creating files.

Useful for testing filters before actually exporting.

**GUI**:
- Check "Dry Run" checkbox
- Click "Export"
- See results in progress dialog

**CLI**:
```bash
# Show what would be exported
g2n --label "Inbox" --dry-run

# With verbose to see details
g2n --label "Inbox" --dry-run --verbose
```

**Output**:
```
Dry-run mode enabled - no files will be created

Step 1/5: Authenticating...
Step 2/5: Connecting to Gmail...
Step 3/5: Fetching emails... Found 45 emails
Step 4/5: Parsing emails... 45 emails parsed
Step 5/5: Converting to Markdown... (skipped in dry-run)

Would create 45 files in: /path/to/output
```

---

## Advanced Features

### 1. Profiles (Save & Reuse Settings)

**What it does**: Save your export settings (label, filters, options) as a named profile for quick re-use.

**Example**: Save "Monthly Client Reports" profile with:
- Label: "Client A"
- Date: Last month
- Organization: By date
- Index: Enabled

Then next month, just load the profile and click Export.

**GUI - Creating a Profile**:

1. Configure all your settings:
   - Select label
   - Set filters
   - Choose output directory
   - Set options (organize by date, create index, etc.)

2. Click "Profiles" button

3. Click "Save Profile"

4. Enter profile name: "Monthly Client Reports"

5. Click "Save"

**GUI - Using a Profile**:

1. Click "Profiles" button

2. Select profile from list: "Monthly Client Reports"

3. Click "Load"

4. Settings automatically populate

5. Click "Export" to run

**CLI**:
```bash
# Profiles are saved in GUI only
# CLI uses configuration files instead
# See Configuration section below
```

**Built-in Profiles**:
The app comes with example profiles you can modify:
- "Inbox Backup" - Monthly inbox export
- "Sent Mail Archive" - Archive sent mail
- "Client Archive" - Template for client exports

---

### 2. Export History

**What it does**: Keep a record of all your exports with statistics.

**Tracks**:
- When you exported
- Which label and filters used
- Number of files created
- Success or failure
- Time taken
- Output location

**GUI - Viewing History**:

1. Click "History" button

2. See list of past exports

3. Click on an export to see details:
   - Date and time
   - Label and filters used
   - Files created
   - Status (success/failed)
   - Duration

**GUI - Repeating an Export**:

1. Click "History" button

2. Find the export you want to repeat

3. Click "Re-export" button

4. Click "Export" to run with same settings

**GUI - Statistics Dashboard**:

History dialog shows overview stats:
- Total exports
- Success rate (X%)
- Average duration
- Most frequently exported label
- Last export time

**Useful for**:
- Remembering what you've already exported
- Checking if export succeeded
- Repeating common exports
- Tracking export history over time

---

### 3. Settings & Configuration

**What it does**: Customize application behavior and defaults.

**GUI - Settings Dialog**:

Click "Settings" button to open settings with tabs:

**Credentials Tab**:
- View current OAuth status
- Re-authenticate with Gmail
- Change credentials file location
- Manage tokens

**Defaults Tab**:
- Default output directory
- Default label to show on startup
- Default date format for --organize-by-date
- Default max results (0 = all)

**Advanced Tab**:
- Text wrapping width for Markdown
- Enable/disable verbose output
- Keep or overwrite existing files
- History database location

**CLI - Configuration File**:

Create `~/.gmail-to-notebooklm/config.yaml`:

```yaml
# Default label to use
label: "Inbox"

# Default output directory
output_dir: "/home/user/gmail-exports"

# Default date format for organization
date_format: "YYYY/MM"

# Max results to fetch
max_results: 0  # 0 = all

# Automatically organize by date
organize_by_date: true

# Create index file
create_index: true

# Text wrapping width (0 = auto)
text_width: 80

# Keep existing files (don't overwrite)
no_overwrite: false

# Credentials location
credentials: "~/.gmail-to-notebooklm/credentials.json"
```

**CLI - Configuration Examples**:

```bash
# Use config file
g2n --config ~/.gmail-to-notebooklm/config.yaml

# Override specific settings
g2n --config config.yaml --max-results 50  # Override max-results

# Custom credentials file
g2n --label "Inbox" --credentials "/path/to/credentials.json"

# Custom token file
g2n --label "Inbox" --token "/path/to/tokens.pickle"
```

---

## Output & Formats

### File Format

Each exported email becomes a Markdown file with this structure:

```markdown
---
From: John Doe <john@example.com>
To: Jane Smith <jane@company.com>
Cc: Manager <manager@company.com>
Date: November 13, 2024 at 2:30 PM
Subject: Project Update - Q4 Review
---

# Email Body

This is the email content converted to Markdown.

## Headers

### Subheaders

- Bullet points
- Work great
- In Markdown

**Bold text**, *italic*, `code`

[Links work too](https://example.com)

---

Dividers are preserved.

```

### Filename Format

Files are named using the email subject + a short ID:

```
Project_Update_Q4_Review_abc123.md
Meeting_Notes_def456.md
Quick_Question_ghi789.md
```

**If subject is very long**:
Files are truncated to ~200 characters:
```
Very_Long_Email_Subject_That_Goes_On_And_On_jkl012.md
```

### Character Handling

Special characters in filenames are cleaned:
```
"Email with / slashes" → Email_with_slashes.md
"Email: with colon" → Email_with_colon.md
"Email\with\backslash" → Email_with_backslash.md
```

---

## Output Modes

### Normal Output

Shows progress with nice formatting.

**CLI**:
```bash
g2n --label "Inbox"

# Output:
# ┌─ Authenticating with Gmail... ✓
# ├─ Fetching emails... Found 45 emails
# ├─ Parsing emails... 45 emails parsed
# ├─ Converting to Markdown... 45 emails converted
# └─ Writing files... Complete!
#
# Exported 45 emails to: /path/to/output
```

### Verbose Output

Shows detailed information for debugging.

**CLI**:
```bash
g2n --label "Inbox" --verbose

# Shows step details, file paths, processing times, etc.
```

### Quiet Output

Minimal output, useful for automation.

**CLI**:
```bash
g2n --label "Inbox" --quiet

# Only shows: Success or error messages only
# Exit code indicates result
```

### JSON Output

Machine-readable format for scripts.

**CLI**:
```bash
g2n --label "Inbox" --json-output

# Output (JSON):
# {
#   "status": "success",
#   "emails_exported": 45,
#   "files_created": 45,
#   "output_directory": "/path/to/output",
#   "duration_seconds": 23.5
# }
```

---

## File Management

### Overwrite Handling

**Default**: Don't overwrite existing files

```bash
# First run - creates files
g2n --label "Inbox" --max-results 5

# Second run - skips existing files
g2n --label "Inbox" --max-results 5
# Result: No files overwritten, no change

# Force overwrite
g2n --label "Inbox" --max-results 5 --overwrite
# Result: All files updated
```

**In GUI**: Checkbox "Overwrite Existing Files" in Settings

### File Structure

Files are organized in the output directory:

```
output-directory/
├── Email_1_abc.md
├── Email_2_def.md
├── Email_3_ghi.md
│
└── If --organize-by-date:
    ├── 2024/01/
    │   ├── Email_1_abc.md
    │   └── Email_2_def.md
    └── 2024/02/
        └── Email_3_ghi.md
```

### Index File

If `--create-index` is used, generates `INDEX.md`:

```markdown
# Email Index

Generated: 2024-11-13 14:30:00
Label: Inbox
Total: 45 emails

[Files are listed with date and sender]
```

---

## Tips & Tricks

### Pro Tips

**Tip 1: Use Profiles for Recurring Exports**
```
Save "Monthly Report" profile with:
- Label: "Reports"
- After: "this month"
- Organize by date: Yes
- Index: Yes

Then monthly, just load and export!
```

**Tip 2: Test with Dry-Run First**
```bash
# Try your filter first
g2n --label "Inbox" --query 'subject:"urgent"' --dry-run

# Once you see results, run for real
g2n --label "Inbox" --query 'subject:"urgent"'
```

**Tip 3: Use History to Find Past Settings**
```
Can't remember your filter settings?
Check History → find past export → click "Re-export"
```

**Tip 4: Create Index for Easy Navigation**
```bash
# Create index so you can navigate files
g2n --label "Inbox" --create-index
# Opens INDEX.md to jump to any email
```

**Tip 5: Archive Systematically**
```bash
# Export by date range in batches
g2n --label "Inbox" --after "2024-01-01" --before "2024-03-31"
g2n --label "Inbox" --after "2024-04-01" --before "2024-06-30"
# More manageable than exporting everything at once
```

### Automation

**Run Daily Exports via Task Scheduler (Windows)**:
```batch
@echo off
REM Daily export of new emails
cd C:\Users\YourName\Documents
g2n --label "Inbox" --after "yesterday" --organize-by-date
```

**Run Scheduled Exports via Cron (Mac/Linux)**:
```bash
# Add to crontab -e
0 9 * * * /usr/local/bin/g2n --label "Inbox" --after "1 day ago"
```

---

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| Easy to use | ✓ | - |
| Profiles | ✓ | YAML config |
| History | ✓ | - |
| Visual progress | ✓ | - |
| Automation | - | ✓ |
| Dry-run | ✓ | ✓ |
| Advanced queries | ✓ | ✓ |
| Scripting | - | ✓ |

---

## Need Help?

- **Getting started**: [GETTING_HELP.md](./GETTING_HELP.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **Configuration**: [CONFIGURATION.md](./CONFIGURATION.md)
- **Examples**: [USAGE.md](./USAGE.md)

---

**Last Updated**: November 2025
**Version**: 1.0
