"""Stable persistence format for per-profile installation hashes."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class InstallationState:
    engine_version: str
    installed: Mapping[str, str]
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("Unsupported installation-state schema version.")
        object.__setattr__(self, "installed", MappingProxyType(dict(self.installed)))


class InstallationStateStore:
    """Read and write state files selected by the profile adapter."""

    def load(self, path: Path, engine_version: str) -> InstallationState:
        if not path.exists():
            return InstallationState(engine_version, {})
        value = json.loads(path.read_text(encoding="utf-8"))
        installed = {
            name: item["compiledHash"]
            for name, item in value.get("installed", {}).items()
            if isinstance(item, dict) and isinstance(item.get("compiledHash"), str)
        }
        return InstallationState(str(value.get("engineVersion", engine_version)), installed, int(value.get("schemaVersion", 1)))

    def save(self, path: Path, state: InstallationState) -> None:
        payload = {
            "engineVersion": state.engine_version,
            "schemaVersion": state.schema_version,
            "installed": {
                name: {
                    "compiledHash": digest,
                    "installedAt": datetime.now(timezone.utc).isoformat(),
                    "compilerVersion": state.engine_version,
                }
                for name, digest in sorted(state.installed.items())
            },
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
