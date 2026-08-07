import json
import shutil
from pathlib import Path

from anki_note_types.validator import ProjectValidator


def test_project_validator_reports_invalid_json(tmp_path: Path):
    project = tmp_path / "project"
    shutil.copytree(Path(__file__).parents[3] / "project", project)
    metadata = project / "note-types" / "Vocabulaire" / "metadata.json"
    metadata.write_text("{", encoding="utf-8")

    report = ProjectValidator().validate(project)

    assert {item.code for item in report.diagnostics} == {"invalid-json"}


def test_project_validator_reports_missing_stylesheet(tmp_path: Path):
    project = tmp_path / "project"
    shutil.copytree(Path(__file__).parents[3] / "project", project)
    metadata = project / "note-types" / "Vocabulaire" / "metadata.json"
    value = json.loads(metadata.read_text(encoding="utf-8"))
    value["stylesheet"] = "missing.css"
    metadata.write_text(json.dumps(value), encoding="utf-8")

    report = ProjectValidator().validate(project)

    assert {item.code for item in report.diagnostics} == {"missing-stylesheet"}
