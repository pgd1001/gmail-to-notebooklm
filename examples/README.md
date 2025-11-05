# Examples

This directory contains example files and usage scenarios for the Gmail to NotebookLM converter.

## Files

### sample_credentials.json

Example structure of the `credentials.json` file you'll download from Google Cloud Console.

**Important**: This is just a structure example with placeholder values. You must download your actual credentials from Google Cloud Console.

See [OAUTH_SETUP.md](../OAUTH_SETUP.md) for instructions.

### sample_config.yaml

Example configuration file showing all available options.

**Usage**:
```bash
# Copy to project root and customize
cp examples/sample_config.yaml .gmail-to-notebooklm.yaml

# Edit with your preferences
# Then run the tool - it will use your config
gmail-to-notebooklm --label "Your Label"
```

See [CONFIGURATION.md](../CONFIGURATION.md) for detailed option descriptions.

## Usage Examples

### Example 1: Basic Export

Export all emails from a single label:

```bash
gmail-to-notebooklm --label "Client A" --output-dir "./client_a"
```

### Example 2: Limited Export

Export only the 100 most recent emails:

```bash
gmail-to-notebooklm --label "Archive" --max-results 100 --output-dir "./archive"
```

### Example 3: Multiple Labels (Bash Script)

Create a script to export multiple labels:

```bash
#!/bin/bash
# export_all.sh

labels=("Client A" "Client B" "Project X")

for label in "${labels[@]}"; do
    echo "Exporting label: $label"
    output_dir="./exports/${label// /_}"
    gmail-to-notebooklm --label "$label" --output-dir "$output_dir"
done

echo "All exports completed!"
```

### Example 4: With Verbose Output

Enable verbose logging to see detailed progress:

```bash
gmail-to-notebooklm --label "Test" --output-dir "./test" --verbose
```

### Example 5: Using Environment Variables

Set defaults with environment variables:

```bash
export GMAIL_TO_NBL_OUTPUT_DIR="./my_exports"
export GMAIL_TO_NBL_MAX_RESULTS="500"

# Now you can omit these options
gmail-to-notebooklm --label "Work Emails"
```

## Sample Output

After running the tool, you'll get Markdown files like this:

**example_email.md**:
```markdown
---
From: John Doe <john@example.com>
To: Jane Smith <jane@example.com>
Date: Mon, 15 Jan 2024 10:30:00 -0800
Subject: Project Update
---

Hi Jane,

Here's the latest update on the project:

- Phase 1 is complete
- Phase 2 is in progress
- Expected completion: End of Q1

**Key milestones**:
1. Requirements gathering ✓
2. Design phase ✓
3. Implementation (in progress)

Let me know if you have any questions.

Best regards,
John
```

## NotebookLM Integration

Once you have the Markdown files:

1. Go to [NotebookLM](https://notebooklm.google.com/)
2. Create a new notebook or open existing
3. Click "Add Sources" → "Upload"
4. Select your Markdown files
5. NotebookLM will index them with full context

**Example queries for NotebookLM**:
- "Summarize all decisions made with Client A"
- "Create a timeline of the project milestones"
- "What are the key action items from these emails?"
- "List all people mentioned across these communications"

## Directory Structure Examples

### Simple structure:
```
exports/
├── Email_1_abc123.md
├── Email_2_def456.md
└── Email_3_ghi789.md
```

### Organized by label:
```
exports/
├── client_a/
│   ├── Email_1_abc123.md
│   └── Email_2_def456.md
├── client_b/
│   ├── Email_3_ghi789.md
│   └── Email_4_jkl012.md
└── internal/
    └── Email_5_mno345.md
```

### Organized by date (with config):
```
exports/
├── 2024/
│   ├── 01/
│   │   ├── Email_1_abc123.md
│   │   └── Email_2_def456.md
│   └── 02/
│       └── Email_3_ghi789.md
```

## Testing

### Test with a small label first:

```bash
# 1. Create a test label in Gmail with 2-3 emails
# 2. Run the export
gmail-to-notebooklm --label "Test Label" --output-dir "./test"

# 3. Verify the output
ls -la ./test
cat ./test/*.md

# 4. Upload to NotebookLM to verify formatting
```

## Troubleshooting Examples

### Problem: "Label not found"

```bash
# Gmail labels are case-sensitive
# Wrong:
gmail-to-notebooklm --label "client a"

# Correct:
gmail-to-notebooklm --label "Client A"

# Check exact label name in Gmail interface
```

### Problem: Rate limiting

```bash
# Process in smaller batches
gmail-to-notebooklm --label "Large Archive" --max-results 100

# Add delay between runs if needed
gmail-to-notebooklm --label "Archive Part 1" --max-results 100
sleep 60
gmail-to-notebooklm --label "Archive Part 2" --max-results 100
```

## Advanced Examples

### Custom filename format (via config):

```yaml
# In .gmail-to-notebooklm.yaml
filename_template: "{date}_{from}_{subject}_{id}"
```

Result: `2024-01-15_john_doe_Project_Update_abc123.md`

### Filtering by date:

```yaml
# In .gmail-to-notebooklm.yaml
filters:
  date_after: "2024-01-01"
  date_before: "2024-12-31"
```

### Excluding automated emails:

```yaml
# In .gmail-to-notebooklm.yaml
filters:
  exclude_senders:
    - "noreply@"
    - "automated@"
    - "donotreply@"
```

## More Information

- [README.md](../README.md) - Project overview
- [USAGE.md](../USAGE.md) - Comprehensive usage guide
- [CONFIGURATION.md](../CONFIGURATION.md) - All configuration options
- [QUICKSTART.md](../QUICKSTART.md) - 5-minute setup guide
