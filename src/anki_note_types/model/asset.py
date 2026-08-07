
from __future__ import annotations
from dataclasses import dataclass
from pathlib import PurePosixPath
from .ids import AssetId

@dataclass(frozen=True, slots=True)
class Asset:
    id: AssetId
    path: PurePosixPath
