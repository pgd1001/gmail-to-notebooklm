# Phase 1 Feature Issues - Gmail to NotebookLM

Use this file to create GitHub issues for Phase 1 features. Copy each section as a new issue.

---

## Issue 1: Add Rich progress bars for better user experience

**Labels**: `enhancement`, `user-experience`, `phase-1`, `priority:p1`

### Description
Replace current `print()` progress indicators with Rich library progress bars showing visual feedback during email fetching, parsing, and conversion.

### Benefits
- Professional, modern UX
- Real-time progress with percentage, ETA, and speed
- Better visual feedback for long-running operations

### Implementation
- [x] Install Rich library (already done)
- [ ] Update `gmail_client.py`: Add progress bar for fetching emails
- [ ] Update `parser.py`: Add progress bar for parsing emails
- [ ] Update `converter.py`: Add progress bar for converting to Markdown
- [ ] Add spinners for API calls

### Files to Modify
- `gmail_to_notebooklm/gmail_client.py`
- `gmail_to_notebooklm/parser.py`
- `gmail_to_notebooklm/converter.py`

### Estimated Effort
Low (1-2 hours)

### Priority
**P1 - Quick Win**

---

## Issue 2: Add YAML configuration file support

**Labels**: `enhancement`, `configuration`, `phase-1`, `priority:p1`

### Description
Add support for loading settings from `.gmail-to-notebooklm.yaml` configuration file to avoid repetitive CLI arguments.

### Benefits
- Save frequently used settings
- Share configurations across team
- Easier to manage complex setups

### Implementation
- [x] Install PyYAML library (already done)
- [ ] Create `config.py` module for loading YAML files
- [ ] Add `--config` CLI parameter for custom config path
- [ ] Look for `.gmail-to-notebooklm.yaml` in current directory by default
- [ ] CLI arguments override config file settings
- [ ] Add config validation

### Files to Create
- `gmail_to_notebooklm/config.py` (new)

### Files to Modify
- `gmail_to_notebooklm/main.py` (add --config parameter)

### Sample Config
```yaml
label: "Client A"
output_dir: "./exports"
max_results: 1000
organize_by_date: true
create_index: true
```

### Estimated Effort
Low (2-3 hours)

### Priority
**P1 - Quick Win**

---

## Issue 3: Add date range filtering (--after, --before)

**Labels**: `enhancement`, `filtering`, `phase-1`, `priority:p1`

### Description
Add `--after` and `--before` parameters to filter emails by date range with user-friendly YYYY-MM-DD format.

### Benefits
- Essential filtering capability
- Process specific time periods
- Faster exports of recent emails

### Implementation
- [ ] Add `--after` parameter accepting YYYY-MM-DD format
- [ ] Add `--before` parameter accepting YYYY-MM-DD format
- [ ] Convert dates to Gmail query syntax (`after:` and `before:`)
- [ ] Integrate with existing query building in `gmail_client.py`
- [ ] Add date validation
- [ ] Add tests for date parsing

### Example Usage
```bash
gmail-to-notebooklm --label "INBOX" --after 2024-01-01 --before 2024-12-31
```

### Files to Modify
- `gmail_to_notebooklm/main.py` (add CLI parameters)
- `gmail_to_notebooklm/gmail_client.py` (update query building)
- `tests/test_gmail_client.py` (add tests)

### Estimated Effort
Low (2-3 hours)

### Priority
**P1 - High Value**

---

## Issue 4: Add sender/recipient filtering

**Labels**: `enhancement`, `filtering`, `phase-1`, `priority:p1`

### Description
Add `--from`, `--to`, and `--exclude-from` parameters to filter emails by sender or recipient.

### Benefits
- Target specific correspondents
- Exclude automated/unwanted senders
- More precise email selection

### Implementation
- [ ] Add `--from` parameter (can be repeated or comma-separated)
- [ ] Add `--to` parameter
- [ ] Add `--exclude-from` parameter for negative filtering
- [ ] Convert to Gmail query syntax (`from:`, `to:`, `-from:`)
- [ ] Support multiple values
- [ ] Add tests

### Example Usage
```bash
# Get emails from specific sender
gmail-to-notebooklm --label "INBOX" --from "client@example.com"

# Exclude automated emails
gmail-to-notebooklm --label "INBOX" --exclude-from "noreply@,automated@"

# Multiple senders
gmail-to-notebooklm --label "INBOX" --from "john@example.com,jane@example.com"
```

