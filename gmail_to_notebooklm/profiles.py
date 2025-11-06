"""Export profile management for saving common configurations."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class ExportProfile:
    """Represents a saved export configuration."""

    def __init__(
        self,
        name: str,
        settings: Dict,
        description: str = "",
    ):
        """Initialize export profile.

        Args:
            name: Profile name
            settings: Export settings dictionary
            description: Profile description
        """
        self.name = name
        self.settings = settings
        self.description = description

    def to_dict(self) -> Dict:
        """Convert profile to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "settings": self.settings,
        }

    @staticmethod
    def from_dict(data: Dict) -> "ExportProfile":
        """Create profile from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            ExportProfile instance
        """
        return ExportProfile(
            name=data["name"],
            settings=data["settings"],
            description=data.get("description", ""),
        )


class ProfileManager:
    """Manage export profiles with JSON storage."""

    def __init__(self, profiles_file: str = "export_profiles.json"):
        """Initialize profile manager.

        Args:
            profiles_file: Path to profiles JSON file
        """
        self.profiles_file = Path(profiles_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create profiles file if it doesn't exist."""
        if not self.profiles_file.exists():
            self.profiles_file.write_text(json.dumps([], indent=2))

    def _load_profiles(self) -> List[ExportProfile]:
        """Load all profiles from file.

        Returns:
            List of ExportProfile instances
        """
        try:
            data = json.loads(self.profiles_file.read_text())
            return [ExportProfile.from_dict(p) for p in data]
        except Exception:
            return []

    def _save_profiles(self, profiles: List[ExportProfile]):
        """Save profiles to file.

        Args:
            profiles: List of ExportProfile instances
        """
        data = [p.to_dict() for p in profiles]
        self.profiles_file.write_text(json.dumps(data, indent=2))

    def list_profiles(self) -> List[ExportProfile]:
        """Get all saved profiles.

        Returns:
            List of ExportProfile instances
        """
        return self._load_profiles()

    def get_profile(self, name: str) -> Optional[ExportProfile]:
        """Get profile by name.

        Args:
            name: Profile name

        Returns:
            ExportProfile instance or None if not found
        """
        profiles = self._load_profiles()
        for profile in profiles:
            if profile.name == name:
                return profile
        return None

    def save_profile(self, profile: ExportProfile, overwrite: bool = False) -> bool:
        """Save export profile.

        Args:
            profile: ExportProfile instance
            overwrite: Allow overwriting existing profile

        Returns:
            True if saved, False if already exists and not overwriting

        Raises:
            ValueError: If profile with same name exists and overwrite=False
        """
        profiles = self._load_profiles()

        # Check if profile exists
        existing_index = None
        for i, p in enumerate(profiles):
            if p.name == profile.name:
                existing_index = i
                break

        if existing_index is not None:
            if not overwrite:
                raise ValueError(f"Profile '{profile.name}' already exists")
            profiles[existing_index] = profile
        else:
            profiles.append(profile)

        self._save_profiles(profiles)
        return True

    def delete_profile(self, name: str) -> bool:
        """Delete profile by name.

        Args:
            name: Profile name

        Returns:
            True if deleted, False if not found
        """
        profiles = self._load_profiles()
        initial_count = len(profiles)

        profiles = [p for p in profiles if p.name != name]

        if len(profiles) < initial_count:
            self._save_profiles(profiles)
            return True

        return False

    def rename_profile(self, old_name: str, new_name: str) -> bool:
        """Rename a profile.

        Args:
            old_name: Current profile name
            new_name: New profile name

        Returns:
            True if renamed, False if not found

        Raises:
            ValueError: If new name already exists
        """
        profiles = self._load_profiles()

        # Check if new name exists
        for p in profiles:
            if p.name == new_name:
                raise ValueError(f"Profile '{new_name}' already exists")

        # Find and rename
        renamed = False
        for profile in profiles:
            if profile.name == old_name:
                profile.name = new_name
                renamed = True
                break

        if renamed:
            self._save_profiles(profiles)

        return renamed

    def import_from_history(self, history_settings: Dict, name: str, description: str = "") -> ExportProfile:
        """Create profile from history export settings.

        Args:
            history_settings: Settings from export history
            name: New profile name
            description: Profile description

        Returns:
            New ExportProfile instance (not saved)
        """
        # Filter out runtime-specific settings
        profile_settings = {
            k: v for k, v in history_settings.items()
            if k not in ["credentials_path", "token_path", "timestamp"]
        }

        return ExportProfile(
            name=name,
            settings=profile_settings,
            description=description,
        )

    def get_default_profiles(self) -> List[ExportProfile]:
        """Get built-in default profiles.

        Returns:
            List of default ExportProfile instances
        """
        return [
            ExportProfile(
                name="Daily Inbox",
                description="Export today's inbox emails",
                settings={
                    "label": "INBOX",
                    "after": "today",
                    "output_dir": "./exports/inbox",
                    "organize_by_date": True,
                    "create_index": True,
                },
            ),
            ExportProfile(
                name="Weekly Reports",
                description="Export last 7 days from Work label",
                settings={
                    "label": "Work",
                    "after": "7 days ago",
                    "output_dir": "./exports/reports",
                    "organize_by_date": True,
                    "create_index": True,
                },
            ),
            ExportProfile(
                name="Important Starred",
                description="Export starred important emails",
                settings={
                    "label": "STARRED",
                    "query": "is:important",
                    "output_dir": "./exports/important",
                    "create_index": True,
                },
            ),
        ]

    def install_default_profiles(self, skip_existing: bool = True):
        """Install built-in default profiles.

        Args:
            skip_existing: Don't overwrite existing profiles
        """
        defaults = self.get_default_profiles()
        existing_names = {p.name for p in self._load_profiles()}

        for profile in defaults:
            if skip_existing and profile.name in existing_names:
                continue

            self.save_profile(profile, overwrite=not skip_existing)
