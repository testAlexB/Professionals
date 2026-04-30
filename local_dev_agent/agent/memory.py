from __future__ import annotations

import json
from pathlib import Path
from typing import List


class LessonMemory:
    def __init__(self, memory_file: Path) -> None:
        self.memory_file = memory_file
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.memory_file.exists():
            self._write([])

    def _read(self) -> List[str]:
        raw = self.memory_file.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        return json.loads(raw)

    def _write(self, lessons: List[str]) -> None:
        self.memory_file.write_text(
            json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add_lesson(self, lesson: str) -> None:
        lesson = lesson.strip()
        if not lesson:
            return
        lessons = self._read()
        if lesson not in lessons:
            lessons.append(lesson)
            self._write(lessons)

    def all_lessons(self) -> List[str]:
        return self._read()
