"""Determine the assets required by a compiled workspace."""

from __future__ import annotations

from anki_note_types.model import Asset, CompiledWorkspace, Workspace


class AssetCollector:
    """Return source assets in stable logical-path order.

    Asset references are intentionally format-agnostic at this stage; copying is
    delegated to the Anki adapter.
    """

    def collect(self, source: Workspace, compiled: CompiledWorkspace) -> tuple[Asset, ...]:
        compiled_names = {note_type.name for note_type in compiled.note_types}
        if not compiled_names:
            return ()
        return tuple(sorted(source.assets, key=lambda asset: str(asset.id)))
