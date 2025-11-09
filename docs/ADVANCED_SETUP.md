# Advanced Setup: Create Your Own OAuth Credentials

> **Note**: This guide is for **advanced users** who want to create their own Google Cloud Project and OAuth credentials.
>
> **Most users don't need this!** If you're using the pre-built Windows executable, OAuth credentials are already embedded. See [SIMPLIFIED_SETUP.md](SIMPLIFIED_SETUP.md) instead.
>
> **Use this guide if you:**
> - Want full control over OAuth credentials
> - Are developing/modifying the application
> - Need more than the 100-user beta limit
> - Prefer not to use embedded credentials

This guide walks you through obtaining the `credentials.json` file required to authenticate with the Gmail API.

## Prerequisites

- A Google account
- Access to [Google Cloud Console](https://console.cloud.google.com/)

## Step-by-Step Instructions

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top of the page
3. Click **"New Project"**
4. Enter a project name (e.g., "Gmail to NotebookLM")
5. Click **"Create"**
6. Wait for the project to be created, then select it from the project dropdown

### 2. Enable the Gmail API

1. In your project, navigate to **"APIs & Services"** > **"Library"** (or use the search bar to find "Gmail API")
2. Search for **"Gmail API"**
3. Click on **"Gmail API"** in the results
4. Click the **"Enable"** button
5. Wait for the API to be enabled (this may take a few seconds)

### 3. Configure OAuth Consent Screen

1. Navigate to **"APIs & Services"** > **"OAuth consent screen"**
2. Select **"External"** user type (unless you have a Google Workspace and want to restrict to internal users)
3. Click **"Create"**
4. Fill in the required fields:
   - **App name**: `Gmail to NotebookLM` (or your preferred name)
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Click **"Save and Continue"**
6. On the **Scopes** page:
   - Click **"Add or Remove Scopes"**
   - Filter for `.../auth/gmail.readonly`
   - Check the box for `https://www.googleapis.com/auth/gmail.readonly`
   - Click **"Update"**
   - Click **"Save and Continue"**
7. On the **Test users** page:
   - Click **"Add Users"**
   - Add your Gmail address (and any other test users)
   - Click **"Save and Continue"**
8. Review the summary and click **"Back to Dashboard"**

### 4. Create OAuth 2.0 Credentials

1. Navigate to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** at the top
3. Select **"OAuth client ID"**
4. For **Application type**, select **"Desktop app"**
5. Enter a name (e.g., "Gmail to NotebookLM Desktop Client")
6. Click **"Create"**
7. A dialog will appear with your client ID and client secret
   - Click **"Download JSON"**
   - Save this file as **`credentials.json`** in the root directory of this project

### 5. Place credentials.json in Your Project

```bash
# Move the downloaded file to your project directory
# The file should be in the same directory as your main.py or CLI script
gmail-to-notebooklm/
├── credentials.json        # ← Place the file here
├── gmail_to_notebooklm/
├── requirements.txt
└── ...
```

**IMPORTANT SECURITY NOTES:**
- **Never commit `credentials.json` to version control** (it's already in `.gitignore`)
- **Never share `credentials.json` publicly**
- The `token.json` file that will be created on first run should also never be committed
- If credentials are compromised, immediately revoke them in Google Cloud Console

### 6. Verify Setup

Once you've placed `credentials.json` in your project directory, you can verify the setup:

```bash
# Run the tool - it will prompt for authorization on first run
gmail-to-notebooklm --label "Test" --output-dir "./test_output"
```

On the first run:
1. A browser window will open
2. Sign in with your Google account (must be a test user you added)
3. Review the permissions (readonly access to Gmail)
4. Click **"Allow"**
5. The tool will save a `token.json` file for future use

## Troubleshooting

### "Access blocked: This app's request is invalid"

**Cause**: OAuth consent screen not configured correctly or missing scopes.

**Solution**:
- Verify you added the `gmail.readonly` scope in the OAuth consent screen
- Make sure you completed all steps in the consent screen configuration

### "Error 403: access_denied"

**Cause**: Your Google account is not listed as a test user.

**Solution**:
- Go to **OAuth consent screen** > **Test users**
- Add your Gmail address
- Try authenticating again

### "The credentials.json file was not found"

**Cause**: File is not in the correct location or has the wrong name.

**Solution**:
- Ensure the file is named exactly `credentials.json` (lowercase)
- Place it in the project root directory (same level as `requirements.txt`)

### "Invalid client secret"

**Cause**: The credentials file is corrupted or from a different project.

**Solution**:
- Delete the existing `credentials.json`
- Download a fresh copy from Google Cloud Console
- Ensure you're downloading from the correct project

## Publishing the App (Production Use)

For production use beyond test users:

1. Go to **OAuth consent screen**
2. Click **"Publish App"**
3. Complete the verification process (required by Google for production apps)
4. Note: Verification can take several days and requires detailed information about your app

For personal/internal use, staying in testing mode with specific test users is recommended.

## Additional Resources

- [Google Gmail API Documentation](https://developers.google.com/gmail/api)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Google Cloud Console](https://console.cloud.google.com/)
