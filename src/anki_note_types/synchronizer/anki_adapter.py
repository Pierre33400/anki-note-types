"""Concrete gateway for Anki's public model-manager API.

The imports are intentionally deferred so the engine remains usable outside
Anki.  The adapter never opens or modifies Anki's SQLite database directly.
"""

from __future__ import annotations

from typing import Any

from anki_note_types.model import CompiledNoteType


class AnkiAdapter:
    """Install compiled note types in the collection attached to ``mw``."""

    _STATE_KEY = "anki_note_types.installation_hashes"

    def __init__(self, mw: Any) -> None:
        self._mw = mw

    @property
    def profile_name(self) -> str:
        return str(self._mw.pm.name)

    def installed_hash(self, note_type_name: str) -> str | None:
        state = self._collection_config()
        value = state.get(note_type_name)
        return value if isinstance(value, str) else None

    def install(self, note_type: CompiledNoteType) -> None:
        models = self._mw.col.models
        model = models.by_name(note_type.name)
        if model is None:
            model = models.new(note_type.name)
            for field_name in note_type.fields:
                models.add_field(model, models.new_field(field_name))
            for template in note_type.templates:
                anki_template = models.new_template(template.name)
                anki_template["qfmt"] = template.front
                anki_template["afmt"] = template.back
                models.add_template(model, anki_template)
            model["css"] = note_type.stylesheet
            models.add(model)
            return

        existing_fields = tuple(field["name"] for field in model["flds"])
        if existing_fields != note_type.fields:
            raise ValueError(
                f"Fields for {note_type.name!r} differ from the existing Anki note type; "
                "automatic field migration is intentionally not supported."
            )
        model["css"] = note_type.stylesheet
        model["tmpls"] = []
        for template in note_type.templates:
            anki_template = models.new_template(template.name)
            anki_template["qfmt"] = template.front
            anki_template["afmt"] = template.back
            model["tmpls"].append(anki_template)
        models.update_dict(model)

    def record_installation(self, note_type_name: str, compiled_hash: str) -> None:
        state = self._collection_config()
        state[note_type_name] = compiled_hash
        self._mw.col.set_config(self._STATE_KEY, state)

    def _collection_config(self) -> dict[str, str]:
        value = self._mw.col.get_config(self._STATE_KEY, default={})
        return dict(value) if isinstance(value, dict) else {}
