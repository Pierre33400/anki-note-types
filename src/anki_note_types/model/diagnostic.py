from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .source_location import SourceLocation


class DiagnosticLevel(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    level: DiagnosticLevel = DiagnosticLevel.ERROR
    location: SourceLocation | None = None
    suggestion: str | None = None

    @property
    def is_error(self) -> bool:
        return self.level is DiagnosticLevel.ERROR
