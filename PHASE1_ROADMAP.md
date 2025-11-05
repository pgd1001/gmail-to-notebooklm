# Phase 1 Development Roadmap

**Branch**: `feature/phase1-enhancements`
**Target**: v0.2.0
**Status**: In Progress

## 📋 Issues Created

All 9 issues created on GitHub:
- [Issue #1](https://github.com/pgd1001/gmail-to-notebooklm/issues/1) - 🎯 P0: Gmail query syntax
- [Issue #2](https://github.com/pgd1001/gmail-to-notebooklm/issues/2) - 📝 P1: YAML config support
- [Issue #3](https://github.com/pgd1001/gmail-to-notebooklm/issues/3) - 📅 P1: Date range filtering
- [Issue #4](https://github.com/pgd1001/gmail-to-notebooklm/issues/4) - 👤 P1: Sender/recipient filtering
- [Issue #5](https://github.com/pgd1001/gmail-to-notebooklm/issues/5) - 🎨 P1: Rich progress bars
- [Issue #6](https://github.com/pgd1001/gmail-to-notebooklm/issues/6) - 📋 P1: Index file generation
- [Issue #7](https://github.com/pgd1001/gmail-to-notebooklm/issues/7) - 📁 P1: Date-based organization
- [Issue #8](https://github.com/pgd1001/gmail-to-notebooklm/issues/8) - 🧪 P1: Tests
- [Issue #9](https://github.com/pgd1001/gmail-to-notebooklm/issues/9) - 📚 P1: Documentation

## 🎯 Development Order (Recommended)

### Sprint 1: Foundation (6-9 hours)
- [ ] **Issue #2** - YAML Configuration Support (2-3h)
  - Create `config.py` module
  - Add config loading and validation
  - Update `main.py` to accept `--config` parameter
  - Test with sample config file

- [ ] **Issue #1** - Gmail Query Syntax Support (3-4h) ⭐ CRITICAL
  - Update `gmail_client.py` to accept query parameter
  - Make `--label` optional in `main.py`
  - Add `--query` CLI parameter
  - Combine query with label if both provided
  - Add query building helper functions

### Sprint 2: Filtering Features (4-6 hours)
- [ ] **Issue #3** - Date Range Filtering (2-3h)
  - Add `--after` and `--before` parameters
  - Convert dates to Gmail query format
  - Add date validation
  - Integrate with query builder

- [ ] **Issue #4** - Sender/Recipient Filtering (2-3h)
  - Add `--from`, `--to`, `--exclude-from` parameters
  - Support multiple values (comma-separated)
  - Convert to Gmail query format
  - Integrate with query builder

### Sprint 3: Output Enhancements (4-6 hours)
- [ ] **Issue #6** - Index File Generation (2-3h)
  - Create index generation function in `utils.py`
  - Add `--create-index` flag to CLI
  - Generate Markdown table with links
  - Add to export workflow

- [ ] **Issue #7** - Date-Based Organization (2-3h)
  - Add `--organize-by-date` flag
  - Add `--date-format` parameter
  - Update `write_markdown_file` to support subdirectories
  - Create directory structure based on date

### Sprint 4: User Experience (1-2 hours)
- [ ] **Issue #5** - Rich Progress Bars (1-2h)
  - Update `gmail_client.py` with Rich progress
  - Update `parser.py` with Rich progress
  - Update `converter.py` with Rich progress
  - Add spinners for API calls
  - Test on Windows console

### Sprint 5: Quality Assurance (6-9 hours)
- [ ] **Issue #8** - Tests for New Features (4-6h)
  - Add config loading tests
  - Add query building tests
  - Add date filtering tests
  - Add sender filtering tests
  - Add index generation tests
  - Add date organization tests
  - Target 80%+ coverage on new code

- [ ] **Issue #9** - Documentation Updates (2-3h)
  - Update USAGE.md with new examples
  - Update CONFIGURATION.md with YAML format
  - Update QUICKSTART.md
  - Update README.md features list
  - Add CHANGELOG.md v0.2.0 entry
  - Update CLAUDE.md

## 📊 Progress Tracker

### Completed ✅
- [x] Dependencies added (Rich, PyYAML)
- [x] GitHub issues created
- [x] Feature branch created
- [x] Roadmap documented

### In Progress 🚧
- [ ] Sprint 1: Foundation
- [ ] Sprint 2: Filtering
- [ ] Sprint 3: Output
- [ ] Sprint 4: UX
- [ ] Sprint 5: QA

### Blocked ⛔
- None

## 🔄 Workflow

### Development Cycle
1. Pick an issue from the roadmap
2. Create a commit referencing the issue: `git commit -m "feat: add feature (#N)"`
3. Test the feature locally
4. Update tests
5. Move to next issue
6. Repeat until sprint complete

### Testing Before Merge
```bash
# Run all tests
pytest tests/ -v --cov=gmail_to_notebooklm

# Run linting
flake8 gmail_to_notebooklm tests

# Format code
black gmail_to_notebooklm tests
isort gmail_to_notebooklm tests

# Test CLI
python -m gmail_to_notebooklm.main --help
```

### Merge to Main
```bash
# When Phase 1 complete:
git checkout main
git merge feature/phase1-enhancements
git tag v0.2.0
git push origin main --tags
```

## 📝 Commit Message Convention

Use conventional commits format:

```
feat(module): add new feature (#issue)
fix(module): fix bug (#issue)
docs: update documentation (#issue)
test: add tests for feature (#issue)
chore: update dependencies
```

Examples:
```
feat(config): add YAML configuration support (#2)
feat(query): add Gmail query syntax support (#1)
feat(utils): add index file generation (#6)
test(config): add config loading tests (#8)
docs(usage): add Gmail query examples (#9)
```

## 🎯 Definition of Done

A feature is complete when:
- [ ] Code implemented and working
- [ ] Tests added with good coverage
- [ ] Documentation updated
- [ ] Manual testing passed
- [ ] Code formatted (black, isort)
- [ ] Linting passed (flake8)
- [ ] Committed with proper message
- [ ] GitHub issue updated/closed

## 🚀 Release Checklist (v0.2.0)

Before merging to main:
- [ ] All 9 issues resolved
- [ ] Test coverage ≥ 52% (maintain or improve)
- [ ] All tests passing
- [ ] Documentation complete
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `pyproject.toml` and `__init__.py`
- [ ] Manual testing on Windows
- [ ] README.md updated with new features

## 📈 Estimated Timeline

- **Sprint 1**: 2-3 days
- **Sprint 2**: 1-2 days
- **Sprint 3**: 1-2 days
- **Sprint 4**: 0.5-1 day
- **Sprint 5**: 2-3 days

**Total**: 6-11 days (1-2 weeks)

## 🔗 Quick Links

- **Repository**: https://github.com/pgd1001/gmail-to-notebooklm
- **Issues**: https://github.com/pgd1001/gmail-to-notebooklm/issues
- **Branch**: `feature/phase1-enhancements`
- **Documentation**: See `PHASE1_ISSUES.md` for detailed issue descriptions

## 💡 Tips

1. **Start with foundational features** (#2, #1) - they enable others
2. **Test incrementally** - don't wait until the end
3. **Commit frequently** - small, focused commits
4. **Update docs as you go** - easier than batch at end
5. **Use GitHub issue references** - helps track progress

## 🆘 Getting Help

If stuck:
1. Check `PHASE1_ISSUES.md` for detailed implementation notes
2. Review existing code patterns in the repo
3. Check Gmail API documentation
4. Ask for clarification on specific issues

---

**Last Updated**: 2024-11-05
**Status**: Ready to begin Sprint 1
