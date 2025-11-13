# Privacy Policy

**Gmail to NotebookLM**
**Last Updated**: November 2025

## Overview

Gmail to NotebookLM is a privacy-first application designed to convert your Gmail messages into Markdown files for use with Google NotebookLM. This privacy policy explains how we handle your data.

**TL;DR**: We don't collect, store, or transmit your data. Everything stays on your computer. We only access your Gmail with your explicit permission using read-only access.

---

## Data We Access

### Gmail Access
- **Scope**: `gmail.readonly` (read-only access)
- **What we read**: Email headers (From, To, Cc, Subject, Date) and message bodies
- **What we process**: HTML and text content to convert to Markdown
- **What we export**: Markdown files stored locally on your computer

### What We DON'T Access
- Email attachments
- Contacts or contact information (beyond email addresses in headers)
- Gmail settings or labels metadata
- Any other Google account data

---

## How Data is Stored

### Local Storage Only
All exported files are stored **exclusively on your computer** in the location you specify:

```
your-output-directory/
├── Email_Subject_1_abc123.md
├── Email_Subject_2_def456.md
└── subdirectories/ (if organize-by-date is enabled)
```

### No Cloud Storage
- Files are **never** uploaded to cloud services
- Files are **never** transmitted to our servers
- Files remain under your complete control

### Export Metadata
If you use the export history feature:
- A local SQLite database tracks export statistics
- Location: `~/.gmail-to-notebooklm/history.db`
- Contains: timestamps, file counts, success/failure status
- **Not transmitted anywhere**

### Configuration Files
Your application settings are stored locally:
- Profiles: `~/.gmail-to-notebooklm/profiles.json`
- Config: `~/.gmail-to-notebooklm/config.yaml`
- OAuth tokens: `~/.gmail-to-notebooklm/tokens.pickle`
- **All stored on your computer only**

---

## Google OAuth & Authentication

### How It Works
1. You click "Setup" in the application
2. Your browser opens to Google's login page
3. You sign in and approve read-only Gmail access
4. Google provides a refresh token stored **locally on your computer**
5. The token is used only to fetch your own emails

