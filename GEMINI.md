# GEMINI.md

## Project Overview

This project is a Python-based tool to convert emails from a specific Gmail label into Markdown files. These files are formatted for use as sources in Google NotebookLM, including email headers for better context.

**Key Technologies:**

*   Python
*   Google API Client for Python
*   BeautifulSoup4
*   html2text (or a similar HTML to Markdown conversion library)

## Building and Running

**1. Installation:**

It is assumed that the project uses a `requirements.txt` file for dependencies.

```bash
pip install -r requirements.txt
```

**2. Authentication:**

The tool uses OAuth 2.0 to access Gmail. You will need to have `credentials.json` from Google Cloud Platform in the root directory. The first time you run the tool, it will likely open a browser window to authorize access.

**3. Running the tool:**

A main script, possibly named `main.py` or `gmail_to_notebooklm.py`, is expected to be the entry point.

```bash
# Example of how the tool might be run
python main.py --label "Client A" --output-dir "output"
```

*TODO: Verify the exact command to run the tool and the available arguments.*

## Development Conventions

*   The code should be modular and well-structured.
*   Follow Google's OAuth 2.0 best practices.
*   Use a library like `beautifulsoup4` for HTML parsing and `html2text` for Markdown conversion.
*   Output files should be UTF-8 encoded.
*   File naming convention: `[Sanitized_Subject_Line]_[Shortened_Email_ID].md`
