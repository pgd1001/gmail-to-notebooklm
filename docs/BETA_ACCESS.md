# Beta Testing Program

Gmail to NotebookLM is currently in **Testing Mode** with Google OAuth, which means the application is limited to **100 beta testers**.

## What is Testing Mode?

Testing Mode is Google's initial stage for OAuth applications. It allows up to 100 users to use the application while the developer prepares for full verification.

### Current Limitations

- ✅ **100 total users** (lifetime limit until verification)
- ⚠️ **Authentication tokens expire after 7 days** (requires re-authentication)
- ⚠️ **"Unverified app" warning** during first login
- ✅ **Full functionality** (all features work normally)

### After Full Verification

We plan to complete Google's verification process, which will:
- ✅ Remove the 100-user limit
- ✅ Remove "unverified app" warnings
- ✅ Extend token lifetime (no 7-day expiration)
- ✅ Professional "Verified" status

## Requesting Beta Access

### Who Can Be a Beta Tester?

Anyone can request beta access! We're looking for:

- **Early adopters** who want to try the application
- **Feedback providers** who can report bugs and suggest improvements
- **Use case explorers** who will test different Gmail export scenarios
- **Documentation reviewers** who can help improve our guides

### How to Request Access

1. **Check Availability**: We have limited spots (100 total users)

2. **Submit Request**: Email **pgd1001@gmail.com** with:
   - **Subject**: "Gmail to NotebookLM - Beta Access Request"
   - **Your Gmail address** (the one you'll use for authentication)
   - **Brief description** of your use case (optional)
   - **Platform**: Windows version (10 or 11)

3. **Wait for Confirmation**: We'll add you as a test user (usually within 24-48 hours)

4. **Download and Install**: Once confirmed, download from [GitHub Releases](https://github.com/pgd1001/gmail-to-notebooklm/releases)

5. **Authenticate**: Run the app, click through the "unverified app" warning (this is normal!)

### Email Template

```
To: pgd1001@gmail.com
Subject: Gmail to NotebookLM - Beta Access Request

Hi,

I'd like to become a beta tester for Gmail to NotebookLM.

Gmail address: your.email@gmail.com
Windows version: Windows 11 (or 10)
Use case: [Brief description - optional]

Thank you!
```

## Using the "Unverified App" Warning

Even as a beta tester, you'll see an "unverified app" warning during first login. This is completely normal and safe. Here's how to proceed:

### Step-by-Step Authentication

1. **Launch the application**

2. **Start authentication** (browser will open automatically)

3. **Sign in** to your Gmail account

4. **See the warning screen**:
   ```
   Google hasn't verified this app
   ```

5. **Click "Advanced"** at the bottom of the warning

6. **Click "Go to Gmail to NotebookLM (unsafe)"**
   - Note: It's not actually unsafe - this is standard for apps in Testing mode
   - The app only requests read-only Gmail access

7. **Review permissions**:
   - Read your email messages and settings
   - This is read-only access - cannot send or delete emails

8. **Click "Allow"**

9. **You're authenticated!** The app will work normally now

### Why the "Unsafe" Warning?

This warning appears for all apps in Testing mode that haven't completed Google's verification process. The app is completely safe because:

- ✅ Uses official Google OAuth 2.0
- ✅ Read-only access (cannot modify emails)
- ✅ Open-source code (you can review it)
- ✅ Stores tokens locally only
- ✅ No third-party servers involved

## Beta Tester Responsibilities

As a beta tester, we ask that you:

### Provide Feedback

- **Report bugs**: Open issues on [GitHub](https://github.com/pgd1001/gmail-to-notebooklm/issues)
- **Suggest features**: Share ideas for improvements
- **Document issues**: Include error messages and steps to reproduce

### Test Scenarios

Try different export scenarios:
- Various Gmail labels
- Different date ranges
- Large exports (100+ emails)
- Special characters in email subjects
- Emails with attachments
- Different email formats (HTML, plain text)

### Share Your Experience

- What works well?
- What's confusing?
- What could be improved?
- How do you use the exported Markdown files?

## Re-authentication After 7 Days

### Why Tokens Expire

In Testing mode, Google requires re-authentication every 7 days. This is a security measure for unverified apps.

### How to Re-authenticate

When your token expires:

1. **You'll see an authentication error** when using the app

2. **Delete the token** (GUI has a "Revoke Token" option, or manually delete `token.json`)

3. **Run the app again** - authentication will start automatically

4. **Go through the OAuth flow** again (same "unverified app" warning process)

This limitation will be removed after full verification.

## Current Beta Status

- **Available Slots**: Contact us to check availability
- **Verification Timeline**: Planned for Q1 2025
- **Current Version**: v0.4.0
- **Platform**: Windows 10/11 (64-bit)

## Frequently Asked Questions

### Is this free?

Yes! Gmail to NotebookLM is free and open-source (MIT License).

### Will my data be shared?

No. The application:
- Runs entirely on your computer
- Stores nothing in the cloud
- Only accesses your Gmail (read-only)
- Never sends data to third-party servers

### Can I test the Python version instead?

Yes! Advanced users can:
1. Clone the repository
2. Install dependencies (`pip install -e .`)
3. Use their own OAuth credentials (see [ADVANCED_SETUP.md](ADVANCED_SETUP.md))

This bypasses the 100-user limit but requires creating your own Google Cloud Project.

### What happens after verification?

After verification:
- Existing beta testers continue with no interruption
- New users can download and use without manual approval
- Tokens won't expire after 7 days
- No more "unverified app" warnings

### Can I help with verification?

Yes! The best way to help is:
- Test thoroughly and report bugs
- Provide feedback on documentation
- Share your use cases and suggestions
- Spread the word if you find it useful

## Development Roadmap

### Phase 4: Distribution & Packaging ✅ (Current)
- Windows standalone executables
- Professional installer
- Embedded OAuth credentials

### Phase 4B: Simplified OAuth ✅ (Current)
- Embedded credentials in .exe files
- Simplified user experience
- Beta testing program

### Phase 5: Verification & Scaling (Planned Q1 2025)
- Complete Google OAuth verification
- Remove 100-user limit
- Professional verified status
- Extended token lifetime

### Future Phases (Planned)
- Cloud sync features
- Automated scheduling
- Advanced filtering
- macOS and Linux support

## Contact

Questions about beta access?

- **Email**: pgd1001@gmail.com
- **GitHub Issues**: [Report bugs](https://github.com/pgd1001/gmail-to-notebooklm/issues)
- **Documentation**: [Full docs](README.md)

---

Thank you for being an early adopter! Your feedback helps make Gmail to NotebookLM better for everyone.

**Version**: 0.4.0
**Last Updated**: 2025-11-06
**License**: MIT
