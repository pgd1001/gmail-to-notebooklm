"""Export progress dialog for Gmail to NotebookLM GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Dict
import threading

from gmail_to_notebooklm.core import ExportEngine, ExportResult, ProgressUpdate


class ExportDialog(tk.Toplevel):
    """Dialog showing export progress.

    Displays:
    - Current step (1-5)
    - Step description
    - Progress bar
    - Percentage complete
    - Cancel button
    """

    def __init__(self, parent, settings: Dict):
        """Initialize export dialog.

        Args:
            parent: Parent Tkinter widget
            settings: Export settings dictionary
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = settings

        # Configure window
        self.title("Exporting Emails")
        self.geometry("500x300")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        # State
        self.export_engine: ExportEngine = None
        self.export_result: ExportResult = None
        self.cancelled = False

        # Build UI
        self._create_widgets()

        # Prevent closing during export
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text="Exporting Emails to Markdown",
            font=("Segoe UI", 11, "bold")
        )
        title.pack(pady=(0, 20))

        # Current step
        self.step_label = ttk.Label(
            main_frame,
            text="Starting export...",
            font=("Segoe UI", 9)
        )
        self.step_label.pack(pady=(0, 10))

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
            length=400
        )
        self.progress_bar.pack(pady=(0, 10))

        # Percentage label
        self.percentage_label = ttk.Label(
            main_frame,
            text="0%",
            font=("Segoe UI", 9)
        )
        self.percentage_label.pack(pady=(0, 10))

        # Detail label (for sub-progress like "Fetching 5/100")
        self.detail_label = ttk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 8),
            foreground="gray"
        )
        self.detail_label.pack(pady=(0, 20))

        # Status label (for errors/warnings)
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 8),
            foreground="orange",
            wraplength=450
        )
        self.status_label.pack(pady=(0, 10))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel_export
        )
        self.cancel_button.pack(side=tk.RIGHT)

        self.close_button = ttk.Button(
            button_frame,
            text="Close",
            command=self._close_dialog,
            state=tk.DISABLED
        )
        self.close_button.pack(side=tk.RIGHT, padx=(0, 10))

    def _on_progress(self, update: ProgressUpdate):
        """Handle progress update from export engine.

        Args:
            update: Progress information
        """
        # Update UI on main thread
        self.after(0, self._update_progress_ui, update)

    def _update_progress_ui(self, update: ProgressUpdate):
        """Update progress UI elements.

        Args:
            update: Progress information
        """
        # Update step label
        self.step_label.config(
            text=f"Step {update.step}/{update.total_steps}: {update.message}"
        )

        # Calculate overall progress (each step is 20% of total)
        base_progress = ((update.step - 1) / update.total_steps) * 100
        step_progress = (update.percent / update.total_steps)
        total_progress = base_progress + step_progress

        # Update progress bar
        self.progress_var.set(total_progress)
        self.percentage_label.config(text=f"{int(total_progress)}%")

        # Update detail label if we have current/total info
        if update.total > 0:
            self.detail_label.config(
                text=f"{update.current} of {update.total} items"
            )
        else:
            self.detail_label.config(text="")

    def _on_status(self, message: str):
        """Handle status message from export engine.

        Args:
            message: Status message
        """
        # Update UI on main thread
        self.after(0, self._update_status_ui, message)

    def _update_status_ui(self, message: str):
        """Update status label.

        Args:
            message: Status message
        """
        self.status_label.config(text=message)

    def _on_error(self, error: Exception) -> bool:
        """Handle error from export engine.

        Args:
            error: Exception that occurred

        Returns:
            True to retry, False to abort
        """
        # Show error dialog on main thread
        # Return False (don't retry) for now
        self.after(0, messagebox.showerror, "Export Error", str(error))
        return False

    def start_export(self):
        """Start the export process in background thread."""
        def export_task():
            try:
                # Create engine with callbacks
                self.export_engine = ExportEngine(
                    progress_callback=self._on_progress,
                    status_callback=self._on_status,
                    error_callback=self._on_error
                )

                # Run export
                self.export_result = self.export_engine.export(self.settings)

                # Show completion on main thread
                self.after(0, self._on_export_complete)

            except Exception as e:
                # Show error on main thread
                self.after(0, self._on_export_error, e)

        # Start background thread
        thread = threading.Thread(target=export_task, daemon=True)
        thread.start()

    def _on_export_complete(self):
        """Handle export completion."""
        result = self.export_result

        # Update UI
        self.cancel_button.config(state=tk.DISABLED)
        self.close_button.config(state=tk.NORMAL)

        if result.success:
            # Success
            self.step_label.config(text="Export completed successfully!")
            self.progress_var.set(100)
            self.percentage_label.config(text="100%")

            # Show summary
            if result.stats.get("consolidation_mode"):
                summary = (
                    f"Created consolidated document\n"
                    f"Filename: {result.stats.get('consolidation_filename', 'export.md')}\n"
                    f"Output directory: {result.output_dir}\n"
                    f"Duration: {result.duration_seconds:.1f} seconds"
                )
            else:
                summary = (
                    f"Created {result.files_created} files\n"
                    f"Output directory: {result.output_dir}\n"
                    f"Duration: {result.duration_seconds:.1f} seconds"
                )

            if result.errors:
                summary += f"\n\nWarnings: {len(result.errors)} files had errors"

            messagebox.showinfo("Export Complete", summary)

        else:
            # Failed or cancelled
            if result.errors and "cancelled" in result.errors[0].lower():
                self.step_label.config(text="Export cancelled")
                self.status_label.config(
                    text="Export was cancelled by user",
                    foreground="orange"
                )
            else:
                self.step_label.config(text="Export failed")
                self.status_label.config(
                    text=f"Errors: {', '.join(result.errors[:3])}",
                    foreground="red"
                )
                messagebox.showerror(
                    "Export Failed",
                    f"Export failed with errors:\n\n{chr(10).join(result.errors[:5])}"
                )

    def _on_export_error(self, error: Exception):
        """Handle unexpected export error.

        Args:
            error: Exception that occurred
        """
        self.step_label.config(text="Export failed")
        self.status_label.config(text=str(error), foreground="red")

        self.cancel_button.config(state=tk.DISABLED)
        self.close_button.config(state=tk.NORMAL)

        messagebox.showerror("Export Error", f"Export failed:\n\n{error}")

    def _cancel_export(self):
        """Cancel the export process."""
        if self.export_engine and not self.cancelled:
            self.cancelled = True
            self.export_engine.cancel()
            self.cancel_button.config(state=tk.DISABLED, text="Cancelling...")
            self.status_label.config(
                text="Cancelling export...",
                foreground="orange"
            )

    def _close_dialog(self):
        """Close the dialog."""
        self.destroy()

    def _on_close(self):
        """Handle window close button."""
        if self.close_button["state"] == tk.NORMAL:
            self._close_dialog()
        else:
            # Export in progress, ask to cancel
            if messagebox.askyesno(
                "Cancel Export?",
                "Export is in progress. Do you want to cancel?"
            ):
                self._cancel_export()
