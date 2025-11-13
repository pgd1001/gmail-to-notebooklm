# Getting Help & Documentation

Welcome to Gmail to NotebookLM! This guide helps you find answers and get support.

## Quick Navigation

### 🚀 **Getting Started** (First Time?)
- **Windows Executable Users**: Start with [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md)
- **Python Developers**: Start with [QUICKSTART.md](./QUICKSTART.md)
- **Want to see examples?**: Check [USAGE.md](./USAGE.md)

### ⚙️ **Setup & Authentication**
- **"I don't have credentials"**: [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md)
- **"I want to set up my own OAuth"**: [ADMIN_SETUP.md](./ADMIN_SETUP.md)
- **"I see 'unverified app' warning"**: [BETA_ACCESS.md](./BETA_ACCESS.md)
- **"Something went wrong with setup"**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

### 📚 **Using the App**
- **"What features are available?"**: [FEATURES_GUIDE.md](./FEATURES_GUIDE.md)
- **"How do I configure settings?"**: [CONFIGURATION.md](./CONFIGURATION.md)
- **"How do I use the GUI?"**: [FEATURES_GUIDE.md#gui-features](./FEATURES_GUIDE.md#gui-features)
- **"How do I use the CLI?"**: [FEATURES_GUIDE.md#cli-features](./FEATURES_GUIDE.md#cli-features)

### 🔒 **Privacy & Security**
- **"What data do you collect?"**: [PRIVACY_POLICY.md](./PRIVACY_POLICY.md)
- **"How is my data stored?"**: [PRIVACY_POLICY.md#how-data-is-stored](./PRIVACY_POLICY.md#how-data-is-stored)
- **"How secure is this?"**: [PRIVACY_AND_SECURITY.md](./PRIVACY_AND_SECURITY.md)

### 🐛 **Having Issues?**
- **"Something isn't working"**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **"The app crashed"**: [TROUBLESHOOTING.md#crashes](./TROUBLESHOOTING.md#crashes)
- **"I forgot my setup"**: [TROUBLESHOOTING.md#forgot-setup](./TROUBLESHOOTING.md#forgot-setup)
- **"I'm getting an error"**: [TROUBLESHOOTING.md#error-messages](./TROUBLESHOOTING.md#error-messages)

### 👨‍💻 **For Developers**
- **"I want to contribute"**: [DEVELOPMENT.md](./DEVELOPMENT.md)
- **"How do I build the project?"**: [BUILD_QUICK_REFERENCE.md](./BUILD_QUICK_REFERENCE.md)
- **"How do I build the Windows installer?"**: [BUILD_INSTALLER.md](./BUILD_INSTALLER.md)
- **"How do I build with embedded credentials?"**: [BUILDING_WITH_EMBEDDED_CREDENTIALS.md](./BUILDING_WITH_EMBEDDED_CREDENTIALS.md)

---

## Documentation Map

### **User Guides** (Start Here)

| Document | Best For | Time |
|----------|----------|------|
| [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md) | Windows .exe users, no Python/setup needed | 5 min |
| [QUICKSTART.md](./QUICKSTART.md) | Python developers, quick overview | 10 min |
| [USAGE.md](./USAGE.md) | Learning all features with examples | 20 min |
| [FEATURES_GUIDE.md](./FEATURES_GUIDE.md) | Understanding all user-facing features | 15 min |
| [CONFIGURATION.md](./CONFIGURATION.md) | Customizing settings and config files | 15 min |

### **Setup Guides** (Choose One)

| Document | Best For | Complexity |
|----------|----------|-----------|
| [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md) | Windows users, no setup needed | Easy |
| [ADMIN_SETUP.md](./ADMIN_SETUP.md) | Creating your own OAuth credentials | Medium |
| [ADVANCED_SETUP.md](./ADVANCED_SETUP.md) | Detailed technical setup steps | Hard |

### **Troubleshooting & Support**

| Document | Purpose |
|----------|---------|
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common problems and solutions |
| [BETA_ACCESS.md](./BETA_ACCESS.md) | Beta program info and "unverified app" help |

### **Privacy & Security**

| Document | Purpose |
|----------|---------|
| [PRIVACY_POLICY.md](./PRIVACY_POLICY.md) | What data we collect and how we handle it |
| [PRIVACY_AND_SECURITY.md](./PRIVACY_AND_SECURITY.md) | Security practices and best practices |

### **Developer Guides** (Contributors)

| Document | Purpose |
|----------|---------|
| [DEVELOPMENT.md](./DEVELOPMENT.md) | Getting started as a contributor |
| [BUILD_QUICK_REFERENCE.md](./BUILD_QUICK_REFERENCE.md) | Quick build commands |
| [BUILD_INSTALLER.md](./BUILD_INSTALLER.md) | Building Windows installers |
| [BUILDING_WITH_EMBEDDED_CREDENTIALS.md](./BUILDING_WITH_EMBEDDED_CREDENTIALS.md) | Building with bundled credentials |
| [DISTRIBUTION.md](./DISTRIBUTION.md) | Release and distribution process |

### **Reference**

| Document | Purpose |
|----------|---------|
| [INSTALLATION.md](./INSTALLATION.md) | Installation methods and requirements |
| [SETUP_WINDOWS.md](./SETUP_WINDOWS.md) | Windows-specific installation |
| [README.md](./README.md) | Project overview and links |

---

## Common Questions (FAQ)

### **Setup & Access**

**Q: Do I need to create credentials?**
A: Not if you use the Windows .exe! It has embedded credentials. See [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md).

**Q: Is it safe to give this app access to Gmail?**
A: Yes! The app uses read-only access. It can't delete, modify, or send emails. See [PRIVACY_AND_SECURITY.md](./PRIVACY_AND_SECURITY.md).

**Q: What does "unverified app" mean?**
A: It's normal for beta software. Google just warns you. Click through to continue. See [BETA_ACCESS.md](./BETA_ACCESS.md).

**Q: How often do I need to re-authenticate?**
A: In beta mode, tokens expire after 7 days. After Google verification, it will be longer. See [BETA_ACCESS.md](./BETA_ACCESS.md).

### **Using the App**

**Q: Can I exclude certain emails from export?**
A: Yes! Use query filters like `--query "before:2023-01-01"`. See [FEATURES_GUIDE.md](./FEATURES_GUIDE.md).

**Q: Can I save my settings?**
A: Yes! Use profiles. Save common setups and re-use them. See [FEATURES_GUIDE.md](./FEATURES_GUIDE.md#profiles).

**Q: What if an email has attachments?**
A: The app exports the email body, not attachments. See [USAGE.md](./USAGE.md#limitations).

**Q: How do I organize my exports?**
A: Use `--organize-by-date` to create date-based folders. See [FEATURES_GUIDE.md](./FEATURES_GUIDE.md).

### **Troubleshooting**

**Q: The app won't start**
A: See [TROUBLESHOOTING.md#app-won't-start](./TROUBLESHOOTING.md).

**Q: I'm getting authentication errors**
A: See [TROUBLESHOOTING.md#authentication-errors](./TROUBLESHOOTING.md).

**Q: Files aren't being created**
A: See [TROUBLESHOOTING.md#files-not-created](./TROUBLESHOOTING.md).

**Q: Something else is wrong**
A: See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) or open a GitHub issue.

### **Privacy & Security**

**Q: Where are my files stored?**
A: Only on your computer, in the folder you specify. Never in cloud. See [PRIVACY_POLICY.md](./PRIVACY_POLICY.md).

**Q: Is my Gmail password stored?**
A: No! The app uses OAuth tokens, not passwords. See [PRIVACY_POLICY.md](./PRIVACY_POLICY.md).

**Q: Can I delete everything and revoke access?**
A: Yes! Delete the `~/.gmail-to-notebooklm/` folder. See [PRIVACY_POLICY.md#deletion](./PRIVACY_POLICY.md#deletion).

---

## Support Channels

### 📖 **Documentation** (Recommended First Step)
- This page: [GETTING_HELP.md](./GETTING_HELP.md)
- Troubleshooting: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- All docs: [docs/](./README.md)

### 🐛 **Report Issues**
- **GitHub Issues**: [Open an issue](https://github.com/yourusername/gmail-to-notebooklm/issues)
- **Security Issues**: Email [your.email@example.com] with details

### 💬 **Get Community Help**
- **GitHub Discussions**: [Start a discussion](https://github.com/yourusername/gmail-to-notebooklm/discussions)
- **GitHub Issues**: Ask questions in issues

### 📧 **Contact Project Maintainer**
- **Email**: [your.email@example.com]
- **GitHub**: [@yourusername](https://github.com/yourusername)

---

## Tips for Getting Better Help

### When Reporting Issues
1. **Describe what you did** - Step-by-step reproduction
2. **Show what happened** - Copy exact error messages
3. **Share your environment** - Windows/Mac/Linux, Python version, etc.
4. **Include logs** - Run with `--verbose` to get detailed output

### Example Issue Report
```
Title: "Setup wizard fails with 'credentials not found'"

Steps to reproduce:
1. Opened app
2. Clicked "Setup Wizard"
3. Got error on step 3

Error message:
Credentials file not found at ~/.gmail-to-notebooklm/credentials.json

Environment:
- Windows 11
- Gmail to NotebookLM v0.3.0
- No credentials.json file

What I expected:
Wizard should help me create or find credentials

What actually happened:
Wizard showed error and quit
```

---

## Documentation Shortcuts

### **From the Application**

**Windows .exe (GUI)**:
- Click "Help" menu → "Getting Help & Documentation"
- Opens this page in your browser

**Command Line**:
```bash
# Show all documentation files
g2n --help-setup

# Open docs folder
g2n --show-docs
```

### **From the Web**

- **GitHub Repository**: https://github.com/yourusername/gmail-to-notebooklm
- **Documentation**: https://github.com/yourusername/gmail-to-notebooklm/tree/main/docs
- **Issues**: https://github.com/yourusername/gmail-to-notebooklm/issues
- **Discussions**: https://github.com/yourusername/gmail-to-notebooklm/discussions

---

## Still Need Help?

If you can't find what you're looking for:

1. **Search the docs** - Use Ctrl+F to search this page
2. **Check TROUBLESHOOTING.md** - Most issues are covered there
3. **Open a GitHub Issue** - Describe your problem with as much detail as possible
4. **Browse Examples** - See [USAGE.md](./USAGE.md) for real-world examples

We're here to help! Don't hesitate to ask.

---

**Last Updated**: November 2025
**Version**: 1.0

---

## Quick Links Summary

| I want to... | Go to... |
|---|---|
| Get started quickly | [SIMPLIFIED_SETUP.md](./SIMPLIFIED_SETUP.md) |
| Learn all features | [FEATURES_GUIDE.md](./FEATURES_GUIDE.md) |
| Set up my own credentials | [ADMIN_SETUP.md](./ADMIN_SETUP.md) |
| Fix a problem | [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) |
| Understand privacy | [PRIVACY_POLICY.md](./PRIVACY_POLICY.md) |
| Contribute code | [DEVELOPMENT.md](./DEVELOPMENT.md) |
| Build installers | [BUILD_INSTALLER.md](./BUILD_INSTALLER.md) |
| View all docs | [README.md](./README.md) |
