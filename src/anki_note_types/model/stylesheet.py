
from __future__ import annotations
from dataclasses import dataclass
from .ids import StylesheetId

@dataclass(frozen=True, slots=True)
class Stylesheet:
    id: StylesheetId
    content: str
