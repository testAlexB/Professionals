from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shlex
import subprocess


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



    def run_command(self, command: str, timeout_sec: int = 120) -> ToolResult:
        command = command.strip()
        if not command:
            return ToolResult(False, "Command is empty")

        try:
            parts = shlex.split(command)
        except ValueError as exc:
            return ToolResult(False, f"Invalid command: {exc}")

        if not parts:
            return ToolResult(False, "Command is empty")

        allowed = {"dotnet", "python", "python3", "py", "pytest"}
        if parts[0] not in allowed:
            return ToolResult(False, f"Command not allowed: {parts[0]}")

        try:
            completed = subprocess.run(
                parts,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False,
            )
        except FileNotFoundError:
            return ToolResult(False, f"Command not found: {parts[0]}")
        except subprocess.TimeoutExpired:
            return ToolResult(False, f"Command timed out after {timeout_sec}s")

        output = (completed.stdout or "")
        err = (completed.stderr or "")
        merged = (output + ("\n" if output and err else "") + err).strip()
        merged = merged or "<no output>"

        if completed.returncode != 0:
            return ToolResult(False, f"Exit code {completed.returncode}\n{merged}")
        return ToolResult(True, merged)

    def list_files(self, relative_dir: str = ".") -> ToolResult:
        directory = self._resolve_safe(relative_dir)
        if not directory.exists() or not directory.is_dir():
            return ToolResult(False, f"Directory not found: {relative_dir}")
        files = []
        for p in sorted(directory.rglob("*")):
            if p.is_file():
                files.append(str(p.relative_to(self.workspace)))
        return ToolResult(True, "\n".join(files) if files else "<empty>")
