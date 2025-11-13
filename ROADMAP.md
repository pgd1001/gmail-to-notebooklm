# Gmail to NotebookLM - Development Roadmap

**Version:** 0.7.0
**Last Updated:** November 2025
**Current Status:** Beta with email consolidation and NotebookLM anchors

---

## Overview

This roadmap outlines the planned enhancements to Gmail to NotebookLM through v1.5.0. Features are organized by priority, effort, and release phase.

**Legend:**
- 🔴 High Priority | 🟡 Medium Priority | 🟢 Low Priority
- ⏱️ Effort (Low/Medium/High)
- 📅 Estimated Release

---

## Phase 1: Foundation & Quality (v0.8.0 - v0.9.0)

**Focus:** Stability, performance, and critical missing features
**Timeline:** Q4 2025 - Q1 2026
**Status:** In Planning

### 1.1 🔴 Attachment Handling ⏱️ High 📅 v0.8.0

**Goal:** Extract, save, and reference email attachments

**Features:**
- Save attachments to separate `attachments/` folder structure
- Generate markdown links to attachments in email body
- Support inline images (base64 encode or file references)
- Attachment metadata in email headers (filename, size, type)
- Option to skip attachments for consolidation mode

**Implementation Details:**
- Modify `parser.py` to extract attachment metadata
- Update `converter.py` to generate attachment links
- Add `attachment_handler.py` utility module
- Update CLI with `--include-attachments` flag
- Update GUI with attachment checkbox

**Dependencies:**
- No external dependencies (use email.mime standard library)

**Testing:**
- Unit tests for attachment extraction
- Integration tests with various attachment types
- Test with malformed attachments

**Files to Modify:**
- `gmail_to_notebooklm/parser.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/utils.py` (add attachment utilities)
- `gmail_to_notebooklm/main.py` (CLI flag)
- `gmail_to_notebooklm/gui/windows/main_window.py` (GUI checkbox)

---

### 1.2 🔴 Email Threading & Conversation View ⏱️ High 📅 v0.8.0

**Goal:** Group emails by thread for better context

**Features:**
- Auto-detect email threads using `thread_id` from Gmail API
- Show thread relationships (reply-to chains)
- Add "Thread: X of Y" indicator in email headers
- Thread-based table of contents in consolidated docs
- Option to group consolidation by thread (already supported, enhance display)

**Implementation Details:**
- Add `thread_depth` calculation to `parser.py`
- Create `EmailThread` data structure in `utils.py`
- Modify `converter.py` to show thread context
- Add visual threading in consolidated output (indentation, arrows)
- Update core.py grouping logic

**Example Output:**
```markdown
## Email Threading {#thread-abc123}

### [0/1] Project Kickoff {#email-project-kickoff-xyz}
**From:** Manager <manager@example.com>
**To:** Team <team@example.com>
**Date:** January 1, 2024

Let's start the project...

---

### [1/1] RE: Project Kickoff {#email-re-project-kickoff-xyz}
> Let's start the project...

**From:** Developer <dev@example.com>
**To:** Manager <manager@example.com>
**Date:** January 2, 2024

Sounds good, I'm ready!
```

**Files to Modify:**
- `gmail_to_notebooklm/parser.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/utils.py`
- `gmail_to_notebooklm/core.py`

---

### 1.3 🟡 Better Error Handling ⏱️ Medium 📅 v0.8.0

**Goal:** Improve debugging and recovery from errors

**Features:**
- Per-email error logs (not just summary)
- Detailed error recovery suggestions
- Option to skip problematic emails and continue
- Error report generation (HTML or PDF)
- Debug mode with verbose logging

**Implementation Details:**
- Add `error_handler.py` module
- Modify `core.py` to collect detailed error context
- Add error reporting in `ExportResult`
- Create error recovery strategies

**Example Error Report:**
```
Email ID: 1234567890abcdef
Subject: Important Project Update
From: user@example.com
Error: Failed to convert HTML to Markdown
Details: BeautifulSoup parse error on malformed HTML
Suggestion: Try exporting with plaintext body only
```

