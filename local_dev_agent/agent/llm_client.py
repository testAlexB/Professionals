from __future__ import annotations

from typing import Any, Dict, List


class OllamaClient:
    def __init__(self, model: str) -> None:
        self.model = model

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        try:
            import ollama
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: ollama. Install with `pip install -r requirements.txt`."
            ) from exc

        response = ollama.chat(model=self.model, messages=messages)
        return response["message"]["content"]
