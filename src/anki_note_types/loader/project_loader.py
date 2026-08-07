"""Load the declarative note-type sources from a project directory."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath

from anki_note_types.model import Asset, Catalog, NoteType, Partial, Stylesheet, Template, Workspace
from anki_note_types.model.ids import AssetId, NoteTypeId, PartialId, StylesheetId, TemplateId
from anki_note_types.model.manifests import NoteTypeManifest, TemplateManifest
from anki_note_types.validator.manifest_validator import ManifestValidator


class ProjectLoader:
    """Build the source model without applying validation or transformations."""

    def load(self, project_path: Path) -> Workspace:
        stylesheets = self._load_stylesheets(project_path / "css")
        partials = self._load_partials(project_path / "partials")
        assets = self._load_assets(project_path / "assets")
        note_types = self._load_note_types(project_path / "note-types", stylesheets, assets)
        return Workspace(note_types, partials, stylesheets, assets)

    def _load_stylesheets(self, directory: Path) -> Catalog[StylesheetId, Stylesheet]:
        items: dict[StylesheetId, Stylesheet] = {}
        if directory.exists():
            for path in sorted(directory.rglob("*.css")):
                identifier = StylesheetId(path.relative_to(directory).as_posix())
                items[identifier] = Stylesheet(identifier, path.read_text(encoding="utf-8"))
        return Catalog(items)

    def _load_partials(self, directory: Path) -> Catalog[PartialId, Partial]:
        items: dict[PartialId, Partial] = {}
        if directory.exists():
            for path in sorted(directory.rglob("*.html")):
                identifier = PartialId(path.stem)
                if identifier in items:
                    raise ValueError(f"Duplicate partial identifier: {identifier}")
                items[identifier] = Partial(identifier, path.read_text(encoding="utf-8"))
        return Catalog(items)

    def _load_assets(self, directory: Path) -> Catalog[AssetId, Asset]:
        items: dict[AssetId, Asset] = {}
        if directory.exists():
            for path in sorted(item for item in directory.rglob("*") if item.is_file()):
                logical_path = path.relative_to(directory).as_posix()
                identifier = AssetId(logical_path)
                items[identifier] = Asset(identifier, PurePosixPath(logical_path))
        return Catalog(items)

    def _load_note_types(
        self,
        directory: Path,
        stylesheets: Catalog[StylesheetId, Stylesheet],
        assets: Catalog[AssetId, Asset],
    ) -> Catalog[NoteTypeId, NoteType]:
        items: dict[NoteTypeId, NoteType] = {}
        manifest_validator = ManifestValidator()
        if not directory.exists():
            return Catalog(items)
        for path in sorted(item for item in directory.iterdir() if item.is_dir()):
            metadata = self._read_json(path / "metadata.json")
            self._require_valid_manifest(manifest_validator.validate_note_type(metadata), path / "metadata.json")
            note_type_id = NoteTypeId(path.name)
            stylesheet_id = StylesheetId(str(metadata["stylesheet"]))
            note_type_manifest = NoteTypeManifest(
                id=note_type_id,
                name=str(metadata["name"]),
                stylesheet=stylesheet_id,
                fields=tuple(str(field) for field in metadata["fields"]),
                schema_version=int(metadata["schemaVersion"]),
            )
            templates = self._load_templates(path / "templates", manifest_validator)
            items[note_type_id] = NoteType(
                note_type_manifest,
                templates,
                stylesheets.get(stylesheet_id),
                assets,
            )
        return Catalog(items)

    def _load_templates(self, directory: Path, manifest_validator: ManifestValidator) -> Catalog[TemplateId, Template]:
        items: dict[TemplateId, Template] = {}
        for path in sorted(item for item in directory.iterdir() if item.is_dir()):
            metadata = self._read_json(path / "template.json")
            self._require_valid_manifest(manifest_validator.validate_template(metadata), path / "template.json")
            identifier = TemplateId(str(metadata["name"]))
            if identifier in items:
                raise ValueError(f"Duplicate template identifier: {identifier}")
            manifest = TemplateManifest(
                id=identifier,
                name=str(metadata["name"]),
                schema_version=int(metadata["schemaVersion"]),
            )
            items[identifier] = Template(
                manifest,
                (path / "front.html").read_text(encoding="utf-8"),
                (path / "back.html").read_text(encoding="utf-8"),
            )
        return Catalog(items)

    @staticmethod
    def _read_json(path: Path) -> dict[str, object]:
        with path.open(encoding="utf-8") as source:
            value = json.load(source)
        if not isinstance(value, dict):
            raise ValueError(f"Expected a JSON object in {path}")
        return value

    @staticmethod
    def _require_valid_manifest(diagnostics: tuple[object, ...], path: Path) -> None:
        if diagnostics:
            messages = "; ".join(getattr(item, "message") for item in diagnostics)
            raise ValueError(f"Invalid manifest {path}: {messages}")
