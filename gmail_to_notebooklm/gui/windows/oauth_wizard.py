"""OAuth 2.0 setup wizard for Gmail to NotebookLM GUI."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import webbrowser


class OAuthWizard(tk.Toplevel):
    """Wizard for setting up OAuth 2.0 credentials.

    Guides users through:
    1. Creating Google Cloud project
    2. Enabling Gmail API
    3. Creating OAuth credentials
    4. Downloading credentials.json
    5. Running first authentication
    """

    def __init__(self, parent, on_complete=None):
        """Initialize OAuth wizard.

        Args:
            parent: Parent Tkinter widget
            on_complete: Callback function when setup is complete
        """
        super().__init__(parent)
        self.parent = parent
        self.on_complete = on_complete

        # Configure window
        self.title("Gmail API Setup Wizard")
        self.geometry("700x500")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        # State
        self.current_step = 0
        self.credentials_path = None

        # Build UI
        self._create_widgets()
        self._show_step(0)

        # Prevent closing during important steps
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self):
        """Create wizard widgets."""
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(
            main_frame,
            text="Gmail API Setup",
            font=("Segoe UI", 14, "bold")
        )
        self.title_label.pack(pady=(0, 10))

        # Subtitle
        self.subtitle_label = ttk.Label(
            main_frame,
            text="Step 1 of 5",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Content area (will be filled by each step)
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        self.back_button = ttk.Button(
            button_frame,
            text="< Back",
            command=self._prev_step,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT)

        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(10, 0))

        self.next_button = ttk.Button(
            button_frame,
            text="Next >",
            command=self._next_step
        )
        self.next_button.pack(side=tk.RIGHT)

    def _show_step(self, step: int):
        """Show specific wizard step.

        Args:
            step: Step number (0-4)
        """
        self.current_step = step

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Update subtitle
        self.subtitle_label.config(text=f"Step {step + 1} of 5")

        # Show appropriate step
        if step == 0:
            self._show_welcome()
        elif step == 1:
            self._show_google_cloud()
        elif step == 2:
            self._show_enable_api()
        elif step == 3:
            self._show_credentials()
        elif step == 4:
            self._show_download()

        # Update buttons
        self.back_button.config(state=tk.NORMAL if step > 0 else tk.DISABLED)
        self.next_button.config(text="Finish" if step == 4 else "Next >")

    def _show_welcome(self):
        """Show welcome step."""
        self.title_label.config(text="Welcome to Gmail to NotebookLM")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "This wizard will help you set up access to the Gmail API.\n\n"
            "You'll need to:\n"
            "1. Create a Google Cloud project (free)\n"
            "2. Enable the Gmail API\n"
            "3. Create OAuth 2.0 credentials\n"
            "4. Download the credentials file\n"
            "5. Authenticate with your Gmail account\n\n"
            "This process takes about 5-10 minutes.\n\n"
            "Requirements:\n"
            "• A Google account with Gmail access\n"
            "• A web browser for authentication"
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=20)

    def _show_google_cloud(self):
        """Show Google Cloud Console step."""
        self.title_label.config(text="Create Google Cloud Project")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "1. Go to the Google Cloud Console\n"
            "2. Click 'Select a project' → 'New Project'\n"
            "3. Enter a project name (e.g., 'Gmail to NotebookLM')\n"
            "4. Click 'Create'\n"
            "5. Wait for the project to be created\n"
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=10)

        # Open browser button
        open_button = ttk.Button(
            content,
            text="Open Google Cloud Console",
            command=lambda: webbrowser.open("https://console.cloud.google.com/")
        )
        open_button.pack(pady=10)

        # Info box
        info_frame = ttk.Frame(content, relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=20, padx=20)

        info_label = ttk.Label(
            info_frame,
            text="💡 Tip: Keep this wizard open while you complete the steps in your browser.",
            foreground="blue",
            wraplength=550
        )
        info_label.pack(pady=10, padx=10)

    def _show_enable_api(self):
        """Show Enable Gmail API step."""
        self.title_label.config(text="Enable Gmail API")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "1. In the Google Cloud Console, select your project\n"
            "2. Go to 'APIs & Services' → 'Library'\n"
            "3. Search for 'Gmail API'\n"
            "4. Click on 'Gmail API' in the results\n"
            "5. Click 'Enable'\n"
            "6. Wait for the API to be enabled\n"
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=10)

        # Open API library button
        open_button = ttk.Button(
            content,
            text="Open API Library",
            command=lambda: webbrowser.open("https://console.cloud.google.com/apis/library")
        )
        open_button.pack(pady=10)

    def _show_credentials(self):
        """Show Create Credentials step."""
        self.title_label.config(text="Create OAuth Credentials")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "1. Go to 'APIs & Services' → 'Credentials'\n"
            "2. Click 'Create Credentials' → 'OAuth client ID'\n"
            "3. If prompted, configure the OAuth consent screen:\n"
            "   • Choose 'External' user type\n"
            "   • Fill in app name and your email\n"
            "   • Add your email as a test user\n"
            "   • Save and continue through remaining steps\n"
            "4. Back in Credentials, create OAuth client ID:\n"
            "   • Application type: 'Desktop app'\n"
            "   • Name: 'Gmail to NotebookLM'\n"
            "5. Click 'Create'\n"
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=10)

        # Open credentials button
        open_button = ttk.Button(
            content,
            text="Open Credentials Page",
            command=lambda: webbrowser.open("https://console.cloud.google.com/apis/credentials")
        )
        open_button.pack(pady=10)

    def _show_download(self):
        """Show Download Credentials step."""
        self.title_label.config(text="Download Credentials")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "1. In the Credentials page, find your OAuth 2.0 Client ID\n"
            "2. Click the download icon (⬇) on the right\n"
            "3. Save the file as 'credentials.json'\n"
            "4. Use the button below to select the downloaded file\n"
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=10)

        # File selection
        file_frame = ttk.Frame(content)
        file_frame.pack(fill=tk.X, pady=20)

        ttk.Label(file_frame, text="Credentials file:").pack(anchor=tk.W)

        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill=tk.X, pady=5)

        self.path_var = tk.StringVar(value="Not selected")
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state="readonly")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_button = ttk.Button(
            path_frame,
            text="Browse...",
            command=self._browse_credentials
        )
        browse_button.pack(side=tk.LEFT)

        # Warning box
        if not self.credentials_path:
            warning_frame = ttk.Frame(content, relief=tk.SOLID, borderwidth=1)
            warning_frame.pack(fill=tk.X, pady=10)

            warning_label = ttk.Label(
                warning_frame,
                text="⚠️ Please select the credentials.json file before finishing.",
                foreground="orange",
                wraplength=550
            )
            warning_label.pack(pady=10, padx=10)

    def _browse_credentials(self):
        """Open file browser for credentials selection."""
        filename = filedialog.askopenfilename(
            title="Select credentials.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            self.credentials_path = filename
            self.path_var.set(filename)

            # Validate the file
            try:
                import json
                with open(filename, 'r') as f:
                    data = json.load(f)
                    if "installed" not in data and "web" not in data:
                        messagebox.showwarning(
                            "Invalid Credentials",
                            "This doesn't appear to be a valid OAuth credentials file.\n\n"
                            "Make sure you downloaded the OAuth 2.0 Client ID credentials, "
                            "not the API key or service account credentials."
                        )
                        self.credentials_path = None
                        self.path_var.set("Not selected")
            except Exception as e:
                messagebox.showerror(
                    "Invalid File",
                    f"Could not read credentials file:\n\n{e}"
                )
                self.credentials_path = None
                self.path_var.set("Not selected")

    def _next_step(self):
        """Move to next step."""
        if self.current_step == 4:
            self._finish()
        else:
            self._show_step(self.current_step + 1)

    def _prev_step(self):
        """Move to previous step."""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _finish(self):
        """Complete the wizard."""
        if not self.credentials_path:
            messagebox.showwarning(
                "Credentials Required",
                "Please select the credentials.json file before finishing."
            )
            return

        # Copy credentials to project directory
        try:
            import shutil
            target_path = Path("credentials.json")

            # Ask before overwriting
            if target_path.exists():
                if not messagebox.askyesno(
                    "Overwrite Existing File?",
                    f"A credentials.json file already exists.\n\n"
                    "Do you want to replace it with the new one?"
                ):
                    return

            shutil.copy(self.credentials_path, target_path)

            messagebox.showinfo(
                "Setup Complete",
                "Credentials have been saved!\n\n"
                "Click OK to continue. You'll be prompted to authenticate "
                "with your Gmail account in a browser window."
            )

            # Close wizard and trigger callback
            if self.on_complete:
                self.on_complete()

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error Saving Credentials",
                f"Could not save credentials.json:\n\n{e}"
            )

    def _on_cancel(self):
        """Handle cancel button."""
        if messagebox.askyesno(
            "Cancel Setup?",
            "Are you sure you want to cancel the setup?\n\n"
            "You won't be able to use the application without valid credentials."
        ):
            self.destroy()

    def _on_close(self):
        """Handle window close button."""
        self._on_cancel()
