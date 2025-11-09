# Gmail to NotebookLM - Documentation

Complete documentation for Gmail to NotebookLM application.

## Quick Start

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[SIMPLIFIED_SETUP.md](SIMPLIFIED_SETUP.md)** - For Windows .exe users (no Python needed) ⭐ **START HERE**

## User Guides

### For End Users
- **[SIMPLIFIED_SETUP.md](SIMPLIFIED_SETUP.md)** - Using pre-built Windows executables
- **[BETA_ACCESS.md](BETA_ACCESS.md)** - Joining the beta testing program
- **[USAGE.md](USAGE.md)** - Comprehensive feature guide and examples
- **[CONFIGURATION.md](CONFIGURATION.md)** - Configuration options and settings

### For Advanced Users
- **[INSTALLATION.md](INSTALLATION.md)** - Python installation from source
- **[ADVANCED_SETUP.md](ADVANCED_SETUP.md)** - Creating your own OAuth credentials
- **[SETUP_WINDOWS.md](SETUP_WINDOWS.md)** - Windows-specific setup instructions

## Developer Guides

### Building & Distribution
- **[BUILDING_WITH_EMBEDDED_CREDENTIALS.md](BUILDING_WITH_EMBEDDED_CREDENTIALS.md)** - How to build with embedded OAuth ⭐ **IMPORTANT**
- **[BUILD_INSTALLER.md](BUILD_INSTALLER.md)** - Building Windows executables and installer
- **[DISTRIBUTION.md](DISTRIBUTION.md)** - Distribution strategy and release process
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development setup and contribution guide

### Project Information
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[phases/](phases/)** - Phase summaries and roadmaps

## Documentation Structure

```
docs/
├── README.md (this file)           # Documentation index
│
├── User Guides/
│   ├── QUICKSTART.md              # 5-minute setup
│   ├── SIMPLIFIED_SETUP.md        # For .exe users ⭐
│   ├── BETA_ACCESS.md             # Beta testing program
│   ├── USAGE.md                   # Feature guide
│   ├── CONFIGURATION.md           # Settings & config
│   ├── INSTALLATION.md            # Python installation
│   ├── ADVANCED_SETUP.md          # Custom OAuth setup
│   └── SETUP_WINDOWS.md           # Windows setup
│
├── Developer Guides/
│   ├── BUILDING_WITH_EMBEDDED_CREDENTIALS.md  ⭐ How to build
│   ├── BUILD_INSTALLER.md         # Build process
│   ├── DISTRIBUTION.md            # Distribution guide
│   └── DEVELOPMENT.md             # Dev setup
│
├── Project Info/
│   └── CHANGELOG.md               # Version history
│
└── phases/                        # Phase documentation
    ├── PHASE1_ISSUES.md
    ├── PHASE1_ROADMAP.md
    ├── EXPANSION_ROADMAP.md
    ├── PHASE4_SUMMARY.md
    └── PHASE4B_SUMMARY.md
```

## Common Tasks

### I want to...

**Use the application** (as an end user):
1. Download the Windows installer from [GitHub Releases](https://github.com/pgd1001/gmail-to-notebooklm/releases)
2. Follow [SIMPLIFIED_SETUP.md](SIMPLIFIED_SETUP.md)
3. See [USAGE.md](USAGE.md) for features

**Join the beta testing program**:
- See [BETA_ACCESS.md](BETA_ACCESS.md) for access request process

**Build the application for distribution**:
1. Follow [BUILDING_WITH_EMBEDDED_CREDENTIALS.md](BUILDING_WITH_EMBEDDED_CREDENTIALS.md) ⭐
2. See [BUILD_INSTALLER.md](BUILD_INSTALLER.md) for build process
3. See [DISTRIBUTION.md](DISTRIBUTION.md) for release process

**Develop and contribute**:
1. See [INSTALLATION.md](INSTALLATION.md) for Python setup
2. See [DEVELOPMENT.md](DEVELOPMENT.md) for development workflow
3. See [ADVANCED_SETUP.md](ADVANCED_SETUP.md) for OAuth credentials

**Understand what changed**:
- See [CHANGELOG.md](CHANGELOG.md) for version history

## Key Features

- **No Python Required** - Standalone Windows executables
- **Simplified OAuth** - Embedded credentials, no Google Cloud Console setup
- **Desktop GUI** - Modern Tkinter interface
- **Enhanced CLI** - DevOps-friendly command-line tool
- **Export History** - Track all exports with SQLite
- **Profile Management** - Save and reuse export configurations
- **Read-Only Access** - Cannot send or delete emails
- **Local Processing** - All data stays on your machine

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/pgd1001/gmail-to-notebooklm/issues)
- **Email**: pgd1001@gmail.com
- **Documentation**: This directory!

## Version

**Current Version**: 0.4.0

**What's New in 0.4.0**:
- ✅ Simplified OAuth with embedded credentials
- ✅ Windows standalone executables (.exe)
- ✅ Professional installer
- ✅ Beta testing program
- ✅ Comprehensive documentation reorganization

See [CHANGELOG.md](CHANGELOG.md) for full history.

## Quick Links

| I am... | I want to... | Read this |
|---------|--------------|-----------|
| End User | Use the app | [SIMPLIFIED_SETUP.md](SIMPLIFIED_SETUP.md) |
| End User | Learn all features | [USAGE.md](USAGE.md) |
| Beta Tester | Join beta program | [BETA_ACCESS.md](BETA_ACCESS.md) |
| Developer | Build executables | [BUILDING_WITH_EMBEDDED_CREDENTIALS.md](BUILDING_WITH_EMBEDDED_CREDENTIALS.md) |
| Developer | Develop/contribute | [DEVELOPMENT.md](DEVELOPMENT.md) |
| Power User | Custom OAuth setup | [ADVANCED_SETUP.md](ADVANCED_SETUP.md) |
| Distributor | Release strategy | [DISTRIBUTION.md](DISTRIBUTION.md) |

---

**License**: MIT
**Repository**: https://github.com/pgd1001/gmail-to-notebooklm
**Author**: Paul Deegan
