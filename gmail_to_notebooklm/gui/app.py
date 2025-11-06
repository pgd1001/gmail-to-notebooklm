"""Main GUI application class."""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Optional

from gmail_to_notebooklm.gui.windows.main_window import MainWindow


class GmailToNotebookLMApp:
    """Main application class for Gmail to NotebookLM GUI.

    This class manages the Tkinter application lifecycle and main window.
    """

    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.root.title("Gmail to NotebookLM")
        self.root.geometry("800x600")

        # Set minimum window size
        self.root.minsize(600, 400)

        # Configure style
        self._setup_style()

        # Create main window
        self.main_window = MainWindow(self.root)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_style(self):
        """Configure application styling."""
        style = ttk.Style()

        # Use a modern theme if available
        available_themes = style.theme_names()
        if "vista" in available_themes:
            style.theme_use("vista")
        elif "clam" in available_themes:
            style.theme_use("clam")

        # Configure custom styles
        style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 9))
        style.configure("Action.TButton", padding=10)

    def _on_close(self):
        """Handle window close event."""
        # TODO: Check if export is in progress and confirm
        self.root.quit()

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Entry point for GUI application."""
    app = GmailToNotebookLMApp()
    app.run()


if __name__ == "__main__":
    main()
