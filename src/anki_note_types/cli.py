"""Command-line interface for validation and deterministic builds."""

from __future__ import annotations

import argparse
from pathlib import Path

from .application import Application


def main() -> int:
    parser = argparse.ArgumentParser(prog="anki-note-types")
    parser.add_argument("--project", type=Path, default=Path("project"))
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("validate")
    build = subcommands.add_parser("build")
    build.add_argument("--output", type=Path, default=Path("build"))
    sync = subcommands.add_parser("sync")
    sync.add_argument("--dry-run", action="store_true", required=True)

    arguments = parser.parse_args()
    application = Application()
    if arguments.command == "validate":
        report = application.validate(arguments.project)
        for diagnostic in report.diagnostics:
            print(f"{diagnostic.level}: {diagnostic.code}: {diagnostic.message}")
        return 0 if report.success else 1
    if arguments.command == "build":
        report = application.build(arguments.project, arguments.output)
        print(f"Built artefacts in {report.output_path}")
        return 0 if report.success else 1

    compiled = application.compile(arguments.project)
    print(f"Dry run: {len(compiled.note_types)} note type(s) would be synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
