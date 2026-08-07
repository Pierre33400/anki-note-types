"""Discover profile directories without coupling the engine to Anki's UI."""

from __future__ import annotations

from pathlib import Path

from anki_note_types.model import Profile


class ProfileManager:
    """Discover profile directories under a caller-supplied Anki data root."""

    def discover(self, profiles_root: Path) -> tuple[Profile, ...]:
        if not profiles_root.exists():
            return ()
        return tuple(
            Profile(path.name, {})
            for path in sorted(profiles_root.iterdir())
            if path.is_dir()
        )
