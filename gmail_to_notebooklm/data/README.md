# Data Directory

This directory contains embedded application data files.

## default_credentials.json

This file contains the default OAuth 2.0 credentials for the application. These credentials allow users to authenticate without creating their own Google Cloud Project.

**IMPORTANT SECURITY NOTES:**

1. **DO NOT commit this file to Git** - It is listed in .gitignore
2. **For distribution only** - These credentials are embedded in the compiled .exe files
3. **Testing mode limitations**:
   - Limited to 100 test users
   - Tokens expire after 7 days
   - Users must be manually added as test users in Google Cloud Console

## How to Add Your Credentials

If you're building this project from source:

1. Create a Google Cloud Project (see ADVANCED_SETUP.md)
2. Create OAuth Desktop App credentials
3. Download the credentials JSON file
4. Copy it to this location as `default_credentials.json`
5. The application will automatically use these embedded credentials

## Credential Search Order

The application looks for credentials in this order:

1. `./credentials.json` (current directory) - User-provided
2. `~/.gmail-to-notebooklm/credentials.json` (user config) - User-provided
3. `gmail_to_notebooklm/data/default_credentials.json` (embedded) - Default

This allows power users to override the embedded credentials with their own.

## For End Users

If you downloaded the pre-built executable, the credentials are already embedded. You don't need to do anything - just run the application and authenticate!
