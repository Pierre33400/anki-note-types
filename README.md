# Anki Note Types

Development toolkit for Anki note types. The note-type sources live in
`project/`; the Python implementation lives in `src/anki_note_types/`; compiled
artefacts are written to `build/`.

## Goals

- Git versioning
- HTML templates
- Shared CSS
- Validation
- Compilation
- Synchronization
- Multiple Anki profiles

Status: Early development.

## Local commands

After installing the development dependencies, run:

```text
anki-note-types validate
anki-note-types build --output build
anki-note-types sync --dry-run
pytest
ruff check src tests
black --check src tests
```
