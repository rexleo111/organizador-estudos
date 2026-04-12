"""Organizador de Estudos - Interface CLI."""

import sys

from src import __version__
from src.manager import TaskManager
from src.storage import load_tasks, save_tasks


def print_header():
    """Exibe o cabecalho do programa."""
    print("=" * 50)
    print(f"  Organizador de Estudos  v{__version__}")
    print("=" * 50)


def print_menu():
    """Exibe o menu principal."""
    print("\n--- MENU ---")
    print("[1] Adicionar tarefa")
    print("[2] Listar tarefas")
    print("[3] Concluir tarefa")
    print("[4] Remover tarefa")
    print("[5] Ver resumo")
    print("[0] Sair")


def format_task(task):
    """Formata uma tarefa para exibicao."""
    status = "[x]" if task["completed"] else "[ ]"
    deadline = f" | Prazo: {task['deadline']}" if task["deadline"] else ""
    return (
        f"  {status} #{task['id']} [{task['subject']}] "
        f"{task['description']}{deadline}"
    )


def action_add(manager):
    """Acao: adicionar tarefa."""
    print("\n--- Adicionar Tarefa ---")
    subject = input("Disciplina: ").strip()
    description = input("Descricao: ").strip()
    deadline = input("Prazo (DD/MM/AAAA ou Enter para pular): ").strip()

    try:
        task = manager.add_task(subject, description, deadline or None)
        print(f"\nTarefa #{task['id']} adicionada com sucesso.")
    except ValueError as e:
        print(f"\nErro: {e}")


def action_list(manager):
    """Acao: listar tarefas."""
    print("\n--- Listar Tarefas ---")
    subject = input("Filtrar por disciplina (ou Enter para todas): ").strip()
    pending_input = input("Mostrar apenas pendentes? (s/N): ").strip().lower()
    only_pending = pending_input == "s"

    tasks = manager.list_tasks(
        subject=subject or None, only_pending=only_pending
    )

    if not tasks:
        print("\nNenhuma tarefa encontrada.")
        return

    print(f"\n{len(tasks)} tarefa(s) encontrada(s):\n")
    for task in tasks:
        print(format_task(task))


def action_complete(manager):
    """Acao: concluir tarefa."""
    print("\n--- Concluir Tarefa ---")
    try:
        task_id = int(input("ID da tarefa: "))
        task = manager.complete_task(task_id)
        print(f"\nTarefa #{task['id']} marcada como concluida.")
    except ValueError as e:
        print(f"\nErro: {e}")


def action_remove(manager):
    """Acao: remover tarefa."""
    print("\n--- Remover Tarefa ---")
    try:
        task_id = int(input("ID da tarefa: "))
        task = manager.remove_task(task_id)
        print(f"\nTarefa #{task['id']} removida.")
    except ValueError as e:
        print(f"\nErro: {e}")


def action_summary(manager):
    """Acao: exibir resumo."""
    summary = manager.get_summary()

    print("\n--- Resumo ---")
    print(f"Total de tarefas: {summary['total']}")
    print(f"Concluidas:       {summary['completed']}")
    print(f"Pendentes:        {summary['pending']}")

    if summary["subjects"]:
        print("\nPor disciplina:")
        for subj, info in summary["subjects"].items():
            print(f"  {subj}: {info['completed']}/{info['total']} concluidas")


def main():
    """Loop principal da aplicacao CLI."""
    print_header()

    manager = TaskManager()

    tasks, next_id = load_tasks()
    manager.tasks = tasks
    manager._next_id = next_id

    actions = {
        "1": action_add,
        "2": action_list,
        "3": action_complete,
        "4": action_remove,
        "5": action_summary,
    }

    while True:
        print_menu()
        choice = input("\nEscolha uma opcao: ").strip()

        if choice == "0":
            save_tasks(manager.tasks, manager._next_id)
            print("\nDados salvos. Ate mais.")
            sys.exit(0)

        action = actions.get(choice)
        if action:
            action(manager)
            save_tasks(manager.tasks, manager._next_id)
        else:
            print("\nOpcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
