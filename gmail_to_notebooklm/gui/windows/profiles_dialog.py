"""Export profiles management dialog for Gmail to NotebookLM GUI."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Dict

try:
    from gmail_to_notebooklm.profiles import ProfileManager, ExportProfile
    PROFILES_AVAILABLE = True
except ImportError:
    PROFILES_AVAILABLE = False


class ProfilesDialog(tk.Toplevel):
    """Dialog for managing export profiles.

    Allows users to:
    - View saved profiles
    - Create new profiles
    - Edit existing profiles
    - Delete profiles
    - Load profile into main window
    """

    def __init__(self, parent, on_load_callback=None):
        """Initialize profiles dialog.

        Args:
            parent: Parent Tkinter widget
            on_load_callback: Callback function when profile is loaded
        """
        super().__init__(parent)
        self.parent = parent
        self.on_load_callback = on_load_callback

        # Configure window
        self.title("Export Profiles")
        self.geometry("800x600")

        # Center on parent
        self.transient(parent)

        if not PROFILES_AVAILABLE:
            self._show_unavailable()
            return

        # State
        self.profile_manager = ProfileManager()
        self.selected_profile_name = None

        # Build UI
        self._create_widgets()
        self._load_profiles()

    def _show_unavailable(self):
        """Show message when profiles are unavailable."""
        message = ttk.Label(
            self,
            text="Export profiles are not available.",
            justify=tk.CENTER,
            font=("Segoe UI", 10)
        )
        message.pack(expand=True)

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy
        )
        close_button.pack(pady=20)

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text="Export Profiles",
            font=("Segoe UI", 12, "bold")
        )
        title.pack(pady=(0, 5))

        subtitle = ttk.Label(
            main_frame,
            text="Save and load common export configurations",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        subtitle.pack(pady=(0, 15))

        # Content frame with list and details
        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Left: Profile list
        list_frame = ttk.LabelFrame(content, text="Saved Profiles", padding="10")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Listbox with scrollbar
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.profiles_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scroll.set,
            font=("Segoe UI", 10)
        )
        scroll.config(command=self.profiles_listbox.yview)
        self.profiles_listbox.pack(fill=tk.BOTH, expand=True)
        self.profiles_listbox.bind("<<ListboxSelect>>", self._on_select)
        self.profiles_listbox.bind("<Double-1>", lambda e: self._load_profile())

        # Right: Profile details
        details_frame = ttk.LabelFrame(content, text="Profile Details", padding="10")
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Profile info
        self.profile_name_label = ttk.Label(
            details_frame,
            text="No profile selected",
            font=("Segoe UI", 10, "bold")
        )
        self.profile_name_label.pack(anchor=tk.W, pady=(0, 5))

        self.profile_desc_label = ttk.Label(
            details_frame,
            text="",
            font=("Segoe UI", 9),
            foreground="gray",
            wraplength=300
        )
        self.profile_desc_label.pack(anchor=tk.W, pady=(0, 10))

        # Settings display
        settings_label = ttk.Label(
            details_frame,
            text="Settings:",
            font=("Segoe UI", 9, "bold")
        )
        settings_label.pack(anchor=tk.W, pady=(0, 5))

        # Text widget for settings
        text_scroll = ttk.Scrollbar(details_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.settings_text = tk.Text(
            details_frame,
            height=15,
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        text_scroll.config(command=self.settings_text.yview)
        self.settings_text.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        # Left side buttons
        self.load_button = ttk.Button(
            button_frame,
            text="Load Profile",
            command=self._load_profile,
            state=tk.DISABLED
        )
        self.load_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = ttk.Button(
            button_frame,
            text="Delete",
            command=self._delete_profile,
            state=tk.DISABLED
        )
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))

        self.rename_button = ttk.Button(
            button_frame,
            text="Rename",
            command=self._rename_profile,
            state=tk.DISABLED
        )
        self.rename_button.pack(side=tk.LEFT, padx=(0, 5))

        # Right side buttons
        new_button = ttk.Button(
            button_frame,
            text="New Profile",
            command=self._new_profile
        )
        new_button.pack(side=tk.LEFT)

        close_button = ttk.Button(
            button_frame,
            text="Close",
            command=self.destroy
        )
        close_button.pack(side=tk.RIGHT)

    def _load_profiles(self):
        """Load profiles from manager."""
        self.profiles_listbox.delete(0, tk.END)

        profiles = self.profile_manager.list_profiles()
        for profile in profiles:
            self.profiles_listbox.insert(tk.END, profile.name)

        # Show message if no profiles
        if not profiles:
            self.profiles_listbox.insert(tk.END, "(No saved profiles)")
            self.profiles_listbox.config(state=tk.DISABLED)
        else:
            self.profiles_listbox.config(state=tk.NORMAL)

    def _on_select(self, event):
        """Handle profile selection."""
        selection = self.profiles_listbox.curselection()
        if not selection:
            self.load_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.rename_button.config(state=tk.DISABLED)
            self.profile_name_label.config(text="No profile selected")
            self.profile_desc_label.config(text="")
            self._update_settings_display({})
            return

        # Get selected profile
        self.selected_profile_name = self.profiles_listbox.get(selection[0])
        if self.selected_profile_name == "(No saved profiles)":
            return

        profile = self.profile_manager.get_profile(self.selected_profile_name)
        if not profile:
            return

        # Enable buttons
        self.load_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)
        self.rename_button.config(state=tk.NORMAL)

        # Update details
        self.profile_name_label.config(text=profile.name)
        self.profile_desc_label.config(text=profile.description or "No description")
        self._update_settings_display(profile.settings)

    def _update_settings_display(self, settings: Dict):
        """Update settings text display.

        Args:
            settings: Settings dictionary
        """
        self.settings_text.config(state=tk.NORMAL)
        self.settings_text.delete("1.0", tk.END)

        if not settings:
            self.settings_text.insert("1.0", "No settings")
        else:
            for key, value in settings.items():
                self.settings_text.insert(tk.END, f"{key}: {value}\n")

        self.settings_text.config(state=tk.DISABLED)

    def _load_profile(self):
        """Load selected profile into main window."""
        if not self.selected_profile_name:
            return

        profile = self.profile_manager.get_profile(self.selected_profile_name)
        if not profile:
            messagebox.showerror("Error", "Profile not found")
            return

        if self.on_load_callback:
            self.on_load_callback(profile.settings)
            messagebox.showinfo("Profile Loaded", f"Profile '{profile.name}' loaded successfully!")
            self.destroy()
        else:
            messagebox.showinfo("Profile Loaded", f"Profile '{profile.name}' settings:\n\n{profile.settings}")

    def _delete_profile(self):
        """Delete selected profile."""
        if not self.selected_profile_name:
            return

        if messagebox.askyesno(
            "Delete Profile?",
            f"Are you sure you want to delete the profile '{self.selected_profile_name}'?"
        ):
            if self.profile_manager.delete_profile(self.selected_profile_name):
                messagebox.showinfo("Deleted", "Profile deleted successfully")
                self._load_profiles()
            else:
                messagebox.showerror("Error", "Failed to delete profile")

    def _rename_profile(self):
        """Rename selected profile."""
        if not self.selected_profile_name:
            return

        new_name = simpledialog.askstring(
            "Rename Profile",
            f"Enter new name for profile '{self.selected_profile_name}':",
            parent=self
        )

        if not new_name:
            return

        try:
            if self.profile_manager.rename_profile(self.selected_profile_name, new_name):
                messagebox.showinfo("Renamed", "Profile renamed successfully")
                self._load_profiles()
            else:
                messagebox.showerror("Error", "Failed to rename profile")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _new_profile(self):
        """Create new profile from current settings."""
        # Ask for profile name
        name = simpledialog.askstring(
            "New Profile",
            "Enter profile name:",
            parent=self
        )

        if not name:
            return

        # Ask for description
        description = simpledialog.askstring(
            "Profile Description",
            "Enter profile description (optional):",
            parent=self
        )

        # For now, create empty profile
        # In full implementation, would get settings from main window
        settings = {
            "label": "",
            "output_dir": "./output",
            "organize_by_date": False,
            "create_index": False,
        }

        profile = ExportProfile(name=name, settings=settings, description=description or "")

        try:
            self.profile_manager.save_profile(profile)
            messagebox.showinfo("Created", "Profile created successfully!\n\nEdit the profile settings in the main window.")
            self._load_profiles()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
