"""Export history viewer dialog for Gmail to NotebookLM GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional

try:
    from gmail_to_notebooklm.history import ExportHistory
    HISTORY_AVAILABLE = True
except ImportError:
    HISTORY_AVAILABLE = False


class HistoryDialog(tk.Toplevel):
    """Dialog for viewing export history.

    Displays:
    - List of recent exports
    - Export statistics
    - Re-export functionality
    """

    def __init__(self, parent):
        """Initialize history dialog.

        Args:
            parent: Parent Tkinter widget
        """
        super().__init__(parent)
        self.parent = parent

        # Configure window
        self.title("Export History")
        self.geometry("900x600")

        # Center on parent
        self.transient(parent)

        if not HISTORY_AVAILABLE:
            self._show_unavailable()
            return

        # State
        self.history = ExportHistory()
        self.selected_export_id = None

        # Build UI
        self._create_widgets()
        self._load_history()

    def _show_unavailable(self):
        """Show message when history is unavailable."""
        message = ttk.Label(
            self,
            text="Export history is not available.\nHistory tracking requires Python 3.9+.",
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
            text="Export History",
            font=("Segoe UI", 12, "bold")
        )
        title.pack(pady=(0, 10))

        # Statistics panel
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.stats_label = ttk.Label(
            stats_frame,
            text="Loading statistics...",
            font=("Segoe UI", 9)
        )
        self.stats_label.pack()

        # History list
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("timestamp", "label", "files", "duration", "status"),
            show="headings",
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=self.tree.yview)

        # Configure columns
        self.tree.heading("timestamp", text="Date/Time")
        self.tree.heading("label", text="Label/Query")
        self.tree.heading("files", text="Files")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("status", text="Status")

        self.tree.column("timestamp", width=150)
        self.tree.column("label", width=250)
        self.tree.column("files", width=80, anchor=tk.CENTER)
        self.tree.column("duration", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", lambda e: self._view_details())

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        self.view_button = ttk.Button(
            button_frame,
            text="View Details",
            command=self._view_details,
            state=tk.DISABLED
        )
        self.view_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = ttk.Button(
            button_frame,
            text="Delete",
            command=self._delete_export,
            state=tk.DISABLED
        )
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))

        refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=self._load_history
        )
        refresh_button.pack(side=tk.LEFT)

        close_button = ttk.Button(
            button_frame,
            text="Close",
            command=self.destroy
        )
        close_button.pack(side=tk.RIGHT)

    def _load_history(self):
        """Load export history from database."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load exports
        exports = self.history.get_recent_exports(limit=100)

        for export in exports:
            # Format timestamp
            ts = export["timestamp"]
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")

            # Format label/query
            if export["label"]:
                label_text = export["label"]
                if export["query"]:
                    label_text += f" ({export['query'][:30]}...)" if len(export["query"]) > 30 else f" ({export['query']})"
            elif export["query"]:
                label_text = export["query"][:50] + "..." if len(export["query"]) > 50 else export["query"]
            else:
                label_text = "N/A"

            # Format duration
            duration = f"{export['duration_seconds']:.1f}s"

            # Format status
            status = "✓ Success" if export["success"] else "✗ Failed"

            # Insert item
            item_id = self.tree.insert(
                "",
                tk.END,
                values=(ts, label_text, export["files_created"], duration, status),
                tags=(export["id"],)
            )

        # Load statistics
        stats = self.history.get_statistics()
        stats_text = (
            f"Total Exports: {stats['total_exports']} | "
            f"Total Files: {stats['total_files']} | "
            f"Success Rate: {stats['success_rate']:.1f}% | "
            f"Avg Duration: {stats['avg_duration_seconds']:.1f}s"
        )
        self.stats_label.config(text=stats_text)

    def _on_select(self, event):
        """Handle tree selection event."""
        selection = self.tree.selection()
        if selection:
            # Enable buttons
            self.view_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)

            # Get export ID from tags
            item_id = selection[0]
            tags = self.tree.item(item_id, "tags")
            if tags:
                self.selected_export_id = int(tags[0])
        else:
            self.view_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_export_id = None

    def _view_details(self):
        """Show detailed view of selected export."""
        if not self.selected_export_id:
            return

        export = self.history.get_export_details(self.selected_export_id)
        if not export:
            messagebox.showerror("Error", "Export not found")
            return

        # Create details window
        details = tk.Toplevel(self)
        details.title(f"Export Details - ID {export['id']}")
        details.geometry("700x500")
        details.transient(self)

        # Main frame
        main = ttk.Frame(details, padding="20")
        main.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main,
            text=f"Export ID: {export['id']}",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(0, 10))

        # Details
        details_frame = ttk.LabelFrame(main, text="Export Information", padding="10")
        details_frame.pack(fill=tk.X, pady=(0, 10))

        info_text = f"""
Timestamp: {export['timestamp']}
Label: {export['label'] or 'N/A'}
Query: {export['query'] or 'N/A'}
Files Created: {export['files_created']}
Duration: {export['duration_seconds']:.2f} seconds
Output Directory: {export['output_dir']}
Status: {'Success' if export['success'] else 'Failed'}
Errors: {export['error_count']}
        """.strip()

        ttk.Label(
            details_frame,
            text=info_text,
            justify=tk.LEFT,
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W)

        # Files list
        if export.get("files"):
            files_frame = ttk.LabelFrame(main, text=f"Files ({len(export['files'])})", padding="10")
            files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            # Create listbox with scrollbar
            scroll = ttk.Scrollbar(files_frame)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

            files_list = tk.Listbox(
                files_frame,
                yscrollcommand=scroll.set,
                font=("Consolas", 9)
            )
            scroll.config(command=files_list.yview)
            files_list.pack(fill=tk.BOTH, expand=True)

            for file in export["files"]:
                files_list.insert(tk.END, f"{file['filename']} - {file['subject']}")

        # Close button
        ttk.Button(
            main,
            text="Close",
            command=details.destroy
        ).pack()

    def _delete_export(self):
        """Delete selected export from history."""
        if not self.selected_export_id:
            return

        if messagebox.askyesno(
            "Delete Export?",
            f"Are you sure you want to delete this export from history?\n\n"
            f"This will not delete the exported files, only the history record."
        ):
            if self.history.delete_export(self.selected_export_id):
                messagebox.showinfo("Deleted", "Export deleted from history")
                self._load_history()
            else:
                messagebox.showerror("Error", "Failed to delete export")
