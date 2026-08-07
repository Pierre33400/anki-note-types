"""Boundary between the engine and the official Anki API."""

from __future__ import annotations

from typing import Protocol

from anki_note_types.model import CompiledNoteType


class AnkiGateway(Protocol):
    """Operations required from an Anki-profile adapter."""

    @property
    def profile_name(self) -> str:
        """Return the target profile's display name."""

    def installed_hash(self, note_type_name: str) -> str | None:
        """Return the recorded compiled hash for a note type."""

    def install(self, note_type: CompiledNoteType) -> None:
        """Install the compiled note type through Anki's official API."""

    def record_installation(self, note_type_name: str, compiled_hash: str) -> None:
        """Persist the installation state in the profile's private storage."""
