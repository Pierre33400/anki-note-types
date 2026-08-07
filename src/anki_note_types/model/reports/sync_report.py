from __future__ import annotations

from dataclasses import dataclass, field

from ..diagnostic import Diagnostic


@dataclass(frozen=True, slots=True)
class SyncReport:
    updated_profiles: tuple[str, ...] = field(default_factory=tuple)
    skipped_profiles: tuple[str, ...] = field(default_factory=tuple)
    diagnostics: tuple[Diagnostic, ...] = field(default_factory=tuple)

    @property
    def success(self) -> bool:
        return not any(item.is_error for item in self.diagnostics)
