from pathlib import Path

from anki_note_types.synchronizer import InstallationState, InstallationStateStore, ProfileManager


def test_installation_state_round_trip(tmp_path: Path):
    path = tmp_path / "state.json"
    store = InstallationStateStore()

    store.save(path, InstallationState("0.1.0", {"Vocabulary": "digest"}))
    loaded = store.load(path, "0.1.0")

    assert loaded.installed == {"Vocabulary": "digest"}


def test_profile_manager_discovers_directories(tmp_path: Path):
    (tmp_path / "Profile A").mkdir()
    (tmp_path / "not-a-profile.txt").write_text("", encoding="utf-8")

    profiles = ProfileManager().discover(tmp_path)

    assert [profile.name for profile in profiles] == ["Profile A"]
