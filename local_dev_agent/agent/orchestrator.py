from __future__ import annotations

import json
from typing import Dict, List

from .llm_client import OllamaClient
from .memory import LessonMemory
from .tools import WorkspaceTools

SYSTEM_PROMPT = """You are a local coding assistant.
You can call tools by returning JSON only in this format:
{"tool":"read_file|write_file|append_file|list_files|run_command","args":{...}}
If no tool needed, return normal text.
Always follow user's lessons.
"""
MAX_TOOL_STEPS = 8


class AgentOrchestrator:
    def __init__(self, llm: OllamaClient, tools: WorkspaceTools, memory: LessonMemory) -> None:
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.history: List[Dict[str, str]] = []

    def clear_history(self) -> None:
        self.history = []

    def _render_lessons(self) -> str:
        lessons = self.memory.all_lessons()
        if not lessons:
            return "No lessons yet."
        return "\n".join(f"- {x}" for x in lessons)

    def run_turn(self, user_text: str) -> str:
        cmd = self._handle_local_command(user_text)
        if cmd is not None:
            return cmd

        msgs: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT + "\nLessons:\n" + self._render_lessons()},
            *self.history,
            {"role": "user", "content": user_text},
        ]

        self.history.append({"role": "user", "content": user_text})

        current_msgs = msgs
        for _ in range(MAX_TOOL_STEPS):
            model_text = self.llm.chat(current_msgs)
            tool_payload = self._maybe_parse_json(model_text)
            self.history.append({"role": "assistant", "content": model_text})
            if not tool_payload:
                return model_text

            tool_result = self._execute_tool(tool_payload)
            self.history.append({"role": "tool", "content": tool_result})
            current_msgs = [
                {"role": "system", "content": SYSTEM_PROMPT + "\nLessons:\n" + self._render_lessons()},
                *self.history,
                {
                    "role": "user",
                    "content": "Continue. If more actions are needed, return next JSON tool call. "
                    "If done, return final text summary.",
                },
            ]

        timeout_text = "Stopped after max autonomous steps. Please continue with a follow-up request."
        self.history.append({"role": "assistant", "content": timeout_text})
        return timeout_text


    def _handle_local_command(self, user_text: str):
        t = user_text.strip()
        if t == "/help":
            return "Commands: /help, /clear, /lessons, /lesson <text>, /exit"
        if t == "/clear":
            self.clear_history()
            return "Chat history cleared."
        if t == "/lessons":
            lessons = self.memory.all_lessons()
            return "No lessons yet." if not lessons else "\n".join(f"{i}. {x}" for i, x in enumerate(lessons, 1))
        if t.startswith("/lesson "):
            self.memory.add_lesson(t[len("/lesson ") :].strip())
            return "Lesson saved."
        return None
    def _maybe_parse_json(self, text: str):
        text = text.strip()
        if not text.startswith("{"):
            return None
        try:
            payload = json.loads(text)
            if "tool" in payload and "args" in payload:
                return payload
        except json.JSONDecodeError:
            return None
        return None

    def _execute_tool(self, payload: dict) -> str:
        tool = payload["tool"]
        args = payload.get("args", {})

        if tool == "read_file":
            result = self.tools.read_file(args["path"])
        elif tool == "write_file":
            result = self.tools.write_file(args["path"], args["content"])
        elif tool == "append_file":
            result = self.tools.append_file(args["path"], args["content"])
        elif tool == "list_files":
            result = self.tools.list_files(args.get("path", "."))
        elif tool == "run_command":
            result = self.tools.run_command(args["command"], args.get("timeout_sec", 300))
        else:
            return f"Unknown tool: {tool}"

        status = "OK" if result.ok else "ERROR"
        return f"{status}: {result.message}"
