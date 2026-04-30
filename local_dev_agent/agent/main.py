from __future__ import annotations

import argparse
from pathlib import Path

from .llm_client import OllamaClient
from .memory import LessonMemory
from .orchestrator import AgentOrchestrator
from .tools import WorkspaceTools


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local coding AI agent")
    parser.add_argument("--workspace", required=True, help="Folder where agent can read/write files")
    parser.add_argument("--model", default="qwen2.5-coder:14b", help="Ollama model name")
    parser.add_argument("--memory-file", default=".agent_lessons.json", help="Lessons file path")
    return parser.parse_args()


def run() -> None:
    try:
        from rich.console import Console
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: rich. Install with `pip install -r requirements.txt`."
        ) from exc

    args = parse_args()
    console = Console()

    workspace = Path(args.workspace).resolve()
    tools = WorkspaceTools(workspace)
    memory = LessonMemory(Path(args.memory_file).resolve())
    llm = OllamaClient(args.model)
    agent = AgentOrchestrator(llm, tools, memory)

    console.print("[bold green]Local Dev Agent started[/bold green]")
    console.print(f"Workspace: {workspace}")
    console.print("Type /help for commands.")

    while True:
        user = console.input("\n[bold cyan]You:[/bold cyan] ").strip()

        if not user:
            continue
        if user == "/exit":
            console.print("Bye!")
            break

        try:
            answer = agent.run_turn(user)
            console.print(f"[bold magenta]Agent:[/bold magenta] {answer}")
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Error:[/red] {exc}")


if __name__ == "__main__":
    run()
