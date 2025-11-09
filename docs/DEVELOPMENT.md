# Development Guide

Guide for developers contributing to the Gmail to NotebookLM converter.

## Table of Contents

- [Setup Development Environment](#setup-development-environment)
- [Project Structure](#project-structure)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Building and Packaging](#building-and-packaging)
- [Contributing Guidelines](#contributing-guidelines)

## Setup Development Environment

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment (recommended)

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/gmail-to-notebooklm.git
cd gmail-to-notebooklm

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Development Dependencies

The `[dev]` extra installs:

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatter
- **flake8** - Linter
- **isort** - Import sorter
- **mypy** - Type checker
- **pre-commit** - Git hooks

## Project Structure

```
gmail-to-notebooklm/
├── gmail_to_notebooklm/          # Main package
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # CLI entry point
│   ├── auth.py                   # OAuth authentication
│   ├── gmail_client.py           # Gmail API client
│   ├── parser.py                 # Email MIME parsing
│   ├── converter.py              # HTML to Markdown conversion
│   └── utils.py                  # Utility functions
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_gmail_client.py
│   ├── test_parser.py
│   ├── test_converter.py
│   ├── conftest.py              # Pytest fixtures
│   └── fixtures/                # Test data
├── examples/                     # Example files
├── docs/                        # Additional documentation
├── .github/                     # GitHub-specific files
│   └── workflows/              # CI/CD workflows
├── requirements.txt             # Production dependencies
├── pyproject.toml              # Package configuration
├── setup.py                    # Setup script
├── MANIFEST.in                 # Package manifest
├── README.md                   # Project overview
├── CHANGELOG.md                # Version history
└── LICENSE                     # License file
```

## Code Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length**: 88 characters (Black default)
- **Imports**: Sorted with isort
- **Docstrings**: Google style
- **Type hints**: Use for all public functions

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Format and sort in one command
black . && isort .
```

### Linting

```bash
# Run flake8
flake8 gmail_to_notebooklm tests

# Run mypy type checking
mypy gmail_to_notebooklm
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`:

```bash
# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

Configured hooks:
- trailing-whitespace removal
- end-of-file-fixer
- check-yaml
- black
- isort
- flake8
- mypy

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gmail_to_notebooklm

# Run specific test file
pytest tests/test_parser.py

# Run specific test
pytest tests/test_parser.py::test_parse_email_headers

# Run with verbose output
pytest -v

# Run and open coverage HTML report
pytest --cov=gmail_to_notebooklm --cov-report=html
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Test Structure

```python
# tests/test_example.py

import pytest
from gmail_to_notebooklm import example_module


class TestExampleFunction:
    """Tests for example_function."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = example_module.example_function("input")
        assert result == "expected_output"

    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            example_module.example_function(None)

    @pytest.mark.parametrize("input,expected", [
        ("test1", "result1"),
        ("test2", "result2"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple input cases."""
        assert example_module.example_function(input) == expected
```

### Test Fixtures

Define reusable test data in `tests/conftest.py`:

```python
import pytest


@pytest.fixture
def sample_email():
    """Sample email for testing."""
    return {
        "id": "12345",
        "subject": "Test Email",
        "from": "test@example.com",
        "body": "<p>Test content</p>",
    }


@pytest.fixture
def mock_gmail_service(mocker):
    """Mock Gmail API service."""
    return mocker.Mock()
```

### Mocking Gmail API

Use `pytest-mock` for Gmail API mocking:

```python
def test_fetch_emails(mocker, mock_gmail_service):
    """Test fetching emails from Gmail."""
    # Mock the API response
    mock_gmail_service.users().messages().list().execute.return_value = {
        "messages": [{"id": "123"}, {"id": "456"}]
    }

    # Test your function
    result = fetch_emails(mock_gmail_service, "Test Label")
    assert len(result) == 2
```

## Building and Packaging

### Local Build

```bash
# Build source distribution and wheel
python -m build

# Output in dist/
# - gmail-to-notebooklm-0.1.0.tar.gz
# - gmail_to_notebooklm-0.1.0-py3-none-any.whl
```

### Install from Local Build

```bash
# Install wheel
pip install dist/gmail_to_notebooklm-0.1.0-py3-none-any.whl

# Install in editable mode (for development)
pip install -e .
```

### Publishing to PyPI

```bash
# Install twine
pip install twine

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Contributing Guidelines

### Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

4. **Run tests and checks**
   ```bash
   pytest
   black .
   isort .
   flake8
   mypy gmail_to_notebooklm
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "Add your feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to GitHub
   - Open a Pull Request from your branch
   - Describe your changes

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Examples**:
```
feat(parser): add support for nested MIME parts
fix(auth): handle expired token refresh
docs(readme): update installation instructions
test(converter): add tests for HTML entity decoding
```

### Pull Request Guidelines

**Before submitting**:
- [ ] Tests pass: `pytest`
- [ ] Code formatted: `black .`
- [ ] Imports sorted: `isort .`
- [ ] Linting passes: `flake8`
- [ ] Type checking passes: `mypy`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

**PR Description should include**:
- What changed
- Why it changed
- How to test it
- Related issues

### Code Review Process

1. **Automated checks**: CI runs tests, linting, type checking
2. **Peer review**: At least one maintainer reviews
3. **Feedback**: Address review comments
4. **Approval**: Maintainer approves PR
5. **Merge**: Squash and merge to main

## Module Development

### Adding a New Module

1. **Create module file**
   ```bash
   touch gmail_to_notebooklm/new_module.py
   ```

2. **Write module code**
   ```python
   """Module for doing something."""

   from typing import List


   def new_function(param: str) -> List[str]:
       """
       Do something useful.

       Args:
           param: Input parameter

       Returns:
           List of results

       Raises:
           ValueError: If param is invalid
       """
       if not param:
           raise ValueError("param cannot be empty")

       return [param.upper()]
   ```

3. **Create tests**
   ```bash
   touch tests/test_new_module.py
   ```

4. **Write tests**
   ```python
   import pytest
   from gmail_to_notebooklm.new_module import new_function


   def test_new_function():
       """Test new_function."""
       result = new_function("test")
       assert result == ["TEST"]


   def test_new_function_error():
       """Test error handling."""
       with pytest.raises(ValueError):
           new_function("")
   ```

5. **Update documentation**
   - Add to README.md if user-facing
   - Document in docstrings
   - Update CHANGELOG.md

### Implementing Core Components

#### Authentication Module (auth.py)

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate(credentials_path: str, token_path: str) -> Credentials:
    """Authenticate with Gmail API using OAuth 2.0."""
    # Implementation here
    pass
```

#### Gmail Client (gmail_client.py)

```python
from googleapiclient.discovery import build


class GmailClient:
    """Client for interacting with Gmail API."""

    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def list_messages(self, label: str) -> List[str]:
        """List message IDs for a label."""
        # Implementation here
        pass

    def get_message(self, message_id: str) -> dict:
        """Get full message content."""
        # Implementation here
        pass
```

#### Email Parser (parser.py)

```python
from email.mime.text import MIMEText
from typing import Dict


def parse_email(raw_email: dict) -> Dict[str, str]:
    """Parse Gmail API message into structured format."""
    # Implementation here
    pass
```

#### Markdown Converter (converter.py)

```python
from html2text import HTML2Text


def convert_to_markdown(email_data: Dict[str, str]) -> str:
    """Convert email to Markdown format with headers."""
    # Implementation here
    pass
```

## Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Use Python Debugger

```python
import pdb

def problematic_function():
    x = some_calculation()
    pdb.set_trace()  # Debugger stops here
    return x
```

### VS Code Debug Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Gmail to NotebookLM",
            "type": "python",
            "request": "launch",
            "module": "gmail_to_notebooklm.main",
            "args": ["--label", "Test", "--output-dir", "./test_output"],
            "console": "integratedTerminal"
        }
    ]
}
```

## Performance Profiling

```python
import cProfile
import pstats

# Profile a function
cProfile.run('main()', 'output.prof')

# Analyze results
p = pstats.Stats('output.prof')
p.sort_stats('cumulative').print_stats(10)
```

## Documentation

### Docstring Format

Use Google style:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not int

    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Updating Documentation

When making changes:
1. Update docstrings in code
2. Update relevant .md files
3. Update CHANGELOG.md
4. Update README.md if user-facing

## Troubleshooting Development Issues

### "Import error" when running tests

```bash
# Install package in editable mode
pip install -e .
```

### "Pre-commit hook failed"

```bash
# Run formatters manually
black .
isort .

# Then commit
git commit
```

### "Type checking failed"

```bash
# Run mypy to see errors
mypy gmail_to_notebooklm

# Add type ignore if needed (use sparingly)
result = problematic_line()  # type: ignore
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Style](https://black.readthedocs.io/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Gmail API Documentation](https://developers.google.com/gmail/api)

## Getting Help

- **Questions**: Open a Discussion on GitHub
- **Bugs**: Create an Issue with reproduction steps
- **Features**: Propose in Discussions before implementing
- **Code Review**: Tag maintainers in PR

---

Thank you for contributing to Gmail to NotebookLM converter!
