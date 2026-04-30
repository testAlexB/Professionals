from pathlib import Path

from agent.memory import LessonMemory
from agent.tools import WorkspaceTools


def test_memory_add_and_read(tmp_path: Path):
    mem = LessonMemory(tmp_path / "lessons.json")
    mem.add_lesson("Rule 1")
    mem.add_lesson("Rule 1")
    mem.add_lesson("Rule 2")
    assert mem.all_lessons() == ["Rule 1", "Rule 2"]


def test_tools_read_write_list(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    w = tools.write_file("src/a.py", "print('hi')")
    assert w.ok

    r = tools.read_file("src/a.py")
    assert r.ok and "print('hi')" in r.message

    l = tools.list_files("src")
    assert l.ok and "src/a.py" in l.message


def test_tools_run_command(tmp_path: Path):
    tools = WorkspaceTools(tmp_path)
    ok = tools.run_command('python -c "print(123)"')
    assert ok.ok and "123" in ok.message

    bad = tools.run_command("bash -lc 'echo hi'")
    assert not bad.ok and "Command not allowed" in bad.message
