"""Copy declared source assets into a build directory deterministically."""

from __future__ import annotations

import shutil
from pathlib import Path

from anki_note_types.model import Asset, Catalog
from anki_note_types.model.ids import AssetId


class AssetPreparer:
    """Copy assets without altering their bytes or logical paths."""

    def prepare(self, assets: Catalog[AssetId, Asset], source: Path, destination: Path) -> tuple[Path, ...]:
        copied: list[Path] = []
        for asset in sorted(assets, key=lambda item: str(item.id)):
            source_path = source / asset.path
            destination_path = destination / "assets" / asset.path
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, destination_path)
            copied.append(destination_path)
        return tuple(copied)
