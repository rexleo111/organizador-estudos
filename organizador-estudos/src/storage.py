"""Módulo de armazenamento em JSON."""

import json
from pathlib import Path

DATA_FILE = Path("data/tasks.json")


def load_tasks():
    """Carrega tarefas do arquivo JSON.

    Returns:
        Tupla (tasks, next_id) com a lista de tarefas e o próximo ID.
    """
    if not DATA_FILE.exists():
        return [], 1

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    tasks = data.get("tasks", [])
    next_id = data.get("next_id", 1)
    return tasks, next_id


def save_tasks(tasks, next_id):
    """Salva tarefas no arquivo JSON.

    Args:
        tasks: Lista de tarefas.
        next_id: Próximo ID disponível.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {"next_id": next_id, "tasks": tasks}

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
