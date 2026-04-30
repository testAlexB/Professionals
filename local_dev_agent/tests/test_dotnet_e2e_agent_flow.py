from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from agent.memory import LessonMemory
from agent.orchestrator import AgentOrchestrator
from agent.tools import WorkspaceTools


class FakeLLM:
    def __init__(self, responses):
        self.responses = responses

    def chat(self, _messages):
        return self.responses.pop(0)


def _tool(tool: str, args: dict) -> str:
    return json.dumps({"tool": tool, "args": args}, ensure_ascii=False)


@pytest.mark.skipif(shutil.which("dotnet") is None, reason="dotnet is not installed in environment")
def test_agent_builds_and_tests_dotnet_console_app(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    memory = LessonMemory(tmp_path / "lessons.json")

    program_cs = """
using System;

namespace TextWorkerApp;

public static class Program
{
    public static int Main(string[] args)
    {
        if (args.Length > 0 && args[0] == "--self-test")
        {
            return SelfTestRunner.Run();
        }

        if (args.Length < 1)
        {
            Console.WriteLine("Usage: TextWorkerApp <filePath>");
            return 1;
        }

        var result = TextProcessor.BuildSummary(args[0]);
        Console.WriteLine(result);
        return 0;
    }
}
""".strip()

    text_processor_cs = """
using System;
using System.IO;
using System.Linq;

namespace TextWorkerApp;

public static class TextProcessor
{
    public static string BuildSummary(string filePath)
    {
        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException($"File not found: {filePath}");
        }

        var content = File.ReadAllText(filePath);
        var lines = File.ReadAllLines(filePath).Length;
        var words = content
            .Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries)
            .Length;
        var charsCount = content.Length;
        return $"Lines={lines}; Words={words}; Chars={charsCount}";
    }
}
""".strip()

    self_test_runner_cs = """
using System;
using System.IO;

namespace TextWorkerApp;

public static class SelfTestRunner
{
    public static int Run()
    {
        var temp = Path.Combine(Path.GetTempPath(), $"text-worker-{Guid.NewGuid():N}.txt");
        try
        {
            File.WriteAllText(temp, "one two\\nthree");
            var summary = TextProcessor.BuildSummary(temp);
            if (summary != "Lines=2; Words=3; Chars=13")
            {
                Console.WriteLine($"FAILED summary mismatch: {summary}");
                return 1;
            }

            Console.WriteLine("ALL_TESTS_PASSED");
            return 0;
        }
        finally
        {
            if (File.Exists(temp)) File.Delete(temp);
        }
    }
}
""".strip()

    llm = FakeLLM(
        [
            _tool("run_command", {"command": "dotnet new console -n TextWorkerApp"}),
            _tool("write_file", {"path": "TextWorkerApp/Program.cs", "content": program_cs}),
            _tool("write_file", {"path": "TextWorkerApp/TextProcessor.cs", "content": text_processor_cs}),
            _tool("write_file", {"path": "TextWorkerApp/SelfTestRunner.cs", "content": self_test_runner_cs}),
            _tool("run_command", {"command": "dotnet build TextWorkerApp/TextWorkerApp.csproj"}),
            _tool("run_command", {"command": "dotnet run --project TextWorkerApp/TextWorkerApp.csproj -- --self-test"}),
            "Done",
        ]
    )

    agent = AgentOrchestrator(llm, tools, memory)
    result = agent.run_turn(
        "Создай консольное приложение для обработки текстового файла, проверь сборку и обязательно выполни тесты."
    )

    assert result == "Done"
    assert (tmp_path / "TextWorkerApp" / "TextWorkerApp.csproj").exists()