### Files to Modify
- `gmail_to_notebooklm/main.py` (add CLI parameters)
- `gmail_to_notebooklm/gmail_client.py` (update query building)
- `tests/test_gmail_client.py` (add tests)

### Estimated Effort
Low (2-3 hours)

### Priority
**P1 - High Value**

---

## Issue 5: Add Gmail query syntax support (--query)

**Labels**: `enhancement`, `filtering`, `phase-1`, `priority:p0`

### Description
Add `--query` parameter to support Gmail's full advanced search syntax, unlocking powerful search capabilities beyond labels.

### Benefits
- Full Gmail search power (subject:, has:attachment, filename:, etc.)
- Replace multiple individual filter parameters
- Most flexible filtering option
- Can be used with or without `--label`

### Implementation
- [ ] Add `--query` CLI parameter
- [ ] Pass query directly to Gmail API `users.messages.list(q=query)`
- [ ] Make `--label` optional when `--query` is provided
- [ ] Combine `--query` with `--label` if both provided
- [ ] Update documentation with Gmail search operators
- [ ] Add examples

### Supported Gmail Search Operators
- `from:` - Filter by sender
- `to:` - Filter by recipient
- `subject:` - Filter by subject text
- `before:` / `after:` - Date filtering
- `has:attachment` - Has attachments
- `filename:` - Specific attachment filename
- `is:starred` / `is:important` - Special flags
- `in:` - In specific folder/label
- Logical operators: `OR`, `-` (NOT), `()` grouping

### Example Usage
```bash
# Complex query
gmail-to-notebooklm --query "from:client@example.com subject:invoice after:2024/01/01 has:attachment"

# Without label (search all mail)
gmail-to-notebooklm --query "from:important@client.com" --output-dir "./important"

# Combined with label
gmail-to-notebooklm --label "Clients" --query "has:attachment" --output-dir "./client_attachments"
```

### Files to Modify
- `gmail_to_notebooklm/main.py` (add --query parameter, make --label optional)
- `gmail_to_notebooklm/gmail_client.py` (accept query parameter in list_messages)
- `tests/test_gmail_client.py` (add query tests)
- `USAGE.md` (document Gmail search syntax)

### Estimated Effort
Medium (3-4 hours)

### Priority
**P0 - Critical Enhancement** (Unlocks major functionality)

---

## Issue 6: Add index file generation (--create-index)

**Labels**: `enhancement`, `output`, `phase-1`, `priority:p1`

### Description
Generate an `INDEX.md` file with a table of contents listing all exported emails with metadata and links.

### Benefits
- Easy navigation of exports
- Quick overview of exported content
- Professional presentation

### Implementation
- [ ] Add `--create-index` CLI flag
- [ ] Create index generation function in `utils.py`
- [ ] Generate Markdown table with: Subject, From, Date, Filename
- [ ] Add relative links to individual email files
- [ ] Support HTML index as alternative format
- [ ] Add tests

### Example Output (INDEX.md)
```markdown
# Email Export Index

**Label**: Client A
**Export Date**: 2024-01-15 10:30:00
**Total Emails**: 42

| Subject | From | Date | File |
|---------|------|------|------|
| Project Update | john@example.com | 2024-01-15 | [Link](Project_Update_abc123.md) |
| Meeting Notes | jane@example.com | 2024-01-14 | [Link](Meeting_Notes_def456.md) |
| ... | ... | ... | ... |
```

### Files to Modify
- `gmail_to_notebooklm/utils.py` (add index generation function)
- `gmail_to_notebooklm/main.py` (add --create-index flag, call generator)
- `tests/test_utils.py` (add index generation tests)

### Estimated Effort
Low (2-3 hours)

### Priority
**P1 - High Value**

---

## Issue 7: Add date-based organization (--organize-by-date)

**Labels**: `enhancement`, `output`, `phase-1`, `priority:p1`

### Description
Add `--organize-by-date` flag to automatically organize exported emails into subdirectories by year/month/day.

### Benefits
- Logical file organization
- Easier to find emails by date
- Cleaner output directory

### Implementation
- [ ] Add `--organize-by-date` CLI flag
- [ ] Add `--date-format` parameter for customizing structure
- [ ] Create subdirectory structure based on email date
- [ ] Support formats: `YYYY/MM`, `YYYY-MM`, `YYYY/MM/DD`, `YYYY-MM-DD`
- [ ] Update file writing logic in `utils.py`
- [ ] Add tests

