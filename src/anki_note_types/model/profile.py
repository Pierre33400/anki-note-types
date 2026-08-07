from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Profile:
    name: str
    installed_hashes: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Profile name cannot be blank.")
        object.__setattr__(self, "installed_hashes", MappingProxyType(dict(self.installed_hashes)))
