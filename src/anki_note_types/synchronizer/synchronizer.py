"""Synchronize compiled note types through an injected Anki adapter."""

from __future__ import annotations

from anki_note_types.model import CompiledWorkspace
from anki_note_types.model.reports import SyncReport

from .anki_gateway import AnkiGateway


class Synchronizer:
    """Install only note types whose compiled hashes changed."""

    def sync(self, workspace: CompiledWorkspace, profile: AnkiGateway, *, dry_run: bool = False) -> SyncReport:
        changed = False
        for note_type in workspace.note_types:
            if profile.installed_hash(note_type.name) == note_type.compiled_hash:
                continue
            changed = True
            if not dry_run:
                profile.install(note_type)
                profile.record_installation(note_type.name, note_type.compiled_hash)
        if changed and not dry_run:
            return SyncReport(updated_profiles=(profile.profile_name,))
        return SyncReport(skipped_profiles=(profile.profile_name,))
