from pathlib import Path

from anki_note_types import Application
from anki_note_types.compiler.asset_collector import AssetCollector
from anki_note_types.loader import ProjectLoader


def test_asset_collector_returns_an_empty_collection_when_no_assets_exist():
    project_path = Path(__file__).parents[3] / "project"
    source = ProjectLoader().load(project_path)
    compiled = Application().compile(project_path)

    assert AssetCollector().collect(source, compiled) == ()
