from __future__ import annotations

import argparse
from pathlib import Path

from .llm_client import OllamaClient
from .memory import LessonMemory
from .orchestrator import AgentOrchestrator
from .tools import WorkspaceTools


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local coding AI agent web UI")
    parser.add_argument("--workspace", required=True, help="Folder where agent can read/write files")
    parser.add_argument("--model", default="qwen2.5-coder:14b", help="Ollama model name")
    parser.add_argument("--memory-file", default=".agent_lessons.json", help="Lessons file path")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--share", action="store_true", help="Create public temporary gradio link")
    parser.add_argument("--trace-file", default=".agent_trace.jsonl", help="Path to JSONL trace log")
    return parser.parse_args()


def build_agent(workspace: str, model: str, memory_file: str, trace_file: str) -> AgentOrchestrator:
    tools = WorkspaceTools(Path(workspace).resolve())
    memory = LessonMemory(Path(memory_file).resolve())
    llm = OllamaClient(model)
    return AgentOrchestrator(llm, tools, memory, trace_file=Path(trace_file).resolve())


def create_chat_interface(agent: AgentOrchestrator):
    try:
        import gradio as gr
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: gradio. Install with `pip install -r requirements-web.txt` (Python 3.12 recommended)."
        ) from exc

    def chat_fn(message: str, history: list[list[str]]):
        _ = history
        try:
            return agent.run_turn(message)
        except Exception as err:  # noqa: BLE001
            return f"Error: {err}"

    return gr.ChatInterface(
        fn=chat_fn,
        title="Local Dev Agent",
        description=(
            "Локальный агент для кода через Ollama. "
            "Команды в чате: /lesson ..., /lessons, /clear, /help"
        ),
    )


def main() -> None:
    args = parse_args()
    agent = build_agent(args.workspace, args.model, args.memory_file, args.trace_file)
    demo = create_chat_interface(agent)
    demo.launch(server_name=args.host, server_port=args.port, share=args.share)


if __name__ == "__main__":
    main()
