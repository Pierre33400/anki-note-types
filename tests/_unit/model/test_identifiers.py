import pytest

from anki_note_types.model.ids import NoteTypeId


def test_identifier_rejects_whitespace_only_values():
    with pytest.raises(ValueError):
        NoteTypeId("   ")
