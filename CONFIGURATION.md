# Configuration Guide

Detailed configuration options for the Gmail to NotebookLM converter.

## Command-Line Arguments

### Search Arguments (v0.2.0+)

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--label` | `-l` | Gmail label to export (optional if using --query) | `--label "Client A"` |
| `--query` | `-q` | Gmail search query | `--query "is:unread"` |

### Filtering Arguments (v0.2.0+)

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--after` | Filter emails after date (YYYY-MM-DD) | None | `--after "2024-01-01"` |
| `--before` | Filter emails before date (YYYY-MM-DD) | None | `--before "2024-12-31"` |
| `--from` | Filter by sender(s) (comma-separated) | None | `--from "john@example.com"` |
| `--to` | Filter by recipient(s) (comma-separated) | None | `--to "client@example.com"` |
| `--exclude-from` | Exclude sender(s) (comma-separated) | None | `--exclude-from "spam@example.com"` |

### Organization Arguments (v0.2.0+)

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--organize-by-date` | Organize files into date subdirectories | `False` | `--organize-by-date` |
| `--date-format` | Date format for subdirectories | `YYYY/MM` | `--date-format "YYYY-MM"` |
| `--create-index` | Generate INDEX.md file | `False` | `--create-index` |

### General Arguments

| Argument | Short | Description | Default | Example |
|----------|-------|-------------|---------|---------|
| `--output-dir` | `-o` | Output directory path | `./output` | `--output-dir "./exports"` |
| `--max-results` | `-m` | Maximum emails to process | Unlimited | `--max-results 100` |
| `--verbose` | `-v` | Enable verbose logging | `False` | `--verbose` |
| `--overwrite` | | Overwrite existing files | `False` | `--overwrite` |
| `--config` | | Custom config file path | None | `--config "./my-config.yaml"` |
| `--help` | `-h` | Show help message | - | `--help` |
| `--version` | | Show version | - | `--version` |

## Environment Variables

Set these environment variables to configure default behavior:

### GMAIL_TO_NBL_OUTPUT_DIR

Default output directory for exported Markdown files.

```bash
# Unix/macOS
export GMAIL_TO_NBL_OUTPUT_DIR="/home/user/exports"

# Windows Command Prompt
set GMAIL_TO_NBL_OUTPUT_DIR=C:\Users\User\exports

# Windows PowerShell
$env:GMAIL_TO_NBL_OUTPUT_DIR="C:\Users\User\exports"
```

**Priority**: Command-line `--output-dir` overrides this variable.

### GMAIL_TO_NBL_CREDENTIALS_PATH

Custom path to `credentials.json` file.

```bash
export GMAIL_TO_NBL_CREDENTIALS_PATH="/secure/location/credentials.json"
```

**Default**: `./credentials.json` (project root)

### GMAIL_TO_NBL_TOKEN_PATH

Custom path for storing `token.json` (authentication token).

```bash
export GMAIL_TO_NBL_TOKEN_PATH="/secure/location/token.json"
```

**Default**: `./token.json` (project root)

### GMAIL_TO_NBL_LOG_LEVEL

Logging verbosity level.

```bash
export GMAIL_TO_NBL_LOG_LEVEL="DEBUG"
```

**Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
**Default**: `INFO`

### GMAIL_TO_NBL_MAX_RESULTS

Default maximum number of emails to process.

```bash
export GMAIL_TO_NBL_MAX_RESULTS="500"
```

**Default**: Unlimited (processes all emails in label)

## Configuration File (v0.2.0+)

Create a `.gmail-to-notebooklm.yaml` file for persistent configuration. The tool searches for this file in:
1. Current directory (`./.gmail-to-notebooklm.yaml`)
2. Home directory (`~/.gmail-to-notebooklm.yaml`)
3. Custom path via `--config` flag

### Example Configuration File

**.gmail-to-notebooklm.yaml**:
```yaml
# Output configuration
output_dir: "./exports"
overwrite: false

# Search configuration
max_results: 1000

