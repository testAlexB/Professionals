from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
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
MAX_TOOLLESS_RETRIES = 2


class AgentOrchestrator:
    def __init__(
        self, llm: OllamaClient, tools: WorkspaceTools, memory: LessonMemory, trace_file: Path | None = None
    ) -> None:
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.history: List[Dict[str, str]] = []
        self.trace_file = trace_file
        if self.trace_file is not None:
            self.trace_file.parent.mkdir(parents=True, exist_ok=True)

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

        must_execute = self._request_requires_actions(user_text)
        current_msgs = msgs
        executed_tools = 0
        toolless_retries = 0
        for _ in range(MAX_TOOL_STEPS):
            model_text = self.llm.chat(current_msgs)
            self._trace("model_response", model_text)
            tool_payload = self._maybe_parse_json(model_text)
            self.history.append({"role": "assistant", "content": model_text})
            if (
                not tool_payload
                and executed_tools == 0
                and (must_execute or self._looks_like_manual_instructions(model_text))
            ):
                toolless_retries += 1
                if toolless_retries > MAX_TOOLLESS_RETRIES:
                    fail_text = (
                        "Agent could not switch to tool execution mode. "
                        "Model kept returning non-tool text instead of JSON tool calls.\n"
                        f"Last model response:\n{model_text}"
                    )
                    self.history.append({"role": "assistant", "content": fail_text})
                    self._trace("agent_error", fail_text)
                    return fail_text
                current_msgs = [
                    {"role": "system", "content": SYSTEM_PROMPT + "\nLessons:\n" + self._render_lessons()},
                    *self.history,
                    {
                        "role": "user",
                        "content": (
                            "Do not provide manual instructions. Execute actions yourself using JSON tool calls only. "
                            "Use run_command/read_file/write_file/... as needed and continue until task is done."
                        ),
                    },
                ]
                continue
            if not tool_payload:
                return model_text

            tool_result = self._execute_tool(tool_payload)
            self._trace("tool_result", tool_result)
            executed_tools += 1
            toolless_retries = 0
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
        self._trace("agent_error", timeout_text)
        return timeout_text

    def _trace(self, event: str, content: str) -> None:
        if self.trace_file is None:
            return
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "content": content,
        }
        with self.trace_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _request_requires_actions(self, user_text: str) -> bool:
        lowered = user_text.lower()
        patterns = [
            r"\bсозд(ай|ать|айте)\b",
            r"\bсобер(и|ите|ать)\b",
            r"\bзапуст(и|ите|ить)\b",
            r"\bвыполн(и|ите|ить)\b",
            r"\bсделай\b",
            r"\bbuild\b",
            r"\brun\b",
            r"\bexecute\b",
            r"\bcreate\b",
            r"\bcompile\b",
            r"\bdotnet\b",
            r"\bpytest\b",
            r"\bpython\b",
        ]
        return any(re.search(p, lowered) for p in patterns)

    def _looks_like_manual_instructions(self, text: str) -> bool:
        lowered = text.lower()
        if "```" in lowered:
            return True
        patterns = [
            r"\bdotnet\s+new\b",
            r"\bdotnet\s+build\b",
            r"\bперейд(ем|ите)\b",
            r"\bзапуст(им|ите)\b",
            r"\bвыполн(ите|им)\b",
            r"\bcd\s+",
        ]
        return any(re.search(p, lowered) for p in patterns)


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
        candidates = [text]
        fenced = re.findall(r"```(?:json)?\s*([\s\S]*?)```", text, flags=re.IGNORECASE)
        candidates.extend(x.strip() for x in fenced if x.strip())

        for candidate in candidates:
            try:
                payload = json.loads(candidate)
                if "tool" in payload and "args" in payload:
                    return payload
            except json.JSONDecodeError:
                pass

        for candidate in candidates:
            for obj_text in self._extract_json_objects(candidate):
                try:
                    payload = json.loads(obj_text)
                    if "tool" in payload and "args" in payload:
                        return payload
                except json.JSONDecodeError:
                    continue
        return None

    def _extract_json_objects(self, text: str) -> List[str]:
        chunks: List[str] = []
        start = -1
        depth = 0
        for i, ch in enumerate(text):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                if depth > 0:
                    depth -= 1
                    if depth == 0 and start != -1:
                        chunks.append(text[start : i + 1])
                        start = -1
        return chunks

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
            result = self.tools.run_command(args["command"], args.get("timeout_sec", 120))
        else:
            return f"Unknown tool: {tool}"

        status = "OK" if result.ok else "ERROR"
        return f"{status}: {result.message}"
