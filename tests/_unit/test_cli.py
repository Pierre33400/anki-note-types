from pathlib import Path

from anki_note_types import cli


def test_cli_validate_returns_success(monkeypatch):
    project = Path(__file__).parents[2] / "project"
    monkeypatch.setattr("sys.argv", ["anki-note-types", "--project", str(project), "validate"])

    assert cli.main() == 0
