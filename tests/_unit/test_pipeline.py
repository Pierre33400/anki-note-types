from pathlib import Path

from anki_note_types import Application
from anki_note_types.loader import ProjectLoader
from anki_note_types.model import Catalog, Workspace
from anki_note_types.validator import WorkspaceValidator


PROJECT_PATH = Path(__file__).parents[2] / "project"


def test_project_loader_loads_the_example_project():
    workspace = ProjectLoader().load(PROJECT_PATH)

    assert len(workspace.note_types) == 2
    assert len(workspace.partials) == 3


def test_validator_reports_missing_partial():
    workspace = ProjectLoader().load(PROJECT_PATH)
    invalid = Workspace(workspace.note_types, Catalog({}), workspace.stylesheets, workspace.assets)

    report = WorkspaceValidator().validate(invalid)

    assert not report.success
    assert {item.code for item in report.diagnostics} == {"missing-partial"}


def test_application_build_resolves_partials(tmp_path: Path):
    report = Application().build(PROJECT_PATH, tmp_path / "build")
    front = (tmp_path / "build" / "Vocabulaire" / "templates" / "Recognition" / "front.html").read_text(
        encoding="utf-8"
    )

    assert report.success
    assert "{{>" not in front
    assert "<main class=\"card\">" in front


def test_compilation_is_deterministic():
    application = Application()

    first = application.compile(PROJECT_PATH)
    second = application.compile(PROJECT_PATH)

    first_hashes = [note_type.compiled_hash for note_type in first.note_types]
    second_hashes = [note_type.compiled_hash for note_type in second.note_types]
    assert first_hashes == second_hashes
