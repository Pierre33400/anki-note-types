
from __future__ import annotations
from dataclasses import dataclass
from .catalog import Catalog
from .asset import Asset
from .ids import AssetId, NoteTypeId, PartialId, StylesheetId
from .note_type import NoteType
from .partial import Partial
from .stylesheet import Stylesheet

@dataclass(frozen=True, slots=True)
class Workspace:
    note_types: Catalog[NoteTypeId, NoteType]
    partials: Catalog[PartialId, Partial]
    stylesheets: Catalog[StylesheetId, Stylesheet]
    assets: Catalog[AssetId, Asset]
