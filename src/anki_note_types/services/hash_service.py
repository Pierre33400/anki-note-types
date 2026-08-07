"""Deterministic SHA-256 hashing helpers."""

from __future__ import annotations

import hashlib
from pathlib import Path


class HashService:
    """Calculate SHA-256 hashes using the project's UTF-8 convention."""

    @staticmethod
    def text(value: str) -> str:
        """Return the SHA-256 digest of *value* encoded as UTF-8."""
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def file(path: Path) -> str:
        """Return the SHA-256 digest of a file's raw bytes."""
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(65_536), b""):
                digest.update(chunk)
        return digest.hexdigest()
