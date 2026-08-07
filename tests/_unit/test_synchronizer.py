from pathlib import Path

from anki_note_types import Application
from anki_note_types.model import CompiledNoteType
from anki_note_types.synchronizer import Synchronizer

PROJECT_PATH = Path(__file__).parents[2] / "project"


class FakeAnkiGateway:
    profile_name = "test-profile"

    def __init__(self) -> None:
        self.hashes: dict[str, str] = {}
        self.installed: list[CompiledNoteType] = []

    def installed_hash(self, note_type_name: str) -> str | None:
        return self.hashes.get(note_type_name)

    def install(self, note_type: CompiledNoteType) -> None:
        self.installed.append(note_type)

    def record_installation(self, note_type_name: str, compiled_hash: str) -> None:
        self.hashes[note_type_name] = compiled_hash


def test_synchronizer_is_idempotent():
    workspace = Application().compile(PROJECT_PATH)
    gateway = FakeAnkiGateway()

    first = Synchronizer().sync(workspace, gateway)
    second = Synchronizer().sync(workspace, gateway)

    assert first.updated_profiles == ("test-profile",)
    assert second.skipped_profiles == ("test-profile",)
    assert len(gateway.installed) == len(workspace.note_types)


def test_dry_run_does_not_install():
    workspace = Application().compile(PROJECT_PATH)
    gateway = FakeAnkiGateway()

    report = Synchronizer().sync(workspace, gateway, dry_run=True)

    assert report.skipped_profiles == ("test-profile",)
    assert not gateway.installed
