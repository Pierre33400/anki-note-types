
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TemplateId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("TemplateId cannot be empty.")

    def __str__(self) -> str:
        return self.value
