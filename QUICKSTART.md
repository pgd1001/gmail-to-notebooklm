# Quick Start Guide

Get up and running with Gmail to NotebookLM converter in 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.9+ installed ([download](https://www.python.org/downloads/))
- [ ] Gmail account
- [ ] 5-10 minutes of time

## 5-Minute Setup

### Step 1: Download and Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/gmail-to-notebooklm.git
cd gmail-to-notebooklm

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install
pip install -r requirements.txt
pip install -e .
```

### Step 2: Get Google Credentials (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (name it "Gmail to NotebookLM")
3. Enable Gmail API:
   - Search "Gmail API" → Click Enable
4. Create credentials:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: **Desktop app**
   - Download JSON → Save as `credentials.json` in project root
5. Configure OAuth consent:
   - OAuth consent screen → External → Create
   - Add your Gmail address as a test user

**Need detailed instructions?** See [OAUTH_SETUP.md](OAUTH_SETUP.md)

### Step 3: Run Your First Export (1 minute)

```bash
# Test with any label (creates it if needed)
gmail-to-notebooklm --label "Test" --output-dir "./test_output"
```

**First run**:
- Browser opens automatically
- Sign in to Google
- Click "Allow" to grant read-only access
- Done! Files appear in `./test_output/`

## Example Workflow

### Organize Emails in Gmail

1. Open Gmail
2. Select emails about a project
3. Click the labels icon (🏷️)
4. Create label: "Project Alpha"

### Export to Markdown

```bash
gmail-to-notebooklm --label "Project Alpha" --output-dir "./project_alpha"
```

### Upload to NotebookLM

1. Visit [notebooklm.google.com](https://notebooklm.google.com/)
2. Create new notebook
3. Add sources → Upload
4. Select the `.md` files from `./project_alpha/`
5. Ask NotebookLM questions about your emails!

## Common Commands

```bash
# Export a specific label
gmail-to-notebooklm --label "Client Work" --output-dir "./client_work"

# Limit number of emails
gmail-to-notebooklm --label "Archive" --max-results 50

# See all options
gmail-to-notebooklm --help

# Check version
gmail-to-notebooklm --version
```

## Quick Troubleshooting

### "credentials.json not found"
**Fix**: Download from Google Cloud Console and place in project root

### "Access denied"
**Fix**: Add your Gmail address as test user in OAuth consent screen

### "Module not found"
**Fix**: Activate virtual environment first
```bash
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### "Label not found"
**Fix**: Check label name in Gmail (case-sensitive). Use exact name:
```bash
# Wrong: --label "client a"
# Correct: --label "Client A"
```

## What Gets Exported?

Each email becomes a Markdown file with:

```markdown
---
From: sender@example.com
To: you@example.com
Date: Mon, 15 Jan 2024 10:30:00
Subject: Project Discussion
---

Email content converted to clean Markdown...
```

## File Naming

Files are named based on subject and email ID:

```
Project_Discussion_18a3f2b1.md
Meeting_Notes_c7d9e4a2.md
Weekly_Update_9f1b2c3d.md
```

## Output Directory Structure

```
output/
├── Project_Discussion_18a3f2b1.md
├── Meeting_Notes_c7d9e4a2.md
└── Weekly_Update_9f1b2c3d.md
```

## Security Notes

✅ **Safe**:
- Tool has read-only access to Gmail
- All data stays on your computer
- No cloud storage or external servers

⚠️ **Important**:
- Never share `credentials.json`
- Never commit `token.json` to git (it's in `.gitignore`)
- Both files contain sensitive authentication data

## Real-World Examples

### Use Case 1: Client Communications

```bash
# Export all emails with a client
gmail-to-notebooklm --label "Client ABC" --output-dir "./clients/abc"

# Upload to NotebookLM
# Ask: "Summarize all decisions made with this client"
```

### Use Case 2: Project Documentation

```bash
# Export project emails
gmail-to-notebooklm --label "Project Alpha" --output-dir "./projects/alpha"

# Upload to NotebookLM
# Ask: "Create a timeline of this project's milestones"
```

### Use Case 3: Research Archive

```bash
# Export research discussions
gmail-to-notebooklm --label "Research" --output-dir "./research" --max-results 100

# Upload to NotebookLM
# Ask: "What are the key insights from these discussions?"
```

## Next Steps

### Learn More
- **Full Usage Guide**: [USAGE.md](USAGE.md)
- **Configuration Options**: [CONFIGURATION.md](CONFIGURATION.md)
- **Detailed Installation**: [INSTALLATION.md](INSTALLATION.md)
- **OAuth Setup**: [OAUTH_SETUP.md](OAUTH_SETUP.md)

### Tips
1. **Start Small**: Test with a label containing 5-10 emails first
2. **Use Descriptive Labels**: "Client_ABC_2024" is better than "ABC"
3. **Regular Exports**: Export weekly to keep NotebookLM updated
4. **Organize Output**: Use separate directories per label

### Advanced Features

Once comfortable, explore:
- Environment variables for defaults
- Configuration files for persistent settings
- Batch scripts for multiple labels
- Custom filtering options

## Getting Help

**Documentation**: Check the [README.md](README.md) for links to all guides

**Issues**: Found a bug? [Report it](https://github.com/yourusername/gmail-to-notebooklm/issues)

**Questions**: Review [USAGE.md](USAGE.md) for detailed examples

## Summary

You now know how to:
- ✅ Install and configure the tool
- ✅ Export Gmail labels to Markdown
- ✅ Upload to NotebookLM
- ✅ Troubleshoot common issues

**Ready to dive deeper?** Check out [USAGE.md](USAGE.md) for comprehensive examples and workflows!

---

**Time taken**: ~5 minutes ⏱️
**Difficulty**: Beginner-friendly 🟢
**Next**: Try exporting your first real label!
