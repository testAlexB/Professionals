from pathlib import Path

import pytest

from agent.memory import LessonMemory
from agent.orchestrator import AgentOrchestrator
from agent.tools import WorkspaceTools
from agent.web_app import build_agent, create_chat_interface


class FakeLLM:
    def __init__(self, responses):
        self.responses = responses

    def chat(self, _messages):
        return self.responses.pop(0)


def test_orchestrator_commands(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM(["plain"])
    agent = AgentOrchestrator(llm, tools, memory)

    assert "Commands:" in agent.run_turn("/help")
    assert agent.run_turn("/lessons") == "No lessons yet."
    assert agent.run_turn("/lesson Keep API stable") == "Lesson saved."
    assert "Keep API stable" in agent.run_turn("/lessons")


def test_orchestrator_tool_flow(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        '{"tool":"write_file","args":{"path":"a.txt","content":"ok"}}',
        "Done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("save file")
    assert result == "Done"
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "ok"


def test_build_agent(tmp_path: Path):
    agent = build_agent(str(tmp_path), "qwen2.5-coder:7b", str(tmp_path / "lessons.json"))
    assert isinstance(agent, AgentOrchestrator)


def test_create_chat_interface_without_gradio(tmp_path: Path, monkeypatch):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    agent = AgentOrchestrator(FakeLLM(["ok"]), tools, memory)

    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "gradio":
            raise ModuleNotFoundError("No module named gradio")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    with pytest.raises(RuntimeError, match="Missing dependency: gradio"):
        create_chat_interface(agent)


def test_orchestrator_run_command_flow(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        '{"tool":"run_command","args":{"command":"python -c \\"print(42)\\""}}',
        "Done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("run python")
    assert result == "Done"


def test_orchestrator_autonomous_multi_step(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        '{"tool":"write_file","args":{"path":"a.txt","content":"A"}}',
        '{"tool":"append_file","args":{"path":"a.txt","content":"B"}}',
        "All done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("create and update file")
    assert result == "All done"
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "AB"


def test_orchestrator_retries_when_llm_gives_manual_steps(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        "Давайте выполним команды:\n```bash\ndotnet new wpf -n MyWpfApp\n```",
        '{"tool":"run_command","args":{"command":"python -c \\"print(1)\\""}}',
        "Done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("создай и собери проект")
    assert result == "Done"
