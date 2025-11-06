"""Main window for Gmail to NotebookLM GUI."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional
import threading

from gmail_to_notebooklm.auth import authenticate, AuthenticationError
from gmail_to_notebooklm.gmail_client import GmailClient, GmailAPIError
from gmail_to_notebooklm.core import ExportEngine, ExportResult, ProgressUpdate
from gmail_to_notebooklm.gui.windows.export_dialog import ExportDialog
from gmail_to_notebooklm.gui.windows.oauth_wizard import OAuthWizard
from gmail_to_notebooklm.gui.windows.settings_dialog import SettingsDialog
from gmail_to_notebooklm.gui.windows.history_dialog import HistoryDialog
from gmail_to_notebooklm.gui.windows.profiles_dialog import ProfilesDialog


class MainWindow(ttk.Frame):
    """Main application window.

    Provides interface for:
    - Gmail label selection
    - Email filtering options
    - Output directory selection
    - Export initiation
    """

    def __init__(self, parent):
        """Initialize main window.

        Args:
            parent: Parent Tkinter widget
        """
        super().__init__(parent, padding="20")
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        # State
        self.gmail_client: Optional[GmailClient] = None
        self.available_labels: list = []
        self.credentials_path = "credentials.json"
        self.token_path = "token.json"
        self.settings = {}

        # Build UI
        self._create_widgets()

        # Check authentication on startup
        self._check_authentication()

    def _create_widgets(self):
        """Create all UI widgets."""
        # Menu bar
        menu_frame = ttk.Frame(self)
        menu_frame.pack(fill=tk.X, pady=(0, 10))

        setup_button = ttk.Button(
            menu_frame,
            text="Setup Wizard",
            command=self._show_oauth_wizard
        )
        setup_button.pack(side=tk.LEFT, padx=(0, 5))

        settings_button = ttk.Button(
            menu_frame,
            text="Settings",
            command=self._show_settings
        )
        settings_button.pack(side=tk.LEFT, padx=(0, 5))

        profiles_button = ttk.Button(
            menu_frame,
            text="Profiles",
            command=self._show_profiles
        )
        profiles_button.pack(side=tk.LEFT, padx=(0, 5))

        history_button = ttk.Button(
            menu_frame,
            text="History",
            command=self._show_history
        )
        history_button.pack(side=tk.LEFT)

        # Title
        title = ttk.Label(
            self,
            text="Gmail to NotebookLM",
            style="Title.TLabel"
        )
        title.pack(pady=(0, 5))

        subtitle = ttk.Label(
            self,
            text="Export Gmail emails to Markdown for NotebookLM",
            style="Subtitle.TLabel"
        )
        subtitle.pack(pady=(0, 20))

        # Authentication status
        self.auth_frame = ttk.Frame(self)
        self.auth_frame.pack(fill=tk.X, pady=(0, 20))

        self.auth_status_label = ttk.Label(
            self.auth_frame,
            text="Not authenticated",
            foreground="red"
        )
        self.auth_status_label.pack(side=tk.LEFT)

        self.auth_button = ttk.Button(
            self.auth_frame,
            text="Authenticate",
            command=self._authenticate
        )
        self.auth_button.pack(side=tk.RIGHT)

        # Main content frame
        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True)

        # Left panel - Selection
        left_panel = ttk.LabelFrame(content, text="Email Selection", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Label selection
        ttk.Label(left_panel, text="Gmail Label:").pack(anchor=tk.W, pady=(0, 5))
        self.label_var = tk.StringVar()
        self.label_combo = ttk.Combobox(
            left_panel,
            textvariable=self.label_var,
            state="readonly",
            width=30
        )
        self.label_combo.pack(fill=tk.X, pady=(0, 15))

        # Query
        ttk.Label(left_panel, text="Gmail Query (optional):").pack(anchor=tk.W, pady=(0, 5))
        self.query_var = tk.StringVar()
        query_entry = ttk.Entry(left_panel, textvariable=self.query_var)
        query_entry.pack(fill=tk.X, pady=(0, 15))

        # Max results
        ttk.Label(left_panel, text="Max Emails (optional):").pack(anchor=tk.W, pady=(0, 5))
        self.max_results_var = tk.StringVar()
        max_results_entry = ttk.Entry(left_panel, textvariable=self.max_results_var, width=10)
        max_results_entry.pack(anchor=tk.W, pady=(0, 15))

        # Right panel - Filters
        right_panel = ttk.LabelFrame(content, text="Filters", padding="10")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Date filters
        ttk.Label(right_panel, text="After Date (YYYY-MM-DD):").pack(anchor=tk.W, pady=(0, 5))
        self.after_var = tk.StringVar()
        after_entry = ttk.Entry(right_panel, textvariable=self.after_var)
        after_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_panel, text="Before Date (YYYY-MM-DD):").pack(anchor=tk.W, pady=(0, 5))
        self.before_var = tk.StringVar()
        before_entry = ttk.Entry(right_panel, textvariable=self.before_var)
        before_entry.pack(fill=tk.X, pady=(0, 10))

        # Sender filters
        ttk.Label(right_panel, text="From (sender email):").pack(anchor=tk.W, pady=(0, 5))
        self.from_var = tk.StringVar()
        from_entry = ttk.Entry(right_panel, textvariable=self.from_var)
        from_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_panel, text="To (recipient email):").pack(anchor=tk.W, pady=(0, 5))
        self.to_var = tk.StringVar()
        to_entry = ttk.Entry(right_panel, textvariable=self.to_var)
        to_entry.pack(fill=tk.X, pady=(0, 10))

        # Bottom panel - Output and Actions
        bottom_panel = ttk.Frame(self)
        bottom_panel.pack(fill=tk.X, pady=(20, 0))

        # Output directory
        output_frame = ttk.LabelFrame(bottom_panel, text="Output", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))

        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill=tk.X)

        ttk.Label(dir_frame, text="Output Directory:").pack(side=tk.LEFT, padx=(0, 10))
        self.output_dir_var = tk.StringVar(value="./output")
        output_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_button = ttk.Button(
            dir_frame,
            text="Browse...",
            command=self._browse_output_dir
        )
        browse_button.pack(side=tk.LEFT)

        # Options
        options_frame = ttk.Frame(output_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))

        self.organize_by_date_var = tk.BooleanVar(value=False)
        organize_check = ttk.Checkbutton(
            options_frame,
            text="Organize by date",
            variable=self.organize_by_date_var
        )
        organize_check.pack(side=tk.LEFT, padx=(0, 20))

        self.create_index_var = tk.BooleanVar(value=False)
        index_check = ttk.Checkbutton(
            options_frame,
            text="Create index",
            variable=self.create_index_var
        )
        index_check.pack(side=tk.LEFT, padx=(0, 20))

        self.overwrite_var = tk.BooleanVar(value=False)
        overwrite_check = ttk.Checkbutton(
            options_frame,
            text="Overwrite existing",
            variable=self.overwrite_var
        )
        overwrite_check.pack(side=tk.LEFT)

        # Export button
        self.export_button = ttk.Button(
            bottom_panel,
            text="Export Emails",
            command=self._start_export,
            style="Action.TButton",
            state=tk.DISABLED
        )
        self.export_button.pack(fill=tk.X)

    def _check_authentication(self):
        """Check if user is already authenticated."""
        try:
            # Try to load existing credentials without triggering OAuth flow
            token_file = Path(self.token_path)
            if token_file.exists():
                self._authenticate(silent=True)
            else:
                self._update_auth_status(False, "Not authenticated")
        except Exception:
            self._update_auth_status(False, "Not authenticated")

    def _authenticate(self, silent=False):
        """Authenticate with Gmail API.

        Args:
            silent: If True, don't show success messages
        """
        def auth_task():
            try:
                # Status updates
                def status_callback(message: str):
                    self.parent.after(0, lambda: self._update_auth_status(None, message))

                # Authenticate
                creds = authenticate(
                    credentials_path=self.credentials_path,
                    token_path=self.token_path,
                    status_callback=status_callback
                )

                # Create Gmail client
                self.gmail_client = GmailClient(creds)

                # Fetch labels
                self.available_labels = self.gmail_client.list_labels()

                # Update UI on main thread
                self.parent.after(0, self._on_auth_success, silent)

            except AuthenticationError as e:
                self.parent.after(0, self._on_auth_error, str(e))
            except Exception as e:
                self.parent.after(0, self._on_auth_error, f"Unexpected error: {e}")

        # Disable button during auth
        self.auth_button.config(state=tk.DISABLED)
        self._update_auth_status(None, "Authenticating...")

        # Run in background thread
        thread = threading.Thread(target=auth_task, daemon=True)
        thread.start()

    def _on_auth_success(self, silent=False):
        """Handle successful authentication.

        Args:
            silent: If True, don't show success message
        """
        self._update_auth_status(True, "Authenticated")
        self.auth_button.config(state=tk.NORMAL, text="Re-authenticate")

        # Populate labels
        self.label_combo["values"] = self.available_labels
        if self.available_labels:
            self.label_combo.current(0)

        # Enable export
        self.export_button.config(state=tk.NORMAL)

        if not silent:
            messagebox.showinfo("Success", "Successfully authenticated with Gmail!")

    def _on_auth_error(self, error_message: str):
        """Handle authentication error.

        Args:
            error_message: Error description
        """
        self._update_auth_status(False, "Authentication failed")
        self.auth_button.config(state=tk.NORMAL)

        messagebox.showerror(
            "Authentication Error",
            f"Failed to authenticate:\n\n{error_message}\n\n"
            "Please check:\n"
            "1. credentials.json exists\n"
            "2. Gmail API is enabled\n"
            "3. Your account is added as test user"
        )

    def _update_auth_status(self, authenticated: Optional[bool], message: str):
        """Update authentication status display.

        Args:
            authenticated: True if authenticated, False if not, None for in-progress
            message: Status message to display
        """
        self.auth_status_label.config(text=message)

        if authenticated is True:
            self.auth_status_label.config(foreground="green")
        elif authenticated is False:
            self.auth_status_label.config(foreground="red")
        else:
            self.auth_status_label.config(foreground="orange")

    def _browse_output_dir(self):
        """Open directory browser for output selection."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)

    def _validate_settings(self) -> tuple[bool, str]:
        """Validate export settings.

        Returns:
            (valid, error_message) tuple
        """
        # Check label or query
        if not self.label_var.get() and not self.query_var.get():
            return False, "Please select a label or enter a query"

        # Check max results format
        if self.max_results_var.get():
            try:
                max_results = int(self.max_results_var.get())
                if max_results <= 0:
                    return False, "Max emails must be positive"
            except ValueError:
                return False, "Max emails must be a number"

        # Check output directory
        if not self.output_dir_var.get():
            return False, "Please select an output directory"

        return True, ""

    def _start_export(self):
        """Start export process."""
        # Validate settings
        valid, error = self._validate_settings()
        if not valid:
            messagebox.showerror("Invalid Settings", error)
            return

        # Build settings dictionary
        settings = {
            "label": self.label_var.get() or None,
            "query": self.query_var.get() or None,
            "output_dir": self.output_dir_var.get(),
            "credentials_path": self.credentials_path,
            "token_path": self.token_path,
            "organize_by_date": self.organize_by_date_var.get(),
            "create_index": self.create_index_var.get(),
            "overwrite": self.overwrite_var.get(),
        }

        # Add optional filters
        if self.max_results_var.get():
            settings["max_results"] = int(self.max_results_var.get())
        if self.after_var.get():
            settings["after"] = self.after_var.get()
        if self.before_var.get():
            settings["before"] = self.before_var.get()
        if self.from_var.get():
            settings["from_"] = self.from_var.get()
        if self.to_var.get():
            settings["to"] = self.to_var.get()

        # Show export dialog
        dialog = ExportDialog(self.parent, settings)
        dialog.start_export()

    def _show_oauth_wizard(self):
        """Show OAuth setup wizard."""
        wizard = OAuthWizard(self.parent, on_complete=lambda: self._authenticate(silent=False))

    def _show_settings(self):
        """Show settings dialog."""
        # Prepare current settings
        current_settings = {
            "credentials_path": self.credentials_path,
            "token_path": self.token_path,
            "output_dir": self.output_dir_var.get(),
            "organize_by_date": self.organize_by_date_var.get(),
            "create_index": self.create_index_var.get(),
            "overwrite": self.overwrite_var.get(),
        }

        # Show dialog
        dialog = SettingsDialog(self.parent, current_settings)
        self.parent.wait_window(dialog)

        # Apply new settings if saved
        result = dialog.get_result()
        if result:
            self.credentials_path = result.get("credentials_path", "credentials.json")
            self.token_path = result.get("token_path", "token.json")
            self.output_dir_var.set(result.get("output_dir", "./output"))
            self.organize_by_date_var.set(result.get("organize_by_date", False))
            self.create_index_var.set(result.get("create_index", False))
            self.overwrite_var.set(result.get("overwrite", False))
            self.settings = result

            messagebox.showinfo("Settings Saved", "Settings have been updated successfully!")

    def _show_history(self):
        """Show export history dialog."""
        HistoryDialog(self.parent)

    def _show_profiles(self):
        """Show export profiles dialog."""
        ProfilesDialog(self.parent, on_load_callback=self._load_profile_settings)

    def _load_profile_settings(self, settings: dict):
        """Load settings from profile.

        Args:
            settings: Profile settings dictionary
        """
        # Apply profile settings to form fields
        if settings.get("label"):
            # Find and select the label in combo box
            labels = self.label_combo["values"]
            if settings["label"] in labels:
                self.label_combo.set(settings["label"])

        if settings.get("query"):
            self.query_var.set(settings["query"])

        if settings.get("output_dir"):
            self.output_dir_var.set(settings["output_dir"])

        if "organize_by_date" in settings:
            self.organize_by_date_var.set(settings["organize_by_date"])

        if "create_index" in settings:
            self.create_index_var.set(settings["create_index"])

        if "overwrite" in settings:
            self.overwrite_var.set(settings["overwrite"])

        if settings.get("max_results"):
            self.max_results_var.set(str(settings["max_results"]))

        if settings.get("after"):
            self.after_var.set(settings["after"])

        if settings.get("before"):
            self.before_var.set(settings["before"])

        if settings.get("from"):
            self.from_var.set(settings["from"])

        if settings.get("to"):
            self.to_var.set(settings["to"])
