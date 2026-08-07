
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StylesheetId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("StylesheetId cannot be empty.")

    def __str__(self) -> str:
        return self.value
