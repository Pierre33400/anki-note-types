from pathlib import Path

from anki_note_types.services import HashService


def test_same_text_same_hash():
    a = HashService.text("hello")
    b = HashService.text("hello")

    assert a == b


def test_hash_uses_sha256():
    assert HashService.text("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_different_text_different_hash():
    a = HashService.text("hello")
    b = HashService.text("world")

    assert a != b


def test_file_hash(tmp_path: Path):
    file = tmp_path / "test.txt"
    file.write_text("abc", encoding="utf-8")

    expected = HashService.text("abc")

    assert HashService.file(file) == expected
