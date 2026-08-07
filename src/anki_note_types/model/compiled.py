from __future__ import annotations

from dataclasses import dataclass

from .catalog import Catalog
from .ids import NoteTypeId, TemplateId


@dataclass(frozen=True, slots=True)
class CompiledTemplate:
    name: str
    front: str
    back: str


@dataclass(frozen=True, slots=True)
class CompiledNoteType:
    name: str
    fields: tuple[str, ...]
    stylesheet: str
    templates: Catalog[TemplateId, CompiledTemplate]
    compiled_hash: str


@dataclass(frozen=True, slots=True)
class CompiledWorkspace:
    note_types: Catalog[NoteTypeId, CompiledNoteType]
