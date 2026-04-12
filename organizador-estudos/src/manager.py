"""Gerenciador de tarefas de estudo."""

from datetime import datetime


class TaskManager:
    """Gerencia tarefas de estudo com operações de CRUD."""

    def __init__(self):
        self.tasks = []
        self._next_id = 1

    def add_task(self, subject, description, deadline=None):
        """Adiciona uma nova tarefa de estudo.

        Args:
            subject: Disciplina ou matéria.
            description: Descrição da tarefa.
            deadline: Prazo no formato DD/MM/AAAA (opcional).

        Returns:
            A tarefa criada.

        Raises:
            ValueError: Se subject ou description estiverem vazios,
                        ou se o deadline tiver formato inválido.
        """
        if not subject or not subject.strip():
            raise ValueError("A disciplina não pode ser vazia.")
        if not description or not description.strip():
            raise ValueError("A descrição não pode ser vazia.")

        parsed_deadline = None
        if deadline:
            try:
                parsed_deadline = datetime.strptime(deadline.strip(), "%d/%m/%Y").strftime(
                    "%d/%m/%Y"
                )
            except ValueError as err:
                raise ValueError(
                    "Formato de data inválido. Use DD/MM/AAAA."
                ) from err

        task = {
            "id": self._next_id,
            "subject": subject.strip(),
            "description": description.strip(),
            "deadline": parsed_deadline,
            "completed": False,
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
        self.tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self, subject=None, only_pending=False):
        """Lista tarefas com filtros opcionais.

        Args:
            subject: Filtra por disciplina (opcional).
            only_pending: Se True, retorna apenas tarefas não concluídas.

        Returns:
            Lista de tarefas filtradas.
        """
        result = self.tasks

        if subject:
            result = [
                t for t in result if t["subject"].lower() == subject.strip().lower()
            ]

        if only_pending:
            result = [t for t in result if not t["completed"]]

        return result

    def complete_task(self, task_id):
        """Marca uma tarefa como concluída.

        Args:
            task_id: ID da tarefa.

        Returns:
            A tarefa atualizada.

        Raises:
            ValueError: Se o ID não for encontrado ou a tarefa já estiver concluída.
        """
        task = self._find_task(task_id)

        if task["completed"]:
            raise ValueError(f"A tarefa #{task_id} já está concluída.")

        task["completed"] = True
        return task

    def remove_task(self, task_id):
        """Remove uma tarefa pelo ID.

        Args:
            task_id: ID da tarefa.

        Returns:
            A tarefa removida.

        Raises:
            ValueError: Se o ID não for encontrado.
        """
        task = self._find_task(task_id)
        self.tasks.remove(task)
        return task

    def get_summary(self):
        """Retorna um resumo geral das tarefas.

        Returns:
            Dicionário com total, concluídas, pendentes e disciplinas.
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed

        subjects = {}
        for task in self.tasks:
            subj = task["subject"]
            if subj not in subjects:
                subjects[subj] = {"total": 0, "completed": 0}
            subjects[subj]["total"] += 1
            if task["completed"]:
                subjects[subj]["completed"] += 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "subjects": subjects,
        }

    def _find_task(self, task_id):
        """Busca uma tarefa pelo ID.

        Raises:
            ValueError: Se o ID não for encontrado.
        """
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise ValueError(f"Tarefa com ID #{task_id} não encontrada.")
