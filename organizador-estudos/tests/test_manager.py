"""Testes automatizados do Organizador de Estudos."""

import pytest

from src.manager import TaskManager

# ===== Fixtures =====


@pytest.fixture
def manager():
    """Cria um TaskManager limpo para cada teste."""
    return TaskManager()


@pytest.fixture
def manager_with_tasks(manager):
    """Cria um TaskManager com tarefas pré-cadastradas."""
    manager.add_task("Matemática", "Resolver lista de derivadas", "15/08/2026")
    manager.add_task("Português", "Ler capítulo 3 do livro")
    manager.add_task("Matemática", "Estudar integrais")
    return manager


# ===== Testes de adição (caminho feliz) =====


class TestAddTask:
    """Testes para adicionar tarefas."""

    def test_add_task_successfully(self, manager):
        """Deve adicionar uma tarefa com todos os campos."""
        task = manager.add_task("Matemática", "Estudar derivadas", "20/12/2026")

        assert task["id"] == 1
        assert task["subject"] == "Matemática"
        assert task["description"] == "Estudar derivadas"
        assert task["deadline"] == "20/12/2026"
        assert task["completed"] is False

    def test_add_task_without_deadline(self, manager):
        """Deve adicionar tarefa sem prazo."""
        task = manager.add_task("História", "Resumo da aula")

        assert task["deadline"] is None
        assert task["subject"] == "História"

    def test_add_multiple_tasks_increments_id(self, manager):
        """IDs devem ser sequenciais."""
        t1 = manager.add_task("Mat", "Tarefa 1")
        t2 = manager.add_task("Port", "Tarefa 2")
        t3 = manager.add_task("Hist", "Tarefa 3")

        assert t1["id"] == 1
        assert t2["id"] == 2
        assert t3["id"] == 3


# ===== Testes de entrada inválida =====


class TestInvalidInput:
    """Testes para entradas inválidas."""

    def test_add_task_empty_subject_raises(self, manager):
        """Deve rejeitar disciplina vazia."""
        with pytest.raises(ValueError, match="disciplina"):
            manager.add_task("", "Descrição válida")

    def test_add_task_blank_subject_raises(self, manager):
        """Deve rejeitar disciplina com apenas espaços."""
        with pytest.raises(ValueError, match="disciplina"):
            manager.add_task("   ", "Descrição válida")

    def test_add_task_empty_description_raises(self, manager):
        """Deve rejeitar descrição vazia."""
        with pytest.raises(ValueError, match="descrição"):
            manager.add_task("Matemática", "")

    def test_add_task_invalid_deadline_raises(self, manager):
        """Deve rejeitar data em formato inválido."""
        with pytest.raises(ValueError, match="Formato de data"):
            manager.add_task("Matemática", "Tarefa", "2026-12-20")

    def test_complete_nonexistent_task_raises(self, manager):
        """Deve falhar ao concluir tarefa inexistente."""
        with pytest.raises(ValueError, match="não encontrada"):
            manager.complete_task(999)

    def test_remove_nonexistent_task_raises(self, manager):
        """Deve falhar ao remover tarefa inexistente."""
        with pytest.raises(ValueError, match="não encontrada"):
            manager.remove_task(42)


# ===== Testes de caso limite =====


class TestEdgeCases:
    """Testes de casos limite."""

    def test_complete_already_completed_task_raises(self, manager_with_tasks):
        """Deve impedir conclusão duplicada."""
        manager_with_tasks.complete_task(1)

        with pytest.raises(ValueError, match="já está concluída"):
            manager_with_tasks.complete_task(1)

    def test_list_empty_returns_empty(self, manager):
        """Deve retornar lista vazia quando não há tarefas."""
        result = manager.list_tasks()
        assert result == []

    def test_list_filters_by_subject(self, manager_with_tasks):
        """Deve filtrar tarefas por disciplina."""
        math_tasks = manager_with_tasks.list_tasks(subject="Matemática")
        assert len(math_tasks) == 2
        assert all(t["subject"] == "Matemática" for t in math_tasks)

    def test_list_only_pending(self, manager_with_tasks):
        """Deve listar apenas tarefas pendentes."""
        manager_with_tasks.complete_task(1)

        pending = manager_with_tasks.list_tasks(only_pending=True)
        assert len(pending) == 2
        assert all(not t["completed"] for t in pending)

    def test_remove_then_list_excludes_removed(self, manager_with_tasks):
        """Tarefa removida não deve aparecer na listagem."""
        manager_with_tasks.remove_task(2)

        tasks = manager_with_tasks.list_tasks()
        ids = [t["id"] for t in tasks]
        assert 2 not in ids
        assert len(tasks) == 2


# ===== Testes do resumo =====


class TestSummary:
    """Testes para o resumo de tarefas."""

    def test_summary_counts(self, manager_with_tasks):
        """Deve calcular totais corretamente."""
        manager_with_tasks.complete_task(1)
        summary = manager_with_tasks.get_summary()

        assert summary["total"] == 3
        assert summary["completed"] == 1
        assert summary["pending"] == 2

    def test_summary_empty(self, manager):
        """Resumo sem tarefas deve ter tudo zerado."""
        summary = manager.get_summary()

        assert summary["total"] == 0
        assert summary["completed"] == 0
        assert summary["pending"] == 0
        assert summary["subjects"] == {}

    def test_summary_per_subject(self, manager_with_tasks):
        """Deve agrupar contagens por disciplina."""
        manager_with_tasks.complete_task(1)
        summary = manager_with_tasks.get_summary()

        assert summary["subjects"]["Matemática"]["total"] == 2
        assert summary["subjects"]["Matemática"]["completed"] == 1
        assert summary["subjects"]["Português"]["total"] == 1
