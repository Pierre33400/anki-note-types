
from __future__ import annotations
from dataclasses import dataclass
from .ids import PartialId

@dataclass(frozen=True, slots=True)
class Partial:
    id: PartialId
    content: str
