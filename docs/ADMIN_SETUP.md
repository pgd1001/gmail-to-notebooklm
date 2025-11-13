# Admin Setup Guide: Creating Custom OAuth Credentials

This guide is for developers and advanced users who want to create their own OAuth credentials instead of using embedded credentials.

**For most users**: Use the Windows .exe with embedded credentials. See [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md).

**For Python developers**: See [ADVANCED_SETUP.md](./ADVANCED_SETUP.md) for a quicker version.

---

## Overview

This process creates Google OAuth 2.0 credentials that allow Gmail to NotebookLM to access your Gmail account.

**What you'll do**:
1. Create a Google Cloud Project
2. Enable the Gmail API
3. Create OAuth 2.0 credentials
4. Configure OAuth consent screen
5. Download credentials.json
6. Use with the application

**Time**: ~10 minutes (first time)

**Requirements**:
- Google account
- Web browser
- No payment needed (API access is free)

---

## Step 1: Create a Google Cloud Project

### 1.1 Open Google Cloud Console

Visit: https://console.cloud.google.com/

**If this is your first time**:
- Click "Select a Project"
- Click "New Project"
- Enter project name: "Gmail to NotebookLM"
- Click "Create"

**If you already have projects**:
- Click the project dropdown at top
- Click "New Project"
- Enter project name: "Gmail to NotebookLM"
- Click "Create"

The project will be created (takes a few seconds).

### 1.2 Verify Project is Selected

In the top left, you should see:
```
Google Cloud  > Gmail to NotebookLM
```

If not, click the dropdown and select "Gmail to NotebookLM".

---

## Step 2: Enable the Gmail API

### 2.1 Open the API Library

In the left sidebar:
1. Click "APIs & Services"
2. Click "Library"

### 2.2 Search for Gmail API

1. In the search box, type: `Gmail API`
2. Click on "Gmail API" (the blue card)

### 2.3 Enable Gmail API

1. Click the blue "ENABLE" button
2. Wait for it to enable (takes a few seconds)
3. You should see: "Gmail API is now enabled"

---

## Step 3: Configure OAuth Consent Screen

### 3.1 Open OAuth Consent Screen

In the left sidebar:
1. Under "APIs & Services", click "OAuth consent screen"

### 3.2 Choose User Type

You'll see two options:
- **Internal** - For Google Workspace domains only
- **External** - For anyone with a Google account

Choose **External**.

Click "Create".

### 3.3 Fill in App Information

**App name** (required):
- Enter: `Gmail to NotebookLM`

**User support email** (required):
- Enter your email address

**Developer contact information** (required):
- Enter your email address

**Privacy policy URL** (optional, but good to have):
- You can skip this for testing

Click "Save and Continue".

### 3.4 Add Scopes

On the "Scopes" page:

1. Click "Add or Remove Scopes"
2. Search for: `gmail.readonly`
3. Check the box next to `https://www.googleapis.com/auth/gmail.readonly`
4. This scopes allow read-only access to Gmail (cannot delete or modify emails)
5. Click "Update"
6. Click "Save and Continue"

### 3.5 Add Test Users

On the "Test users" page:

