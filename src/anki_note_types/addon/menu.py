"""Minimal Anki menu actions for building and synchronizing note types."""

from __future__ import annotations

from pathlib import Path

from anki_note_types import Application
from anki_note_types.synchronizer import AnkiAdapter, Synchronizer


def install_menu(project_path: Path, build_path: Path) -> None:
    """Install build and sync actions in Anki's Tools menu."""
    from aqt import mw  # type: ignore[import-not-found]
    from aqt.qt import QAction  # type: ignore[import-not-found]
    from aqt.utils import tooltip  # type: ignore[import-not-found]

    def build() -> None:
        Application().build(project_path, build_path)
        tooltip("Anki note types built successfully.")

    def synchronize() -> None:
        compiled = Application().compile(project_path)
        report = Synchronizer().sync(compiled, AnkiAdapter(mw))
        tooltip("Anki note types synchronized." if report.updated_profiles else "Anki note types already up to date.")

    build_action = QAction("Build note types", mw)
    build_action.triggered.connect(build)
    mw.form.menuTools.addAction(build_action)
    sync_action = QAction("Synchronize note types", mw)
    sync_action.triggered.connect(synchronize)
    mw.form.menuTools.addAction(sync_action)
