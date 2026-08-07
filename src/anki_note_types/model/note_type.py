
from __future__ import annotations
from dataclasses import dataclass
from .asset import Asset
from .catalog import Catalog
from .ids import AssetId, TemplateId
from .manifests import NoteTypeManifest
from .stylesheet import Stylesheet
from .template import Template

@dataclass(frozen=True, slots=True)
class NoteType:
    manifest: NoteTypeManifest
    templates: Catalog[TemplateId, Template]
    stylesheet: Stylesheet | None
    assets: Catalog[AssetId, Asset]
