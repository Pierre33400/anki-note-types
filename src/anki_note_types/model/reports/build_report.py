from __future__ import annotations

from dataclasses import dataclass, field

from ..diagnostic import Diagnostic


@dataclass(frozen=True, slots=True)
class BuildReport:
    output_path: str | None = None
    diagnostics: tuple[Diagnostic, ...] = field(default_factory=tuple)

    @property
    def success(self) -> bool:
        return not any(item.is_error for item in self.diagnostics)
