
from __future__ import annotations
from dataclasses import dataclass
from pathlib import PurePosixPath

@dataclass(frozen=True, slots=True)
class SourceLocation:
    path: PurePosixPath
    line: int | None = None
    column: int | None = None