# Organization configuration (v0.2.0+)
organize_by_date: true
date_format: "YYYY/MM"  # Options: YYYY/MM, YYYY-MM, YYYY/MM/DD, YYYY-MM-DD
create_index: true

# OAuth configuration
credentials_path: "credentials.json"
token_path: "token.json"

# Logging
verbose: false

# Output file naming
filename_template: "{subject}_{id}"
max_filename_length: 200

# Markdown conversion options
markdown:
  # Preserve links
  preserve_links: true

  # Include email headers in output
  include_headers: true

  # Wrap text at column
  wrap_width: 0  # 0 = no wrapping

  # Convert HTML entities
  decode_entities: true

# Email filtering
filters:
  # Only process emails newer than this date (YYYY-MM-DD)
  date_after: null

  # Only process emails older than this date
  date_before: null

  # Exclude emails from specific senders
  exclude_senders: []

  # Include only emails from specific senders
  include_senders: []

# Performance options
performance:
  # Number of concurrent API requests
  max_workers: 5

  # Retry failed requests
  max_retries: 3

  # Delay between requests (seconds)
  request_delay: 0.1

# Output options
output:
  # Create subdirectories by year/month
  organize_by_date: false

  # Overwrite existing files
  overwrite: false

  # Create index file with all emails
  create_index: false
```

### Configuration File Priority

Configuration is loaded in this order (later overrides earlier):

1. Default values (hardcoded)
2. System config: `/etc/gmail-to-notebooklm/config.yaml` (Linux/macOS)
3. User config: `~/.gmail-to-notebooklm.yaml`
4. Project config: `./.gmail-to-notebooklm.yaml`
5. Environment variables
6. Command-line arguments (highest priority)

## Output Configuration

### Filename Template

Customize output filename format:

```yaml
# In .gmail-to-notebooklm.yaml
filename_template: "{date}_{subject}_{id}"
```

**Available placeholders**:
- `{subject}` - Email subject (sanitized)
- `{id}` - Email ID (shortened)
- `{date}` - Email date (YYYY-MM-DD format)
- `{from}` - Sender email (sanitized)
- `{to}` - Recipient email (sanitized)

**Example outputs**:
- `2024-01-15_Project_Update_18a3f2b1.md`
- `john.doe_Meeting_Notes_c7d9e4a2.md`

### Directory Organization

Organize output by date:

```yaml
output:
  organize_by_date: true
  date_format: "%Y/%m"  # Creates: 2024/01/email.md
```

**Date format options**:
- `%Y/%m` - Year/Month (2024/01)
- `%Y/%m/%d` - Year/Month/Day (2024/01/15)
- `%Y-Q{quarter}` - Year-Quarter (2024-Q1)

## Markdown Conversion Options

### HTML to Markdown Settings

```yaml
markdown:
  # Body width for wrapping (0 = no wrap)
  wrap_width: 0

  # Convert <strong> to **bold**
  strong_mark: "**"

  # Convert <em> to *italic*
  emphasis_mark: "*"

  # Convert <ul> bullets
  ul_style: "-"  # Options: "-", "*", "+"

  # Skip images
  skip_images: false

  # Include image alt text
  include_image_alt: true

  # Convert links to inline format
  inline_links: true

  # Preserve HTML for complex elements
  preserve_html: false
```

### Header Format

Customize the YAML front matter:

```yaml
headers:
  # Include headers in output
  enabled: true

  # Header fields to include
  fields:
    - from
    - to
    - cc
    - subject
    - date
    - message_id

  # Date format
  date_format: "%a, %d %b %Y %H:%M:%S %z"

  # Include thread information
  include_thread_id: false
```

## Filtering Options

### Date-Based Filtering

Process only emails within a date range:

```bash
# Via command line (future feature)
gmail-to-notebooklm --label "Archive" \
  --date-after "2024-01-01" \
  --date-before "2024-12-31"
```

```yaml
# Via config file
filters:
  date_after: "2024-01-01"
  date_before: "2024-12-31"
