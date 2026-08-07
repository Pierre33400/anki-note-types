import shutil
from pathlib import Path

from anki_note_types import Application


PROJECT_PATH = Path(__file__).parents[2] / "project"
GOLDEN_PATH = Path(__file__).parents[1] / "fixtures" / "golden" / "vocabulaire-recognition-front.html"


def test_build_matches_the_golden_template(tmp_path: Path):
    output = tmp_path / "build"

    Application().build(PROJECT_PATH, output)

    actual = (output / "Vocabulaire" / "templates" / "Recognition" / "front.html").read_text(encoding="utf-8")
    assert actual == GOLDEN_PATH.read_text(encoding="utf-8")


def test_build_replaces_stale_output_atomically(tmp_path: Path):
    output = tmp_path / "build"
    output.mkdir()
    stale = output / "stale.txt"
    stale.write_text("obsolete", encoding="utf-8")

    Application().build(PROJECT_PATH, output)

    assert not stale.exists()
    assert (output / "Vocabulaire" / "metadata.json").is_file()


def test_build_copies_assets(tmp_path: Path):
    project = tmp_path / "project"
    shutil.copytree(PROJECT_PATH, project)
    source_asset = project / "assets" / "icons" / "logo.txt"
    source_asset.parent.mkdir(parents=True)
    source_asset.write_text("asset", encoding="utf-8")

    Application().build(project, tmp_path / "build")

    assert (tmp_path / "build" / "assets" / "icons" / "logo.txt").read_text(encoding="utf-8") == "asset"
