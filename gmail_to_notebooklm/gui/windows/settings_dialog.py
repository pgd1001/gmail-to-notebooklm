"""Settings dialog for Gmail to NotebookLM GUI."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Dict, Optional


class SettingsDialog(tk.Toplevel):
    """Dialog for application settings.

    Allows configuration of:
    - Credentials file location
    - Token file location
    - Default output directory
    - Default export options
    """

    def __init__(self, parent, current_settings: Optional[Dict] = None):
        """Initialize settings dialog.

        Args:
            parent: Parent Tkinter widget
            current_settings: Current settings dictionary
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = current_settings or {}

        # Configure window
        self.title("Settings")
        self.geometry("600x500")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        # Result
        self.result = None

        # Build UI
        self._create_widgets()
        self._load_settings()

        # Prevent closing without saving/canceling
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _create_widgets(self):
        """Create settings widgets."""
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text="Application Settings",
            font=("Segoe UI", 12, "bold")
        )
        title.pack(pady=(0, 20))

        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Authentication tab
        auth_frame = ttk.Frame(notebook, padding="10")
        notebook.add(auth_frame, text="Authentication")
        self._create_auth_settings(auth_frame)

        # Export defaults tab
        export_frame = ttk.Frame(notebook, padding="10")
        notebook.add(export_frame, text="Export Defaults")
        self._create_export_settings(export_frame)

        # Advanced tab
        advanced_frame = ttk.Frame(notebook, padding="10")
        notebook.add(advanced_frame, text="Advanced")
        self._create_advanced_settings(advanced_frame)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        cancel_button.pack(side=tk.RIGHT)

        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=self._on_save
        )
        save_button.pack(side=tk.RIGHT, padx=(0, 10))

        reset_button = ttk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_defaults
        )
        reset_button.pack(side=tk.LEFT)

    def _create_auth_settings(self, parent):
        """Create authentication settings.

        Args:
            parent: Parent frame
        """
        # Credentials file
        ttk.Label(parent, text="Credentials File:").pack(anchor=tk.W, pady=(0, 5))

        cred_frame = ttk.Frame(parent)
        cred_frame.pack(fill=tk.X, pady=(0, 15))

        self.credentials_var = tk.StringVar()
        cred_entry = ttk.Entry(cred_frame, textvariable=self.credentials_var)
        cred_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Button(
            cred_frame,
            text="Browse...",
            command=lambda: self._browse_file(
                self.credentials_var,
                "Select credentials.json",
                [("JSON files", "*.json")]
            )
        ).pack(side=tk.LEFT)

        # Token file
        ttk.Label(parent, text="Token File:").pack(anchor=tk.W, pady=(0, 5))

        token_frame = ttk.Frame(parent)
        token_frame.pack(fill=tk.X, pady=(0, 15))

        self.token_var = tk.StringVar()
        token_entry = ttk.Entry(token_frame, textvariable=self.token_var)
        token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Button(
            token_frame,
            text="Browse...",
            command=lambda: self._browse_file(
                self.token_var,
                "Select token.json",
                [("JSON files", "*.json")]
            )
        ).pack(side=tk.LEFT)

        # Revoke token button
        revoke_frame = ttk.Frame(parent)
        revoke_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            revoke_frame,
            text="Revoke Current Token",
            command=self._revoke_token
        ).pack(side=tk.LEFT)

        info_label = ttk.Label(
            revoke_frame,
            text="(Forces re-authentication on next use)",
            font=("Segoe UI", 8),
            foreground="gray"
        )
        info_label.pack(side=tk.LEFT, padx=(10, 0))

    def _create_export_settings(self, parent):
        """Create export default settings.

        Args:
            parent: Parent frame
        """
        # Default output directory
        ttk.Label(parent, text="Default Output Directory:").pack(anchor=tk.W, pady=(0, 5))

        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.X, pady=(0, 15))

        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Button(
            output_frame,
            text="Browse...",
            command=lambda: self._browse_directory(self.output_dir_var)
        ).pack(side=tk.LEFT)

        # Default options
        ttk.Label(
            parent,
            text="Default Export Options:",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.W, pady=(10, 10))

        self.organize_by_date_var = tk.BooleanVar()
        ttk.Checkbutton(
            parent,
            text="Organize by date",
            variable=self.organize_by_date_var
        ).pack(anchor=tk.W, pady=(0, 5))

        # Date format
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(date_frame, text="    Date format:").pack(side=tk.LEFT)

        self.date_format_var = tk.StringVar()
        date_combo = ttk.Combobox(
            date_frame,
            textvariable=self.date_format_var,
            values=["YYYY/MM", "YYYY-MM", "YYYY/MM/DD", "YYYY-MM-DD"],
            state="readonly",
            width=15
        )
        date_combo.pack(side=tk.LEFT, padx=(10, 0))

        self.create_index_var = tk.BooleanVar()
        ttk.Checkbutton(
            parent,
            text="Create index file (INDEX.md)",
            variable=self.create_index_var
        ).pack(anchor=tk.W, pady=(0, 5))

        self.overwrite_var = tk.BooleanVar()
        ttk.Checkbutton(
            parent,
            text="Overwrite existing files",
            variable=self.overwrite_var
        ).pack(anchor=tk.W, pady=(0, 5))

        # Default max results
        max_frame = ttk.Frame(parent)
        max_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(max_frame, text="Default max emails:").pack(side=tk.LEFT)

        self.max_results_var = tk.StringVar()
        max_entry = ttk.Entry(max_frame, textvariable=self.max_results_var, width=10)
        max_entry.pack(side=tk.LEFT, padx=(10, 0))

        ttk.Label(
            max_frame,
            text="(leave empty for no limit)",
            font=("Segoe UI", 8),
            foreground="gray"
        ).pack(side=tk.LEFT, padx=(10, 0))

    def _create_advanced_settings(self, parent):
        """Create advanced settings.

        Args:
            parent: Parent frame
        """
        ttk.Label(
            parent,
            text="Performance & Behavior",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))

        # Show warnings
        self.show_warnings_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent,
            text="Show warning dialogs",
            variable=self.show_warnings_var
        ).pack(anchor=tk.W, pady=(0, 5))

        # Auto-authenticate
        self.auto_auth_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent,
            text="Auto-authenticate on startup",
            variable=self.auto_auth_var
        ).pack(anchor=tk.W, pady=(0, 5))

        # Confirm before overwrite
        self.confirm_overwrite_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent,
            text="Confirm before overwriting files",
            variable=self.confirm_overwrite_var
        ).pack(anchor=tk.W, pady=(0, 15))

        ttk.Label(
            parent,
            text="Application Info",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.W, pady=(10, 10))

        info_frame = ttk.Frame(parent, relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))

        info_text = (
            "Gmail to NotebookLM v0.2.0\n\n"
            "Export Gmail emails to Markdown format for use with Google NotebookLM.\n\n"
            "GitHub: github.com/pgd1001/gmail-to-notebooklm"
        )

        ttk.Label(
            info_frame,
            text=info_text,
            justify=tk.LEFT,
            font=("Segoe UI", 8)
        ).pack(pady=10, padx=10)

    def _browse_file(self, var: tk.StringVar, title: str, filetypes: list):
        """Browse for file.

        Args:
            var: StringVar to update
            title: Dialog title
            filetypes: File type filters
        """
        filename = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes + [("All files", "*.*")]
        )
        if filename:
            var.set(filename)

    def _browse_directory(self, var: tk.StringVar):
        """Browse for directory.

        Args:
            var: StringVar to update
        """
        directory = filedialog.askdirectory(
            title="Select Default Output Directory",
            initialdir=var.get() or "."
        )
        if directory:
            var.set(directory)

    def _revoke_token(self):
        """Revoke authentication token."""
        token_path = self.token_var.get() or "token.json"

        if not Path(token_path).exists():
            messagebox.showinfo(
                "No Token Found",
                f"No token file found at:\n{token_path}"
            )
            return

        if messagebox.askyesno(
            "Revoke Token?",
            "This will delete the saved authentication token.\n\n"
            "You'll need to re-authenticate the next time you use the application.\n\n"
            "Continue?"
        ):
            try:
                from gmail_to_notebooklm.auth import revoke_token
                revoke_token(token_path)
                messagebox.showinfo(
                    "Token Revoked",
                    "Authentication token has been revoked.\n\n"
                    "You'll be prompted to re-authenticate on next use."
                )
            except Exception as e:
                messagebox.showerror(
                    "Error Revoking Token",
                    f"Could not revoke token:\n\n{e}"
                )

    def _load_settings(self):
        """Load current settings into UI."""
        self.credentials_var.set(self.settings.get("credentials_path", "credentials.json"))
        self.token_var.set(self.settings.get("token_path", "token.json"))
        self.output_dir_var.set(self.settings.get("output_dir", "./output"))
        self.organize_by_date_var.set(self.settings.get("organize_by_date", False))
        self.date_format_var.set(self.settings.get("date_format", "YYYY/MM"))
        self.create_index_var.set(self.settings.get("create_index", False))
        self.overwrite_var.set(self.settings.get("overwrite", False))
        self.max_results_var.set(str(self.settings.get("max_results", "")))

    def _reset_defaults(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno(
            "Reset to Defaults?",
            "This will reset all settings to their default values.\n\n"
            "Continue?"
        ):
            self.credentials_var.set("credentials.json")
            self.token_var.set("token.json")
            self.output_dir_var.set("./output")
            self.organize_by_date_var.set(False)
            self.date_format_var.set("YYYY/MM")
            self.create_index_var.set(False)
            self.overwrite_var.set(False)
            self.max_results_var.set("")
            self.show_warnings_var.set(True)
            self.auto_auth_var.set(True)
            self.confirm_overwrite_var.set(True)

    def _on_save(self):
        """Save settings and close."""
        # Validate settings
        try:
            # Build result dictionary
            self.result = {
                "credentials_path": self.credentials_var.get(),
                "token_path": self.token_var.get(),
                "output_dir": self.output_dir_var.get(),
                "organize_by_date": self.organize_by_date_var.get(),
                "date_format": self.date_format_var.get(),
                "create_index": self.create_index_var.get(),
                "overwrite": self.overwrite_var.get(),
                "show_warnings": self.show_warnings_var.get(),
                "auto_auth": self.auto_auth_var.get(),
                "confirm_overwrite": self.confirm_overwrite_var.get(),
            }

            # Add max_results if set
            if self.max_results_var.get():
                try:
                    self.result["max_results"] = int(self.max_results_var.get())
                except ValueError:
                    messagebox.showerror(
                        "Invalid Value",
                        "Max emails must be a number."
                    )
                    return

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error Saving Settings",
                f"Could not save settings:\n\n{e}"
            )

    def _on_cancel(self):
        """Cancel and close without saving."""
        self.result = None
        self.destroy()

    def get_result(self) -> Optional[Dict]:
        """Get the result after dialog is closed.

        Returns:
            Settings dictionary if saved, None if cancelled
        """
        return self.result
