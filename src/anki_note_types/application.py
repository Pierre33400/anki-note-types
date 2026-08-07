"""Application entry point for the source-to-build pipeline."""

from __future__ import annotations

from pathlib import Path

from .build import BuildWriter
from .compiler import WorkspaceCompiler
from .loader import ProjectLoader
from .model import CompiledWorkspace
from .model.reports import BuildReport, ValidationReport
from .validator import ProjectValidator, WorkspaceValidator


class Application:
    """Coordinate loading, validation, pure compilation and build output."""

    def __init__(
        self,
        loader: ProjectLoader | None = None,
        validator: WorkspaceValidator | None = None,
        project_validator: ProjectValidator | None = None,
        compiler: WorkspaceCompiler | None = None,
        writer: BuildWriter | None = None,
    ) -> None:
        self._loader = loader or ProjectLoader()
        self._validator = validator or WorkspaceValidator()
        self._project_validator = project_validator or ProjectValidator()
        self._compiler = compiler or WorkspaceCompiler()
        self._writer = writer or BuildWriter()

    def compile(self, project_path: Path) -> CompiledWorkspace:
        """Return compiled artefacts, or raise when source validation fails."""
        report = self.validate(project_path)
        if not report.success:
            messages = "; ".join(item.message for item in report.diagnostics)
            raise ValueError(f"Source validation failed: {messages}")
        return self._compiler.compile(self._loader.load(project_path))

    def validate(self, project_path: Path) -> ValidationReport:
        """Return all diagnostics that can be found without compiling."""
        source_report = self._project_validator.validate(project_path)
        if not source_report.success:
            return source_report
        workspace_report = self._validator.validate(self._loader.load(project_path))
        return ValidationReport((*source_report.diagnostics, *workspace_report.diagnostics))

    def build(self, project_path: Path, output_path: Path) -> BuildReport:
        """Compile and persist artefacts in *output_path*."""
        report = self.validate(project_path)
        if not report.success:
            messages = "; ".join(item.message for item in report.diagnostics)
            raise ValueError(f"Source validation failed: {messages}")
        workspace = self._loader.load(project_path)
        compiled = self._compiler.compile(workspace)
        self._writer.write(compiled, output_path, assets=workspace.assets, asset_source=project_path / "assets")
        return BuildReport(output_path=str(output_path))
