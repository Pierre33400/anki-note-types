"""Filesystem-level diagnostics emitted before loading the domain model."""

from __future__ import annotations

import json
from pathlib import Path

from anki_note_types.model import Diagnostic, SourceLocation
from anki_note_types.model.reports import ValidationReport

from .manifest_validator import ManifestValidator


class ProjectValidator:
    """Validate source files, JSON syntax and manifest contracts."""

    def validate(self, project_path: Path) -> ValidationReport:
        diagnostics: list[Diagnostic] = []
        note_types = project_path / "note-types"
        if not note_types.is_dir():
            return ValidationReport((self._diagnostic("missing-note-types-directory", note_types),))
        validator = ManifestValidator()
        for directory in sorted(path for path in note_types.iterdir() if path.is_dir()):
            metadata = self._read_json(directory / "metadata.json", diagnostics)
            if metadata is None:
                continue
            diagnostics.extend(validator.validate_note_type(metadata))
            stylesheet = metadata.get("stylesheet")
            if isinstance(stylesheet, str) and not (project_path / "css" / stylesheet).is_file():
                diagnostics.append(self._diagnostic("missing-stylesheet", project_path / "css" / stylesheet))
            templates = directory / "templates"
            if not templates.is_dir():
                diagnostics.append(self._diagnostic("missing-templates-directory", templates))
                continue
            for template in sorted(path for path in templates.iterdir() if path.is_dir()):
                value = self._read_json(template / "template.json", diagnostics)
                if value is not None:
                    diagnostics.extend(validator.validate_template(value))
                for name in ("front.html", "back.html"):
                    path = template / name
                    if not path.is_file():
                        diagnostics.append(self._diagnostic("missing-template-file", path))
        return ValidationReport(tuple(diagnostics))

    def _read_json(self, path: Path, diagnostics: list[Diagnostic]) -> dict[str, object] | None:
        if not path.is_file():
            diagnostics.append(self._diagnostic("missing-manifest", path))
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            diagnostics.append(self._diagnostic("invalid-json", path))
            return None
        if not isinstance(value, dict):
            diagnostics.append(self._diagnostic("invalid-json-object", path))
            return None
        return value

    @staticmethod
    def _diagnostic(code: str, path: Path) -> Diagnostic:
        return Diagnostic(code, f"{code.replace('-', ' ')}: {path}", location=SourceLocation(path))
