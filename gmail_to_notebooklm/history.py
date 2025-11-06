"""Export history tracking with SQLite database."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ExportHistory:
    """Manage export history database.

    Tracks all exports with metadata for:
    - Export replay
    - Analytics
    - Audit trail
    """

    def __init__(self, db_path: str = "export_history.db"):
        """Initialize history database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Exports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                label TEXT,
                query TEXT,
                files_created INTEGER,
                duration_seconds REAL,
                output_dir TEXT,
                settings_json TEXT,
                success INTEGER,
                error_count INTEGER
            )
        """)

        # Export files table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS export_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                export_id INTEGER,
                email_id TEXT,
                filename TEXT,
                subject TEXT,
                from_addr TEXT,
                to_addr TEXT,
                date DATETIME,
                FOREIGN KEY (export_id) REFERENCES exports(id) ON DELETE CASCADE
            )
        """)

        # Create indexes for common queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_exports_timestamp
            ON exports(timestamp DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_export_files_export_id
            ON export_files(export_id)
        """)

        conn.commit()
        conn.close()

    def add_export(
        self,
        label: Optional[str],
        query: Optional[str],
        files_created: int,
        duration_seconds: float,
        output_dir: str,
        settings: Dict,
        success: bool,
        error_count: int = 0,
        files: Optional[List[Dict]] = None,
    ) -> int:
        """Add export record to history.

        Args:
            label: Gmail label
            query: Gmail query
            files_created: Number of files created
            duration_seconds: Export duration
            output_dir: Output directory path
            settings: Export settings dictionary
            success: Whether export succeeded
            error_count: Number of errors
            files: List of file metadata dicts

        Returns:
            Export ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Insert export record
        cursor.execute("""
            INSERT INTO exports (
                label, query, files_created, duration_seconds,
                output_dir, settings_json, success, error_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            label,
            query,
            files_created,
            duration_seconds,
            output_dir,
            json.dumps(settings),
            1 if success else 0,
            error_count,
        ))

        export_id = cursor.lastrowid

        # Insert file records if provided
        if files:
            for file_data in files:
                cursor.execute("""
                    INSERT INTO export_files (
                        export_id, email_id, filename, subject,
                        from_addr, to_addr, date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    export_id,
                    file_data.get("email_id"),
                    file_data.get("filename"),
                    file_data.get("subject"),
                    file_data.get("from"),
                    file_data.get("to"),
                    file_data.get("date"),
                ))

        conn.commit()
        conn.close()

        return export_id

    def get_recent_exports(self, limit: int = 10) -> List[Dict]:
        """Get recent export records.

        Args:
            limit: Maximum number of records

        Returns:
            List of export dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id, timestamp, label, query, files_created,
                duration_seconds, output_dir, settings_json,
                success, error_count
            FROM exports
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        exports = []
        for row in cursor.fetchall():
            export = dict(row)
            export["settings"] = json.loads(export["settings_json"])
            del export["settings_json"]
            exports.append(export)

        conn.close()
        return exports

    def get_export_details(self, export_id: int) -> Optional[Dict]:
        """Get detailed export information including files.

        Args:
            export_id: Export ID

        Returns:
            Export dictionary with files list, or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get export record
        cursor.execute("""
            SELECT
                id, timestamp, label, query, files_created,
                duration_seconds, output_dir, settings_json,
                success, error_count
            FROM exports
            WHERE id = ?
        """, (export_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        export = dict(row)
        export["settings"] = json.loads(export["settings_json"])
        del export["settings_json"]

        # Get file records
        cursor.execute("""
            SELECT
                email_id, filename, subject, from_addr,
                to_addr, date
            FROM export_files
            WHERE export_id = ?
            ORDER BY date DESC
        """, (export_id,))

        export["files"] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return export

    def delete_export(self, export_id: int) -> bool:
        """Delete export record and associated files.

        Args:
            export_id: Export ID

        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM exports WHERE id = ?", (export_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    def get_statistics(self) -> Dict:
        """Get export statistics.

        Returns:
            Dictionary with statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Total exports
        cursor.execute("SELECT COUNT(*) FROM exports")
        stats["total_exports"] = cursor.fetchone()[0]

        # Total files
        cursor.execute("SELECT SUM(files_created) FROM exports")
        total_files = cursor.fetchone()[0]
        stats["total_files"] = total_files if total_files else 0

        # Success rate
        cursor.execute("SELECT COUNT(*) FROM exports WHERE success = 1")
        successful = cursor.fetchone()[0]
        stats["successful_exports"] = successful
        stats["success_rate"] = (successful / stats["total_exports"] * 100) if stats["total_exports"] > 0 else 0

        # Average duration
        cursor.execute("SELECT AVG(duration_seconds) FROM exports WHERE success = 1")
        avg_duration = cursor.fetchone()[0]
        stats["avg_duration_seconds"] = avg_duration if avg_duration else 0

        # Most used label
        cursor.execute("""
            SELECT label, COUNT(*) as count
            FROM exports
            WHERE label IS NOT NULL
            GROUP BY label
            ORDER BY count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            stats["most_used_label"] = row[0]
            stats["most_used_label_count"] = row[1]
        else:
            stats["most_used_label"] = None
            stats["most_used_label_count"] = 0

        conn.close()
        return stats

    def search_exports(
        self,
        label: Optional[str] = None,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        success_only: bool = False,
    ) -> List[Dict]:
        """Search export history.

        Args:
            label: Filter by label
            after: Filter by date after
            before: Filter by date before
            success_only: Only successful exports

        Returns:
            List of matching export dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        conditions = []
        params = []

        if label:
            conditions.append("label = ?")
            params.append(label)

        if after:
            conditions.append("timestamp >= ?")
            params.append(after.isoformat())

        if before:
            conditions.append("timestamp <= ?")
            params.append(before.isoformat())

        if success_only:
            conditions.append("success = 1")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        cursor.execute(f"""
            SELECT
                id, timestamp, label, query, files_created,
                duration_seconds, output_dir, settings_json,
                success, error_count
            FROM exports
            WHERE {where_clause}
            ORDER BY timestamp DESC
        """, params)

        exports = []
        for row in cursor.fetchall():
            export = dict(row)
            export["settings"] = json.loads(export["settings_json"])
            del export["settings_json"]
            exports.append(export)

        conn.close()
        return exports