### Example Directory Structure
```
output/
├── 2024/
│   ├── 01/
│   │   ├── Email_1_abc123.md
│   │   └── Email_2_def456.md
│   └── 02/
│       └── Email_3_ghi789.md
└── INDEX.md
```

### Example Usage
```bash
# Organize by year/month
gmail-to-notebooklm --label "INBOX" --organize-by-date --date-format "YYYY/MM"

# Organize by year-month (flat)
gmail-to-notebooklm --label "INBOX" --organize-by-date --date-format "YYYY-MM"

# Organize by full date
gmail-to-notebooklm --label "INBOX" --organize-by-date --date-format "YYYY/MM/DD"
```

### Files to Modify
- `gmail_to_notebooklm/main.py` (add CLI parameters)
- `gmail_to_notebooklm/utils.py` (update write_markdown_file for date-based paths)
- `tests/test_utils.py` (add tests)

### Estimated Effort
Low (2-3 hours)

### Priority
**P1 - High Value**

---

## Issue 8: Update tests for Phase 1 features

**Labels**: `testing`, `phase-1`, `priority:p1`

### Description
Add comprehensive tests for all new Phase 1 features to maintain code quality and coverage.

### Test Coverage Needed
- [ ] Rich progress bar integration (mock Rich objects)
- [ ] YAML configuration loading and validation
- [ ] Date range filtering (date parsing, query building)
- [ ] Sender/recipient filtering (query building)
- [ ] Gmail query syntax (query parameter handling)
- [ ] Index file generation (content, format, links)
- [ ] Date-based organization (directory structure)

### Target Coverage
- Maintain or improve current 52% coverage
- Aim for 80%+ on new code
- Focus on critical paths and error handling

### Files to Create/Modify
- `tests/test_config.py` (new - for YAML config)
- `tests/test_gmail_client.py` (update - for query building)
- `tests/test_utils.py` (update - for index and date organization)
- `tests/test_main.py` (new - for CLI integration)

### Estimated Effort
Medium (4-6 hours)

### Priority
**P1 - Essential for Quality**

---

## Issue 9: Update documentation for Phase 1 features

**Labels**: `documentation`, `phase-1`, `priority:p1`

### Description
Update all documentation files to reflect Phase 1 features and new capabilities.

### Documentation Updates Needed
- [ ] **USAGE.md**: Add examples for all new CLI parameters
- [ ] **CONFIGURATION.md**: Document YAML config file format and all options
- [ ] **QUICKSTART.md**: Update with simplified config file approach
- [ ] **README.md**: Update features list and examples
- [ ] **CHANGELOG.md**: Add v0.2.0 section with Phase 1 features
- [ ] **CLAUDE.md**: Update with new architecture details

### New Content
- Gmail query syntax guide with examples
- YAML configuration file examples
- Date filtering examples
- Index file example output
- Date-based organization examples

### Files to Modify
- `USAGE.md`
- `CONFIGURATION.md`
- `QUICKSTART.md`
- `README.md`
- `CHANGELOG.md`
- `CLAUDE.md`

### Estimated Effort
Low (2-3 hours)

### Priority
**P1 - User Experience**

---

## Phase 1 Summary

**Total Issues**: 9
**Estimated Total Effort**: 18-28 hours
**Priority Breakdown**:
- P0 (Critical): 1 issue
- P1 (High): 8 issues

**Quick Wins** (Low effort, high value):
1. Rich progress bars (1-2 hours)
2. YAML config support (2-3 hours)
3. Date range filtering (2-3 hours)
4. Index file generation (2-3 hours)

**Dependencies**:
- Issue #5 (Gmail query) should be implemented before issues #3 and #4 (date/sender filtering) for cleaner code
- Issue #8 (tests) should follow feature implementation
- Issue #9 (docs) should be last

**Recommended Order**:
1. Issue #2 - YAML config (foundation)
2. Issue #5 - Gmail query syntax (core feature)
3. Issue #3 - Date filtering
4. Issue #4 - Sender filtering
5. Issue #1 - Rich progress bars
6. Issue #6 - Index generation
7. Issue #7 - Date organization
8. Issue #8 - Tests
9. Issue #9 - Documentation
