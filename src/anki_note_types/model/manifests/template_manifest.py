
from __future__ import annotations
from dataclasses import dataclass
from ..ids import TemplateId

@dataclass(frozen=True, slots=True)
class TemplateManifest:
    id: TemplateId
    name: str
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError(f"Unsupported template schema version: {self.schema_version}")
        if not self.name.strip():
            raise ValueError("Template name cannot be blank.")
