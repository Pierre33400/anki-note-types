
from __future__ import annotations
from dataclasses import dataclass
from ..ids import NoteTypeId, StylesheetId

@dataclass(frozen=True, slots=True)
class NoteTypeManifest:
    id: NoteTypeId
    name: str
    stylesheet: StylesheetId
    fields: tuple[str, ...]
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError(f"Unsupported metadata schema version: {self.schema_version}")
        if not self.name.strip():
            raise ValueError("Note type name cannot be blank.")
        if not self.fields or any(not field.strip() for field in self.fields):
            raise ValueError("A note type must declare at least one field.")