### Data Handled by Google
- Google handles your Gmail account credentials
- Google authenticates your identity
- Google enforces the `gmail.readonly` scope
- Refer to [Google's Privacy Policy](https://policies.google.com/privacy) for Google's practices

### Token Storage
- OAuth refresh tokens are stored in: `~/.gmail-to-notebooklm/tokens.pickle`
- Stored only on your computer
- Protected by operating system file permissions
- You can revoke access anytime at [Google Account Permissions](https://myaccount.google.com/permissions)

---

## What Happens to Your Data

### Processing
1. Emails are fetched from Gmail using your token
2. HTML content is parsed and converted to Markdown locally
3. Files are written to your specified output directory
4. Your original emails remain unchanged in Gmail

### Retention
- **Exported files**: You decide - kept or deleted at your discretion
- **OAuth tokens**: Kept locally until you revoke access
- **History database**: Kept until you delete it
- **Configuration**: Kept until you delete it

### Deletion
To completely remove all application data:

```bash
# Remove all local data
rm -rf ~/.gmail-to-notebooklm/
rm -rf ~/AppData/Local/gmail_to_notebooklm/  # Windows

# Remove exported files (as desired)
rm -rf ./your-export-directory/

# Revoke Gmail access
# Visit: https://myaccount.google.com/permissions
```

---

## Server Communication

### What Gets Sent to Servers

**Your Emails**: Sent only to **Gmail API (Google's servers)**
- Used only to fetch your messages
- Processed in transit over HTTPS
- Never stored on third-party servers
- Refer to [Google API Terms of Service](https://developers.google.com/terms)

**Application Updates**: If you have auto-update enabled
- Check version number only
- NO usage data is sent
- NO error telemetry is sent
- NO user data is included

### What Does NOT Get Sent

| Item | Status |
|------|--------|
| Exported files | Never sent |
| Configuration | Never sent |
| OAuth tokens | Never sent |
| Email content | Never sent outside Gmail API |
| Usage statistics | Never sent |
| Diagnostic data | Never sent |
| Personal information | Never sent |
| File names or metadata | Never sent (except to your drive) |

---

## Third-Party Services

### What We Use
- **Google Gmail API**: To fetch your emails
- **Google OAuth**: For authentication

### What We Don't Use
- Analytics services (Google Analytics, Mixpanel, etc.)
- Crash reporting (Sentry, Rollbar, etc.)
- Error tracking services
- Any SaaS for data processing
- Advertisement networks
- Tracking pixels

### Open Source Libraries
This application uses open-source libraries. Refer to [DEVELOPMENT.md](./DEVELOPMENT.md) for the complete list. All libraries operate locally without data transmission.

---

## Security Practices

### OAuth Scopes
- **Scope**: `gmail.readonly` - Read-only access to Gmail
- **Cannot**: Modify, delete, or send emails
- **Cannot**: Access other Google services
- **Cannot**: Access contacts, calendar, or drive

### Token Security
- Refresh tokens are stored encrypted by the operating system
- Access tokens are generated fresh for each session
- Tokens are never logged or exposed
- Users can revoke access anytime

### File Security
- Exported files have standard file system permissions
- Windows: Protected by NTFS permissions
- Mac/Linux: Protected by standard file permissions
- You should use full-disk encryption for maximum security

### Transport Security
- All communication with Gmail API uses HTTPS (TLS 1.2+)
- Data in transit is encrypted
- Certificate validation is enforced

---

## User Rights

### Access Your Data
You have complete access to all your data at any time:
- Export files are in plain Markdown format
- Configuration is in plain JSON/YAML
- No proprietary formats or encryption

### Modify Your Data
You can modify any exported files:
- Edit Markdown files directly
- Modify configuration files
- Remove files as needed

### Delete Your Data
You can delete any or all data:
- Delete exported files anytime
- Delete configuration: `rm -rf ~/.gmail-to-notebooklm/`
- Delete history: Delete `~/.gmail-to-notebooklm/history.db`
- Revoke OAuth access: Google Account Permissions page

### Port Your Data
All data is in open formats:
- Markdown files can be used anywhere
- Configuration is JSON/YAML (standard formats)
- No lock-in or proprietary formats

---

## Changes to This Policy

We may update this privacy policy as the application evolves. Changes will be:
- Announced in GitHub releases
- Documented in the CHANGELOG
- Available at: [PRIVACY_POLICY.md](https://github.com/yourusername/gmail-to-notebooklm/blob/main/docs/PRIVACY_POLICY.md)

---

## Contact & Support

### Questions About Privacy?
- Open an issue: [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues)
- Email: [your.email@example.com]
- Security concerns: Please report responsibly

### Getting Help
- Troubleshooting: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Setup help: [GETTING_HELP.md](./GETTING_HELP.md)
- Features guide: [FEATURES_GUIDE.md](./FEATURES_GUIDE.md)

---

## Compliance

### GDPR (General Data Protection Regulation)
- We comply with GDPR as an open-source project
- No data is processed on EU servers (unless you use your own)
- Data is processed locally on your machine
- Your data is always under your control

### CCPA (California Consumer Privacy Act)
- No personal information is collected
- No personal information is sold
- Complete data deletion is supported
- Data access is transparent

### Other Regulations
This is a local-first, privacy-first application:
- No data collection = no data privacy concerns
- All processing is on your device
- Compliance is by design

---

## Summary

**This application is designed with privacy as a core principle:**

✓ No data collection
✓ No data transmission
✓ No third-party sharing
✓ No tracking or analytics
✓ No advertisements
✓ Open source and auditable
✓ Complete user control

Your data remains yours. Always.

---

**Version**: 1.0
**Effective Date**: November 2025
**GitHub Repository**: https://github.com/yourusername/gmail-to-notebooklm
