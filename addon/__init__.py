"""Entry-point skeleton for the packaged Anki add-on.

The release process bundles ``src/anki_note_types`` alongside this file.  The
function is deliberately explicit so importing an add-on never builds or
synchronizes a collection unexpectedly.
"""

from pathlib import Path


def setup(project_path: Path, build_path: Path) -> None:
    """Register the add-on's menu actions in the currently running Anki UI."""
    from anki_note_types.addon import install_menu

    install_menu(project_path, build_path)
