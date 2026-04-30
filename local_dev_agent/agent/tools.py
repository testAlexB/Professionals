from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolResult:
    ok: bool
    message: str


class WorkspaceTools:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def _resolve_safe(self, relative_path: str) -> Path:
        candidate = (self.workspace / relative_path).resolve()
        if not str(candidate).startswith(str(self.workspace)):
            raise ValueError("Path is outside workspace")
        return candidate

    def read_file(self, relative_path: str) -> ToolResult:
        path = self._resolve_safe(relative_path)
        if not path.exists():
            return ToolResult(False, f"File not found: {relative_path}")
        return ToolResult(True, path.read_text(encoding="utf-8"))

    def write_file(self, relative_path: str, content: str) -> ToolResult:
        path = self._resolve_safe(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolResult(True, f"Saved: {relative_path}")

    def append_file(self, relative_path: str, content: str) -> ToolResult:
        path = self._resolve_safe(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(content)
        return ToolResult(True, f"Appended: {relative_path}")

    def list_files(self, relative_dir: str = ".") -> ToolResult:
        directory = self._resolve_safe(relative_dir)
        if not directory.exists() or not directory.is_dir():
            return ToolResult(False, f"Directory not found: {relative_dir}")
        files = []
        for p in sorted(directory.rglob("*")):
            if p.is_file():
                files.append(str(p.relative_to(self.workspace)))
        return ToolResult(True, "\n".join(files) if files else "<empty>")
