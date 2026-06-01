"""Organizador de Estudos - Interface Web (Flask)."""

from flask import Flask, redirect, render_template_string, request, url_for

from src.manager import TaskManager
from src.quotes import fetch_quote, translate_quote
from src.storage import load_tasks, save_tasks

app = Flask(__name__)

manager = TaskManager()
tasks, next_id = load_tasks()
manager.tasks = tasks
manager._next_id = next_id

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Organizador de Estudos</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, sans-serif;
            background: #f5f5f5;
            color: #333;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { margin-bottom: 6px; }
        .quote {
            background: #fff;
            border-left: 4px solid #555;
            padding: 12px 16px;
            margin: 16px 0;
            font-style: italic;
            color: #555;
        }
        .quote .author {
            display: block;
            margin-top: 6px;
            font-style: normal;
            font-size: 0.9em;
            color: #888;
        }
        .section {
            background: #fff;
            padding: 16px;
            margin: 16px 0;
            border-radius: 6px;
        }
        .section h2 { margin-bottom: 12px; font-size: 1.1em; }
        input, button {
            padding: 8px 12px;
            font-size: 0.95em;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input { width: 100%; margin-bottom: 8px; }
        button {
            background: #333;
            color: #fff;
            border: none;
            cursor: pointer;
            margin-top: 4px;
        }
        button:hover { background: #555; }
        .task-item {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .task-item:last-child { border-bottom: none; }
        .task-info { flex: 1; }
        .task-actions a {
            margin-left: 8px;
            text-decoration: none;
            font-size: 0.85em;
            color: #555;
        }
        .task-actions a:hover { color: #000; }
        .completed { text-decoration: line-through; color: #999; }
        .summary-item { padding: 4px 0; }
        .empty { color: #999; font-style: italic; }
    </style>
</head>
<body>
    <h1>Organizador de Estudos</h1>

    {% if quote %}
    <div class="quote">
        "{{ quote.text }}"
        <span class="author">- {{ quote.author }}</span>
    </div>
    {% endif %}

    <div class="section">
        <h2>Adicionar tarefa</h2>
        <form method="POST" action="/add">
            <input type="text" name="subject" placeholder="Disciplina" required>
            <input type="text" name="description" placeholder="Descricao" required>
            <input type="text" name="deadline" placeholder="Prazo (DD/MM/AAAA) - opcional">
            <button type="submit">Adicionar</button>
        </form>
    </div>

    <div class="section">
        <h2>Tarefas ({{ tasks|length }})</h2>
        {% if tasks %}
            {% for task in tasks %}
            <div class="task-item">
                <div class="task-info {% if task.completed %}completed{% endif %}">
                    #{{ task.id }} [{{ task.subject }}] {{ task.description }}
                    {% if task.deadline %} | Prazo: {{ task.deadline }}{% endif %}
                </div>
                <div class="task-actions">
                    {% if not task.completed %}
                    <a href="/complete/{{ task.id }}">[concluir]</a>
                    {% endif %}
                    <a href="/remove/{{ task.id }}">[remover]</a>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <p class="empty">Nenhuma tarefa cadastrada.</p>
        {% endif %}
    </div>

    <div class="section">
        <h2>Resumo</h2>
        <div class="summary-item">Total: {{ summary.total }}</div>
        <div class="summary-item">Concluidas: {{ summary.completed }}</div>
        <div class="summary-item">Pendentes: {{ summary.pending }}</div>
        {% if summary.subjects %}
            <br>
            <strong>Por disciplina:</strong>
            {% for subj, info in summary.subjects.items() %}
            <div class="summary-item">
                {{ subj }}: {{ info.completed }}/{{ info.total }} concluidas
            </div>
            {% endfor %}
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    quote = fetch_quote()
    
    if quote:

        texto_traduzido = translate_quote(quote["text"])
        
        # Se a API de tradução retornar sucesso, substitui o texto em inglês
        # Se falhar (retornar None), o if é ignorado e o texto original em inglês é mantido
        if texto_traduzido:
            quote["text"] = texto_traduzido

    summary = manager.get_summary()
    
    return render_template_string(
        PAGE_TEMPLATE,
        tasks=manager.tasks,
        summary=summary,
        quote=quote,
    )


@app.route("/add", methods=["POST"])
def add():
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    deadline = request.form.get("deadline", "").strip() or None

    try:
        manager.add_task(subject, description, deadline)
        save_tasks(manager.tasks, manager._next_id)
    except ValueError:
        pass

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete(task_id):
    try:
        manager.complete_task(task_id)
        save_tasks(manager.tasks, manager._next_id)
    except ValueError:
        pass

    return redirect(url_for("index"))


@app.route("/remove/<int:task_id>")
def remove(task_id):
    try:
        manager.remove_task(task_id)
        save_tasks(manager.tasks, manager._next_id)
    except ValueError:
        pass

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
