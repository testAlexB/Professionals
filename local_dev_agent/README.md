# Local Dev Agent (бесплатный локальный AI-агент для кода)

Этот проект добавляет в репозиторий локального AI-агента, с которым можно общаться в чате и который умеет:

- помогать с задачами по коду (Python / C# и другие языки),
- читать/создавать/обновлять файлы на вашем ПК (в рамках выбранной рабочей папки),
- запоминать ваши правки и пожелания в виде "уроков", чтобы реже повторять ошибки,
- работать без оплаты токенов (через локальную open-source модель в Ollama).

## Что внутри

- `agent/main.py` — CLI-чат,
- `agent/web_app.py` — web-чат (Gradio),
- `agent/llm_client.py` — подключение к Ollama,
- `agent/tools.py` — безопасные инструменты работы с файлами,
- `agent/memory.py` — память (уроки/исправления),
- `agent/orchestrator.py` — цикл "модель ↔ инструменты".

---

## 1) Быстрый старт (Windows)

### Шаг 1. Установить Ollama
1. Скачайте и установите Ollama: https://ollama.com/download
2. Проверьте в PowerShell:
   ```powershell
   ollama --version
   ```

### Шаг 2. Скачать модель для кода

```powershell
ollama pull qwen2.5-coder:14b
```

Если ПК слабее по памяти:

```powershell
ollama pull qwen2.5-coder:7b
```

### Шаг 3. Установить Python-зависимости

```powershell
cd local_dev_agent
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
# для web UI дополнительно:
pip install -r requirements-web.txt
```

---

## 2) Запуск в терминале (CLI)

```powershell
python -m agent.main --workspace "C:\\Users\\<YOU>\\source\\my_project" --model qwen2.5-coder:14b
# опционально: лог всех ответов модели и результатов инструментов:
# --trace-file ".agent_trace.jsonl"
```

Команды в чате:
- `/help`
- `/lesson <текст>`
- `/lessons`
- `/clear`
- `/exit`

---

## 3) Запуск в браузере (web)

```powershell
python -m agent.web_app --workspace "C:\\Users\\<YOU>\\source\\my_project" --model qwen2.5-coder:14b --host 0.0.0.0 --port 7860
# опционально: лог всех ответов модели и результатов инструментов:
# --trace-file ".agent_trace.jsonl"
```

Откройте: `http://localhost:7860`

### Временная публичная ссылка (чтобы "потыкать онлайн")

```powershell
python -m agent.web_app --workspace "C:\\Users\\<YOU>\\source\\my_project" --model qwen2.5-coder:14b --share
```

Gradio выдаст публичный URL (временный), который можно открыть с другого устройства.

---

## 4) Ограничения и безопасность

- Агент работает только внутри папки `--workspace`.
- Выход за пределы рабочей папки блокируется.
- Перед массовыми правками используйте git (`git status`, `git diff`).

---

## 5) "Обучение" без оплаты токенов

Практическая схема:
- вы говорите, что не так,
- добавляете правило через `/lesson ...`,
- агент применяет эти уроки в следующих задачах.

Дополнительно агент умеет выполнять команды внутри `--workspace` через tool `run_command`
с белым списком программ: `dotnet`, `python`, `python3`, `py`, `pytest`.
Агент может выполнять несколько шагов подряд автономно (цепочка tool-вызовов),
пока не получит финальный текстовый ответ.

Это не fine-tuning весов модели, но в реальной разработке обычно сильно помогает.

---

## 6) Тесты

```bash
pytest -q
```


## 7) Проверка качества (что прогонять перед работой)

```bash
pytest -q
python -m agent.main --help
python -m agent.web_app --help
```

Если нет `ollama` или `gradio`, приложение покажет понятную ошибку с подсказкой установки зависимостей.


## 8) Совместимость Python

- CLI/ядро: Python 3.10+
- Web UI (gradio): лучше Python 3.10–3.12.
- На Python 3.13 могут быть конфликты зависимостей gradio/audioop-lts. В таком случае используйте Python 3.12 для web UI.
