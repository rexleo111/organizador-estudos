"""Módulo de armazenamento no Banco de Dados MongoDB."""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["organizador_db"]
collection = db["tarefas_state"]


def load_tasks():
    """Carrega tarefas do MongoDB.

    Returns:
        Tupla (tasks, next_id) com a lista de tarefas e o próximo ID.
    """
    try:
        documento = collection.find_one({"_id": "estado_geral"})
        if documento:
            return documento.get("tasks", []), documento.get("next_id", 1)
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")

    return [], 1


def save_tasks(tasks, next_id):
    """Salva tarefas no MongoDB.

    Args:
        tasks: Lista de tarefas.
        next_id: Próximo ID disponível.
    """
    try:
        collection.update_one(
            {"_id": "estado_geral"},
            {"$set": {"tasks": tasks, "next_id": next_id}},
            upsert=True
        )
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
