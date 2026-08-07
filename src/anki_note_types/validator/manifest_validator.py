"""Validation of the versioned JSON manifest contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from anki_note_types.model import Diagnostic


class ManifestValidator:
    """Validate JSON objects without requiring a third-party JSON Schema runtime."""

    def validate_note_type(self, value: Mapping[str, Any]) -> tuple[Diagnostic, ...]:
        return self._validate(value, {"schemaVersion", "name", "stylesheet", "fields"}, {"name", "stylesheet", "fields"})

    def validate_template(self, value: Mapping[str, Any]) -> tuple[Diagnostic, ...]:
        return self._validate(value, {"schemaVersion", "name"}, {"name"})

    @staticmethod
    def _validate(value: Mapping[str, Any], allowed: set[str], required: set[str]) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []
        if value.get("schemaVersion") != 1:
            diagnostics.append(Diagnostic("invalid-schema-version", "schemaVersion must be 1."))
        for key in sorted(required):
            field = value.get(key)
            if key == "fields":
                valid = isinstance(field, list) and field and all(isinstance(item, str) and item.strip() for item in field)
            else:
                valid = isinstance(field, str) and field.strip()
            if not valid:
                diagnostics.append(Diagnostic("invalid-manifest-field", f"'{key}' is required and cannot be empty."))
        for key in sorted(set(value) - allowed):
            diagnostics.append(Diagnostic("unknown-manifest-field", f"Unknown manifest field '{key}'."))
        return tuple(diagnostics)
