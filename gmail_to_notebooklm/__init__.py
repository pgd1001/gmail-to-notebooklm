"""Gmail to NotebookLM Converter.

Convert Gmail emails from a specific label into Markdown files formatted
for Google NotebookLM.
"""

__version__ = "0.3.0"
__author__ = "Gmail to NotebookLM Contributors"
__license__ = "MIT"

from gmail_to_notebooklm.auth import authenticate
from gmail_to_notebooklm.config import Config, load_config
from gmail_to_notebooklm.gmail_client import GmailClient
from gmail_to_notebooklm.parser import EmailParser
from gmail_to_notebooklm.converter import MarkdownConverter

__all__ = [
    "authenticate",
    "Config",
    "load_config",
    "GmailClient",
    "EmailParser",
    "MarkdownConverter",
    "__version__",
]
