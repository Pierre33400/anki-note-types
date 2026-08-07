"""Validation rules for a loaded workspace."""

from __future__ import annotations

import re

from anki_note_types.model import Diagnostic, DiagnosticLevel, Workspace
from anki_note_types.model.reports import ValidationReport

_PARTIAL = re.compile(r"{{>\s*([A-Za-z0-9_.-]+)\s*}}")


class WorkspaceValidator:
    """Validate cross-file references without changing the source model."""

    def validate(self, workspace: Workspace) -> ValidationReport:
        diagnostics = [
            *self._validate_note_type_names(workspace),
            *self._validate_stylesheets(workspace),
            *self._validate_partials(workspace),
        ]
        return ValidationReport(tuple(diagnostics))

    @staticmethod
    def _validate_note_type_names(workspace: Workspace) -> list[Diagnostic]:
        seen: set[str] = set()
        diagnostics: list[Diagnostic] = []
        for note_type in workspace.note_types:
            name = note_type.manifest.name
            if name in seen:
                diagnostics.append(Diagnostic("duplicate-note-type-name", f"Duplicate note type name: {name}"))
            seen.add(name)
        return diagnostics

    @staticmethod
    def _validate_stylesheets(workspace: Workspace) -> list[Diagnostic]:
        return [
            Diagnostic(
                "missing-stylesheet",
                f"Unknown stylesheet '{note_type.manifest.stylesheet}' for {note_type.manifest.name}.",
            )
            for note_type in workspace.note_types
            if note_type.stylesheet is None
        ]

    def _validate_partials(self, workspace: Workspace) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        graph: dict[str, tuple[str, ...]] = {}
        for partial in workspace.partials:
            graph[str(partial.id)] = tuple(_PARTIAL.findall(partial.content))
        for owner, references in self._template_references(workspace).items():
            for reference in references:
                if reference not in graph:
                    diagnostics.append(Diagnostic("missing-partial", f"Unknown partial '{reference}' in {owner}."))
        diagnostics.extend(self._cycle_diagnostics(graph))
        return diagnostics

    @staticmethod
    def _template_references(workspace: Workspace) -> dict[str, tuple[str, ...]]:
        references: dict[str, tuple[str, ...]] = {}
        for note_type in workspace.note_types:
            for template in note_type.templates:
                references[f"{note_type.manifest.name}/{template.manifest.name}:front"] = tuple(
                    _PARTIAL.findall(template.front)
                )
                references[f"{note_type.manifest.name}/{template.manifest.name}:back"] = tuple(
                    _PARTIAL.findall(template.back)
                )
        return references

    def _cycle_diagnostics(self, graph: dict[str, tuple[str, ...]]) -> list[Diagnostic]:
        visited: set[str] = set()
        active: set[str] = set()
        diagnostics: list[Diagnostic] = []

        def visit(node: str) -> None:
            if node in active:
                diagnostics.append(Diagnostic("cyclic-partials", f"Circular partial reference involving '{node}'."))
                return
            if node in visited:
                return
            visited.add(node)
            active.add(node)
            for child in graph[node]:
                if child in graph:
                    visit(child)
            active.remove(node)

        for partial in graph:
            visit(partial)
        return diagnostics