**Files to Modify:**
- `gmail_to_notebooklm/core.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/parser.py`
- `gmail_to_notebooklm/main.py` (add error report output)

---

### 1.4 🟡 Performance Optimization ⏱️ Medium 📅 v0.9.0

**Goal:** Speed up exports for large mailboxes

**Features:**
- Parallel email fetching (async requests)
- Gmail label list caching (30-min TTL)
- Streaming file writes (don't buffer entire consolidated doc)
- Batch API calls optimization
- Progress prediction with ETA

**Implementation Details:**
- Add `asyncio` support to `gmail_client.py`
- Implement LRU cache for labels
- Refactor `converter.py` for streaming
- Add ETA calculation in `core.py`

**Expected Improvements:**
- 50% faster for 100+ emails
- 70% faster for 500+ emails
- Reduced memory usage for large exports

**Files to Modify:**
- `gmail_to_notebooklm/gmail_client.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/core.py`
- `gmail_to_notebooklm/utils.py` (caching utilities)

---

## Phase 2: Search & Discovery (v1.0.0)

**Focus:** Better filtering and export management
**Timeline:** Q1 2026 - Q2 2026
**Status:** Planning

### 2.1 🔴 Advanced Search & Filter UI ⏱️ Medium 📅 v1.0.0

**Goal:** Rich filtering without command line complexity

**Features:**
- Date range picker (visual calendar)
- Sender autocomplete from email history
- Subject search with regex support
- Size range filter (KB to MB)
- Quick shortcuts: "Last 7 days", "Last 30 days", "This month"
- Multi-select senders (OR logic)
- Advanced filter builder (AND/OR/NOT chains)

**Implementation Details:**
- Add filter builder widget to `main_window.py`
- Create `FilterBuilder` class in `utils.py`
- Translate visual filters to Gmail API queries
- Store filter history in `config.yaml`

**GUI Layout:**
```
┌─ Advanced Filters ────────────────────┐
├ Date Range: [📅] From [📅] To        │
├ Senders: [Dropdown/Autocomplete]     │
├ Subject: [Search Box] [Regex ☐]     │
├ Size: [____] KB to [____] KB         │
├ Quick: [Last 7 days] [This Month]   │
├ ─────────────────────────────────────│
├ [+] Add Filter  [Clear] [Save As]   │
└─────────────────────────────────────┘
```

**Files to Modify:**
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/utils.py` (filter utilities)
- `gmail_to_notebooklm/config.py` (store filter presets)

---

### 2.2 🔴 Export Profiles & Presets ⏱️ Medium 📅 v1.0.0

**Goal:** Save and reuse export configurations

**Features:**
- Save current export settings as named profile
- Load previous profiles with one click
- Profile library: "Work Emails", "Client A Q4", etc.
- Share profiles via JSON export
- Default profiles for common patterns

**Default Profiles:**
- "Last 30 Days" - All emails from past month
- "Client Emails" - Emails to/from specific domain
- "Project Archive" - All labeled emails for a project
- "This Week" - Current week emails

**Implementation Details:**
- Add profile management to `config.py`
- Create `ProfileManager` class
- Update GUI to show profile list
- Add save/load dialogs

**Files to Modify:**
- `gmail_to_notebooklm/config.py`
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/gui/windows/profiles_dialog.py` (enhance)

---

### 2.3 🟡 Rich Metadata Extraction ⏱️ Medium 📅 v1.0.0

**Goal:** Include more contextual information in exports

**Features:**
- Extract and display Gmail labels per email
- Show importance/star status (⭐)
- Extract custom headers (X-Priority, X-Custom, etc.)
- Thread size indicator (replies count)
- Snippet of first reply in thread (if available)

**Example Output:**
```markdown
## Project Kickoff {#email-project-kickoff-xyz}

**From:** Manager <manager@example.com>
**To:** Team <team@example.com>
**Date:** January 1, 2024 at 10:30 AM
**Labels:** Work, Q1-Projects, High-Priority ⭐
**Thread:** 5 replies
**Importance:** High

> First reply snippet from Developer...
```

**Files to Modify:**
- `gmail_to_notebooklm/parser.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/utils.py`

---

### 2.4 🟡 Label Hierarchy Display ⏱️ Medium 📅 v1.0.0

**Goal:** Better navigation of complex label structures

**Features:**
- Tree view of Gmail label hierarchy (Parent/Child)
- Visual label organization in GUI
- Multi-select labels with boolean operators
- Label search/filter
- Show email count per label

**Tree View Example:**
```
📁 Work
  ├─ 📧 Inbox (42)
  ├─ 📁 Projects (98)
  │  ├─ Project-A (23)
  │  └─ Project-B (75)
  └─ 📁 Archive (156)
📁 Personal
  └─ 📧 Family (12)
```

**Files to Modify:**
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/utils.py` (label hierarchy utilities)

---

## Phase 3: Advanced Features (v1.1.0 - v1.2.0)

**Focus:** Smart features and content optimization
**Timeline:** Q2 2026 - Q3 2026
**Status:** Planning

### 3.1 🟡 Email Deduplication ⏱️ Medium 📅 v1.1.0

**Goal:** Remove redundant emails from exports

**Features:**
- Detect duplicates by message-id
- Detect near-duplicates (quoted chains)
- Option to summarize long email threads
- Remove quoted text from replies (optional)
- Keep only latest in duplicate chains

**Implementation Details:**
- Add `deduplicator.py` module
- Hash-based duplicate detection
- Similarity scoring for near-duplicates
- Summary generation using simple heuristics

**Files to Modify:**
- Add `gmail_to_notebooklm/deduplicator.py`
- `gmail_to_notebooklm/core.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/main.py` (add CLI flags)

---

### 3.2 🟡 Incremental Exports ⏱️ High 📅 v1.1.0

**Goal:** Only export new emails since last export

**Features:**
- Track previously exported emails
- Only fetch/export new or modified emails
- Update existing consolidated documents
- Merge mode for incremental updates
- Export history with timestamps

**Implementation Details:**
- Enhance `history.py` to track export state
- Add last-export timestamp to config
- Implement merge logic in `converter.py`
- Add `--merge-with` flag to CLI

**Example Workflow:**
```bash
# First export
g2n --label "Inbox" --consolidate --consolidation-filename "emails.md"

# Week later - only new emails added
g2n --label "Inbox" --consolidate --merge-with "emails.md"
```

**Files to Modify:**
- `gmail_to_notebooklm/history.py`
- `gmail_to_notebooklm/core.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/main.py`

---

### 3.3 🟢 Export Format Options ⏱️ High 📅 v1.2.0

**Goal:** Support multiple output formats

**Features:**
- Multiple output formats: Markdown, JSON, CSV, HTML
- Custom template system for email formatting
- YAML frontmatter vs inline metadata options
- Format-specific optimizations

**Supported Formats:**
- **Markdown** (current) - Plain markdown with YAML frontmatter
- **Markdown Pro** - With metadata, threading, labels
- **JSON** - Machine-readable, preserves all metadata
- **CSV** - Spreadsheet-compatible, one row per email
- **HTML** - Self-contained, browser-viewable
- **Custom Templates** - Jinja2-based user templates

**Implementation Details:**
- Create `exporters/` directory with format-specific classes
- Add template engine (Jinja2)
- Update CLI with `--output-format` flag
- Update `core.py` to delegate to format exporters

**Files to Modify:**
- Create `gmail_to_notebooklm/exporters/` directory
- Create format exporter classes
- `gmail_to_notebooklm/core.py`
- `gmail_to_notebooklm/main.py`

---

## Phase 4: Power Features (v1.3.0 - v1.5.0)

**Focus:** Automation, integration, and intelligence
**Timeline:** Q3 2026 - Q4 2026+
**Status:** Future

### 4.1 🟢 Scheduled Exports ⏱️ High 📅 v1.3.0

**Goal:** Automated export jobs

**Features:**
- Cron-style scheduling (daily, weekly, monthly)
- Email delivery of export results
- Auto-backup to cloud storage (AWS S3, Google Drive)
- Scheduled update of incremental exports
- Job history and status monitoring

**Implementation Details:**
- Add job scheduler (APScheduler)
- Create `scheduler.py` module
- Email sender integration
- Cloud storage drivers

**Example Config:**
```yaml
scheduled_exports:
  - name: "Weekly Inbox"
    label: "Inbox"
    frequency: "weekly"  # daily, weekly, monthly
    day_of_week: "Sunday"
    time: "22:00"
    consolidate: true
    email_to: "user@example.com"
    upload_to: "s3://my-bucket/emails/"
```

**Files to Modify:**
- Create `gmail_to_notebooklm/scheduler.py`
- `gmail_to_notebooklm/config.py`
- `gmail_to_notebooklm/main.py` (daemon mode)

---

### 4.2 🟢 AI-Powered Features ⏱️ High 📅 v1.4.0

**Goal:** Intelligent content processing

**Features:**
- Email summarization (using Claude API)
- Auto-tagging and categorization
- Key points extraction from conversations
- Sentiment analysis
- Action item extraction

**Implementation Details:**
- Add `ai_processor.py` module
- Claude API integration
- Caching of AI results
- Optional feature (requires API key)

**Example Output:**
```markdown
## Project Kickoff {#email-project-kickoff-xyz}

**AI Summary:** Project kickoff meeting scheduled for Jan 15.
Team leads need to prepare resource plans.

**Key Points:**
- Budget approved for Q1
- Timeline: Jan 15 - Mar 31
- Action items assigned to team leads

**Sentiment:** Positive

**Action Items:**
- [ ] Prepare resource plan (assigned to Dev Lead)
- [ ] Review budget allocation (assigned to Finance)
```

**Configuration:**
```bash
g2n --label "Inbox" --consolidate --enable-ai-features --openai-api-key "sk-..."
```

**Files to Modify:**
- Create `gmail_to_notebooklm/ai_processor.py`
- `gmail_to_notebooklm/converter.py`
- `gmail_to_notebooklm/config.py`
- `gmail_to_notebooklm/main.py`

---

### 4.3 🟢 Direct NotebookLM Integration ⏱️ High 📅 v1.4.0

**Goal:** Seamless NotebookLM workflow

**Features:**
- API connection to NotebookLM (if available)
- One-click upload to existing notebook
- Automatic notebook creation with sources
- Notebook management UI

**Workflow:**
```
Gmail Emails → Export → Upload to NotebookLM → Generate Q&A
```

**Implementation Details:**
- Add NotebookLM API client
- OAuth flow for NotebookLM auth
- Notebook manager UI
- Auto-refresh integration

**Files to Modify:**
- Create `gmail_to_notebooklm/notebooklm_client.py`
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/core.py`

---

### 4.4 🟢 Multi-Account Support ⏱️ High 📅 v1.5.0

**Goal:** Work with multiple Gmail accounts

**Features:**
- Switch between multiple Gmail accounts
- Export from multiple accounts to single document
- Account-based organization in output
- Account-specific profiles and history

**Implementation Details:**
- Store multiple credential sets
- Account selector in GUI
- Multi-account export orchestration
- Output structure: `emails-account1.md`, `emails-account2.md` or merged

**Files to Modify:**
- `gmail_to_notebooklm/auth.py`
- `gmail_to_notebooklm/config.py`
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/core.py`

---

## Phase 5: Polish & UX (Throughout All Phases)

### Documentation 🟡

**Timeline:** Ongoing throughout development

**Deliverables:**
- In-app video tutorials (feature highlights)
- Interactive tooltips for all controls
- Example outputs for each feature
- Troubleshooting guide expansion
- API documentation for developers

**Files to Create/Modify:**
- Create `docs/TUTORIALS.md`
- Create `docs/EXAMPLES/` directory
- Update all documentation files
- Create video scripts

---

### GUI Improvements 🟡

**Timeline:** Ongoing throughout development

**Planned Enhancements:**
- Drag-and-drop output directory selection
- Export preview (show first email before saving)
- Real-time character count in consolidated doc
- Dark mode toggle
- Keyboard shortcuts for common actions
- Screen reader support (accessibility)
- High contrast mode

**Files to Modify:**
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/gui/app.py` (theme management)

---

### Analytics Dashboard 🟡

**Timeline:** v1.1.0

**Features:**
- Export size estimates before running
- Stats dashboard: email count by sender, domain, date range
- Conversion statistics (HTML vs plaintext, attachments, etc.)
- Export history visualization
- Storage usage over time

**Files to Modify:**
- Create `gmail_to_notebooklm/gui/windows/analytics_dialog.py`
- `gmail_to_notebooklm/gui/windows/main_window.py`
- `gmail_to_notebooklm/utils.py` (stats generation)

---

## Release Timeline Summary

| Version | Phase | Target | Key Features |
|---------|-------|--------|--------------|
| **0.8.0** | 1 | Q4 2025 | Attachments, Threading, Error Handling |
| **0.9.0** | 1 | Q1 2026 | Performance Optimization |
| **1.0.0** | 2 | Q2 2026 | Advanced Search, Profiles, Metadata, Labels |
| **1.1.0** | 3 | Q2 2026 | Deduplication, Incremental, Analytics |
| **1.2.0** | 3 | Q3 2026 | Format Options |
| **1.3.0** | 4 | Q3 2026 | Scheduled Exports |
| **1.4.0** | 4 | Q4 2026 | AI Features, NotebookLM Integration |
| **1.5.0** | 4 | Q4 2026+ | Multi-Account Support, Polish |

---

## Implementation Priority Matrix

```
Effort
  ↑
  │  3.2              4.2,4.3   4.4
  │  Threading  AI    NotebookLM Multi
  │
H │  1.2        2.3   2.2
  │  Attach Search  Advanced Format
  │
  │  1.3  2.1        3.1     3.3
M │  Errors Search  Dedup   Formats
  │
  │  2.4        1.4       4.1
L │  Labels  Perf  Schedule
  │
  └──────────────────────────→
     Low    Medium    High
     Impact/Value
```

---

## Dependency Management

### New External Dependencies by Phase

**Phase 1:**
- None (use stdlib)

**Phase 2:**
- None (use stdlib and existing deps)

**Phase 3:**
- `jinja2` (templates) - already optional
- `apscheduler` (scheduling) - Phase 4.1

**Phase 4:**
- `openai` (AI features) - optional, conditional import
- `boto3` (AWS) - optional, conditional import
- `google-auth-httplib2` (already have)

---

## Success Metrics

### Phase 1 (Foundation)
- [ ] 0 critical bugs in attachment handling
- [ ] Parallel fetching reduces 100+ email export time by 50%
- [ ] Email threading improves user comprehension (survey)

### Phase 2 (Search)
- [ ] Filter UI reduces export time by 30% (avoid unwanted emails)
- [ ] 80%+ users save and reuse at least one profile
- [ ] Advanced metadata increases NotebookLM analysis quality

### Phase 3 (Advanced)
- [ ] Incremental exports reduce storage by 40%
- [ ] Deduplication reduces consolidated doc size by 20%+
- [ ] Format options support 5+ use cases

### Phase 4 (Power)
- [ ] Scheduled exports enable "set and forget" backup
- [ ] AI summaries save users 30% reading time
- [ ] NotebookLM integration becomes primary workflow

---

## Contributing Guidelines

Developers interested in implementing features from this roadmap should:

1. Open an issue referencing the roadmap item
2. Create a feature branch: `feature/item-name`
3. Follow existing code patterns
4. Add comprehensive tests
5. Update documentation
6. Submit PR for review

---

## Feedback & Adjustments

This roadmap is a living document. Community feedback shapes priorities:

- **Request a feature?** Open a GitHub issue with tag `enhancement`
- **Have bandwidth to contribute?** See Contributing Guidelines above
- **Find a blocker?** Open an issue with tag `blocked`

---

**Last Review:** November 13, 2025
**Next Review:** January 2026
**Owner:** Paul Deegan
