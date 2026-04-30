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
    agent = build_agent(
        str(tmp_path),
        "qwen2.5-coder:7b",
        str(tmp_path / "lessons.json"),
        str(tmp_path / "trace.jsonl"),
    )
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


def test_orchestrator_forces_tools_for_action_requests(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        "Ок, сделаю проект.",
        '{"tool":"run_command","args":{"command":"python -c \\"print(7)\\""}}',
        "Done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("create project and run build")
    assert result == "Done"


def test_request_requires_actions_detects_russian_and_english(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    agent = AgentOrchestrator(FakeLLM(["ok"]), tools, memory)
    assert agent._request_requires_actions("создай проект и собери его")
    assert agent._request_requires_actions("please create project and run build")
    assert not agent._request_requires_actions("объясни архитектуру проекта")


def test_manual_instruction_detector_patterns(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    agent = AgentOrchestrator(FakeLLM(["ok"]), tools, memory)
    assert agent._looks_like_manual_instructions("```bash\ndotnet new wpf -n App\n```")
    assert agent._looks_like_manual_instructions("Перейдите в папку и выполните dotnet build")
    assert not agent._looks_like_manual_instructions("Проект успешно создан и собран.")


def test_action_request_without_tool_calls_returns_explicit_tool_mode_error(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM(["Ок, начну.", "Сейчас сделаю.", "Подождите..."])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("сделай проект и запусти сборку")
    assert "could not switch to tool execution mode" in result
    assert "Подождите..." in result


def test_orchestrator_writes_trace_log(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    trace_file = tmp_path / "trace.jsonl"
    llm = FakeLLM(['{"tool":"write_file","args":{"path":"a.txt","content":"ok"}}', "Done"])
    agent = AgentOrchestrator(llm, tools, memory, trace_file=trace_file)
    result = agent.run_turn("save file")
    assert result == "Done"
    raw = trace_file.read_text(encoding="utf-8")
    assert '"event": "model_response"' in raw
    assert '"event": "tool_result"' in raw


def test_parse_fenced_json_tool_call(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        '```json\n{"tool":"write_file","args":{"path":"a.txt","content":"ok"}}\n```',
        "Done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("save file")
    assert result == "Done"
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "ok"


def test_parse_tool_call_embedded_in_explanatory_text(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")
    llm = FakeLLM([
        (
            "Sure, I'll do it.\n"
            "```json\n"
            '{"tool":"run_command","args":{"command":"python -c \\"print(11)\\""}}\n'
            "```\n"
            "Then I will continue."
        ),
        "Done",
    ])
    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn("run command")
    assert result == "Done"
