
from __future__ import annotations
from dataclasses import dataclass
from .manifests import TemplateManifest

@dataclass(frozen=True, slots=True)
class Template:
    manifest: TemplateManifest
    front: str
    back: str