```

### Sender Filtering

Include or exclude specific senders:

```yaml
filters:
  # Only process emails from these senders
  include_senders:
    - "important@example.com"
    - "client@company.com"

  # Exclude emails from these senders
  exclude_senders:
    - "noreply@newsletter.com"
    - "spam@unwanted.com"
```

### Subject Filtering

Filter by subject patterns:

```yaml
filters:
  # Include only subjects matching regex
  subject_include: "^\\[IMPORTANT\\]"

  # Exclude subjects matching regex
  subject_exclude: "^Re: Automated"
```

## Performance Tuning

### API Rate Limiting

Adjust to stay within Gmail API quotas:

```yaml
performance:
  # Concurrent requests (1-10)
  max_workers: 5

  # Delay between requests (seconds)
  request_delay: 0.1

  # Batch size for list operations
  batch_size: 100

  # Maximum retries for failed requests
  max_retries: 3

  # Retry delay (seconds)
  retry_delay: 1.0
```

**Gmail API Limits**:
- 1 billion quota units per day
- `users.messages.list`: 5 units per call
- `users.messages.get`: 5 units per call

### Memory Optimization

For processing large labels:

```yaml
performance:
  # Process in chunks
  chunk_size: 100

  # Clear cache after each chunk
  clear_cache: true

  # Limit in-memory emails
  max_memory_emails: 50
```

## OAuth Configuration

### Custom Scopes

By default, the tool uses `gmail.readonly`. For custom implementations:

```yaml
oauth:
  # OAuth scopes (comma-separated)
  scopes:
    - "https://www.googleapis.com/auth/gmail.readonly"

  # Redirect URI
  redirect_uri: "http://localhost:8080/"

  # Token storage format
  token_format: "json"  # Options: json, pickle
```

### Credentials Location

```yaml
oauth:
  # Path to credentials.json
  credentials_path: "./credentials.json"

  # Path to token storage
  token_path: "./token.json"

  # Auto-refresh tokens
  auto_refresh: true
```

## Logging Configuration

### Log Levels

```yaml
logging:
  # Main log level
  level: "INFO"

  # Log to file
  file: "./logs/gmail-to-notebooklm.log"

  # Log format
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

  # Rotate log files
  rotate: true
  max_bytes: 10485760  # 10 MB
  backup_count: 5
```

### Component-Specific Logging

```yaml
logging:
  levels:
    gmail_to_notebooklm.auth: "DEBUG"
    gmail_to_notebooklm.gmail_client: "INFO"
    gmail_to_notebooklm.converter: "WARNING"
```

## Example Configurations

### Minimal Configuration

```yaml
output_dir: "./exports"
max_results: 1000
```

### Power User Configuration

```yaml
output_dir: "./exports"
max_results: 5000
log_level: "DEBUG"

markdown:
  wrap_width: 80
  preserve_links: true
  inline_links: true

filters:
  date_after: "2023-01-01"
  exclude_senders:
    - "noreply@"

performance:
  max_workers: 8
  request_delay: 0.05

output:
  organize_by_date: true
  date_format: "%Y/%m"
  create_index: true
```

### Enterprise Configuration

```yaml
output_dir: "/data/gmail-exports"
credentials_path: "/secure/credentials.json"
token_path: "/secure/token.json"

logging:
  level: "INFO"
  file: "/var/log/gmail-to-notebooklm.log"
  rotate: true

performance:
  max_workers: 10
  batch_size: 200
  request_delay: 0.1

output:
  organize_by_date: true
  overwrite: false
  create_index: true

filters:
  exclude_senders:
    - "automated@"
    - "noreply@"
```

## Validation

Validate your configuration file:

```bash
# Check configuration syntax
gmail-to-notebooklm --validate-config

# Show current configuration
gmail-to-notebooklm --show-config

# Use specific config file
gmail-to-notebooklm --config ./my-config.yaml --label "Test"
```

## Next Steps

- See [USAGE.md](USAGE.md) for usage examples
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for customization options
- Check [INSTALLATION.md](INSTALLATION.md) for setup instructions