1. Click "Add Users"
2. Enter your email address (the one you'll use with this app)
3. Click "Add"
4. Click "Save and Continue"

You're now a test user, so you can use this app without "unverified app" warnings.

### 3.6 Review & Finish

Review the information and click "Back to Dashboard".

---

## Step 4: Create OAuth 2.0 Credentials

### 4.1 Create Credentials

In the left sidebar:
1. Click "APIs & Services" → "Credentials"

### 4.2 Create OAuth Client ID

Click "Create Credentials" (blue button at top).

Select: **"OAuth 2.0 Client ID"**

### 4.3 Choose Application Type

A dialog will ask "Which API are you using?"

Choose: **"Desktop application"** (not Web application)

Click "Create".

### 4.4 Download Credentials

A dialog will appear with your Client ID and Client Secret.

**You have two options**:

**Option A: Download the JSON File (Recommended)**
1. Click "Download" button (cloud download icon)
2. Save the file as `credentials.json`
3. Keep this file safe - it's how the app authenticates

**Option B: Copy the Credentials**
1. Click "Copy" for Client ID
2. Save it somewhere
3. Click "Copy" for Client Secret
4. Save it somewhere
5. Manually create `credentials.json` file (harder)

**Use Option A** (download).

Click "OK" to close the dialog.

---

## Step 5: Verify Credentials File

### 5.1 Check Downloaded File

The downloaded file should contain:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "gmail-to-notebooklm",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

**Keep this file secret!** It allows authentication to your account.

---

## Step 6: Use with the Application

### 6.1 For Windows .exe Users

**Skip this step** if using embedded credentials. Just run the app.

If building your own .exe:

1. Copy `credentials.json` to: `gmail_to_notebooklm/data/default_credentials.json`
2. Follow [BUILDING_WITH_EMBEDDED_CREDENTIALS.md](./BUILDING_WITH_EMBEDDED_CREDENTIALS.md)

### 6.2 For Python Users

Place the downloaded `credentials.json` in one of these locations:

**Option A: Project Root** (simplest)
```
your-project/
├── credentials.json          ← Place here
├── main.py
└── ...
```

**Option B: Config Directory** (recommended)
```
~/.gmail-to-notebooklm/
├── credentials.json          ← Place here
└── ...
```

**Option C: Custom Location**
```bash
# Use --credentials flag
g2n --label "Inbox" --credentials "/path/to/credentials.json"

# Or in config file
echo "credentials: /path/to/credentials.json" >> config.yaml
```

### 6.3 First Run - Authentication

Run the application:

**GUI**:
```bash
g2n-gui
# Or from Python module
python -m gmail_to_notebooklm.gui.main
```

**CLI**:
```bash
g2n --label "Inbox"
# Or from Python module
python -m gmail_to_notebooklm.main --label "Inbox"
```

Your browser will open. Sign in with the Google account you added as a test user.

You'll see permissions request:
- `gmail.readonly` - Read-only access to emails

Click "Allow".

The app will save a token for future use.

---

## Troubleshooting

### "Unverified app" Warning

**Why**: Your OAuth app is in testing mode.

**What to do**:
1. Click "Advanced" at bottom
2. Click "Go to Gmail to NotebookLM (unsafe)"
3. Review permissions
4. Click "Allow"

This is normal and expected for testing.

### Can't Find API Library

Check you:
1. Created a project successfully
2. Selected the correct project (top left dropdown)
3. Are in the correct Google Cloud Console (console.cloud.google.com)

### Missing "Create Credentials" Button

Check:
1. Gmail API is enabled
2. You're in "Credentials" page (left sidebar)
3. Signed in with correct Google account

### credentials.json Not Being Found

Check:
1. File is named exactly `credentials.json` (case-sensitive on Mac/Linux)
2. File is in correct location (see Step 6)
3. File contains `"installed"` key, not `"web"`

### "Invalid Client ID" Error

The credentials.json file may be:
1. Corrupted
2. For wrong application type (web instead of desktop)
3. From wrong project

**Solution**: Re-download from Google Cloud Console.

---

## Next Steps

1. **Verify credentials work**:
   ```bash
   g2n --list-labels

   # Should show your Gmail labels without error
   ```

2. **Try first export**:
   ```bash
   g2n --label "Inbox" --max-results 5 --dry-run

   # Preview what would be exported
   ```

3. **Do first real export**:
   ```bash
   g2n --label "Inbox" --max-results 5

   # Create 5 Markdown files from recent emails
   ```

4. **Learn features**: [FEATURES_GUIDE.md](./FEATURES_GUIDE.md)

---

## Advanced: Extending Access

### Add More Test Users

If multiple people need to use this OAuth app:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. "APIs & Services" → "OAuth consent screen"
4. Scroll to "Test users"
5. Click "Add Users"
6. Enter email of person who should have access
7. Click "Add"

That person can now authenticate.

### Upgrading from Testing to Production

After you've tested and want to distribute widely:

1. Submit OAuth app for verification to Google
2. Google reviews your app (7-14 days typically)
3. Once verified, no more "unverified app" warnings
4. Token expiration increases from 7 to 365 days

See [DISTRIBUTION.md](./DISTRIBUTION.md) for details.

---

## Security Best Practices

### Protect Your Credentials

1. **Never commit credentials.json to git**:
   ```bash
   # Add to .gitignore
   echo "credentials.json" >> .gitignore
   ```

2. **Don't share credentials file**:
   - Each person should create their own
   - Or use embedded credentials (built by admin)

3. **Use environment variables** (advanced):
   ```bash
   export GMAIL_CREDENTIALS_PATH="/path/to/credentials.json"
   g2n --label "Inbox"
   ```

4. **Revoke access if leaked**:
   - Go to [Google Account Settings](https://myaccount.google.com/permissions)
   - Find "Gmail to NotebookLM"
   - Click "Remove"
   - Create new credentials

### Limit API Scopes

The app only requests:
- `gmail.readonly` - Read-only access

It **cannot**:
- Delete emails
- Send emails
- Access other Google services
- Access contacts or calendar
- Modify any Gmail settings

### Rotate Credentials Periodically

For high-security environments:
1. Create new credentials every 90 days
2. Delete old credentials from Google Cloud Console
3. Update your copies with new credentials.json

---

## Reference

### Google Cloud Console URLs

- **Main Console**: https://console.cloud.google.com
- **Project Selector**: https://console.cloud.google.com/home/dashboard
- **Gmail API Page**: https://console.cloud.google.com/apis/library/gmail.googleapis.com
- **Credentials Page**: https://console.cloud.google.com/apis/credentials
- **OAuth Consent**: https://console.cloud.google.com/apis/consent

### Gmail API Docs

- **Gmail API Overview**: https://developers.google.com/gmail/api/overview
- **Gmail API Reference**: https://developers.google.com/gmail/api/reference/rest
- **OAuth 2.0 Scopes**: https://developers.google.com/gmail/api/auth/scopes

---

## Need Help?

- **Setup Issues**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **Can't find something**: [GETTING_HELP.md](./GETTING_HELP.md)
- **Quick version**: [ADVANCED_SETUP.md](./ADVANCED_SETUP.md)
- **Report issue**: [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues)

---

**Last Updated**: November 2025
**Version**: 1.0

**For most users**, you don't need this document. Use [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md) instead.
