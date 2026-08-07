"""Pure compilation of validated note-type sources."""

from __future__ import annotations

import re

from anki_note_types.model import Catalog, CompiledNoteType, CompiledTemplate, CompiledWorkspace, Workspace
from anki_note_types.model.ids import NoteTypeId, PartialId, TemplateId
from anki_note_types.services import HashService

_PARTIAL = re.compile(r"{{>\s*([A-Za-z0-9_.-]+)\s*}}")


class WorkspaceCompiler:
    """Resolve partials and generate deterministic, in-memory artefacts."""

    def compile(self, workspace: Workspace) -> CompiledWorkspace:
        note_types: dict[NoteTypeId, CompiledNoteType] = {}
        for note_type in workspace.note_types:
            if note_type.stylesheet is None:
                raise ValueError(f"Missing stylesheet for {note_type.manifest.name}")
            templates: dict[TemplateId, CompiledTemplate] = {}
            for template in note_type.templates:
                templates[template.manifest.id] = CompiledTemplate(
                    name=template.manifest.name,
                    front=self._resolve(template.front, workspace),
                    back=self._resolve(template.back, workspace),
                )
            stylesheet = self._normalize(note_type.stylesheet.content)
            content = self._hash_content(note_type.manifest.name, stylesheet, templates)
            note_types[note_type.manifest.id] = CompiledNoteType(
                name=note_type.manifest.name,
                fields=note_type.manifest.fields,
                stylesheet=stylesheet,
                templates=Catalog(templates),
                compiled_hash=HashService.text(content),
            )
        return CompiledWorkspace(Catalog(note_types))

    def _resolve(self, content: str, workspace: Workspace, stack: tuple[str, ...] = ()) -> str:
        def replace(match: re.Match[str]) -> str:
            identifier = match.group(1)
            if identifier in stack:
                raise ValueError(f"Circular partial reference: {' -> '.join((*stack, identifier))}")
            partial = workspace.partials.require(PartialId(identifier))
            return self._resolve(partial.content, workspace, (*stack, identifier))

        return self._normalize(_PARTIAL.sub(replace, content))

    @staticmethod
    def _normalize(content: str) -> str:
        return content.replace("\r\n", "\n").replace("\r", "\n")

    @staticmethod
    def _hash_content(
        name: str,
        stylesheet: str,
        templates: dict[TemplateId, CompiledTemplate],
    ) -> str:
        parts = [name, stylesheet]
        for identifier, template in sorted(templates.items(), key=lambda item: str(item[0])):
            parts.extend((str(identifier), template.front, template.back))
        return "\n\0\n".join(parts)
