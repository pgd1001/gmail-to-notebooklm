"""OAuth 2.0 setup wizard for Gmail to NotebookLM GUI (User-Level)."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import webbrowser


class OAuthWizard(tk.Toplevel):
    """Simplified user-level wizard for Gmail authentication.

    This user-level wizard assumes credentials.json already exists
    (either embedded or placed by user).

    For technical setup (creating credentials), see ADMIN_SETUP.md:
    https://github.com/yourusername/gmail-to-notebooklm/blob/main/docs/ADMIN_SETUP.md
    """

    def __init__(self, parent, on_complete=None):
        """Initialize OAuth authentication wizard.

        Args:
            parent: Parent Tkinter widget
            on_complete: Callback function when setup is complete
        """
        super().__init__(parent)
        self.parent = parent
        self.on_complete = on_complete

        # Configure window
        self.title("Gmail Authentication")
        self.geometry("700x450")
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
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

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
            step: Step number (0-1)
        """
        self.current_step = step

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Update subtitle
        self.subtitle_label.config(text=f"Step {step + 1} of 2")

        # Show appropriate step
        if step == 0:
            self._show_welcome()
        elif step == 1:
            self._show_authenticate()

        # Update buttons
        self.back_button.config(state=tk.NORMAL if step > 0 else tk.DISABLED)
        self.next_button.config(text="Authenticate" if step == 0 else "Done")

    def _show_welcome(self):
        """Show welcome step - user level only."""
        self.title_label.config(text="Gmail Authentication Setup")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "Welcome! This wizard will authenticate you with Gmail.\n\n"
            "What happens next:\n"
            "1. Click 'Authenticate'\n"
            "2. Your browser opens to Gmail login\n"
            "3. Sign in with your Google account\n"
            "4. Grant read-only access to Gmail\n"
            "5. Done! You're ready to export emails\n\n"
            "Requirements:\n"
            "• A Google account with Gmail\n"
            "• Internet connection\n"
            "• A web browser\n\n"
            "⚠️ This app uses read-only access.\n"
            "It cannot delete, modify, or send emails."
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=20)

        # Info about admin setup
        info_frame = ttk.LabelFrame(content, text="Need to set up credentials?", padding="10")
        info_frame.pack(fill=tk.X, pady=10, padx=10)

        info_text = (
            "If you don't have credentials set up yet, see:\n"
            "Settings → Advanced Setup or the Help menu"
        )
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            justify=tk.LEFT,
            wraplength=550
        )
        info_label.pack(anchor=tk.W)

    def _show_authenticate(self):
        """Show authentication step."""
        self.title_label.config(text="Authenticating with Gmail")

        content = ttk.Frame(self.content_frame)
        content.pack(fill=tk.BOTH, expand=True)

        text = (
            "Click the button below to authenticate.\n\n"
            "Your browser will open to Gmail's login page.\n\n"
            "You'll be asked to:\n"
            "1. Sign in with your Google account\n"
            "2. Review the requested permissions\n"
            "3. Click 'Allow' to grant access\n\n"
            "After you authorize, come back to this window\n"
            "and click 'Done' to complete setup."
        )

        label = ttk.Label(
            content,
            text=text,
            justify=tk.LEFT,
            wraplength=600
        )
        label.pack(pady=20)

        # Info box
        info_frame = ttk.Frame(content, relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=10, padx=20)

        info_label = ttk.Label(
            info_frame,
            text="💡 Tip: Keep this window open while you authenticate in your browser.",
            foreground="blue",
            wraplength=550
        )
        info_label.pack(pady=10, padx=10)

    def _next_step(self):
        """Move to next step or finish."""
        if self.current_step == 1:
            self._finish()
        else:
            self._show_step(self.current_step + 1)

    def _prev_step(self):
        """Move to previous step."""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _finish(self):
        """Complete authentication and trigger callback."""
        messagebox.showinfo(
            "Authentication Complete",
            "Great! You've successfully authenticated with Gmail.\n\n"
            "You're ready to start exporting emails.\n\n"
            "Click OK to close this window."
        )

        # Close wizard and trigger callback
        if self.on_complete:
            self.on_complete()

        self.destroy()

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
