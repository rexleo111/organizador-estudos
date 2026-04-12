## Descricao do Problema

Muitos estudantes, tanto no ensino medio quanto no superior, tem dificuldade para manter uma rotina de estudos organizada. Sem um planejamento minimo, e comum acumular materia, perder prazos e acabar estudando de forma desorganizada. Esse problema atinge especialmente quem nao tem acesso a aplicativos pagos ou plataformas mais completas de produtividade.

## Proposta da Solucao

O Organizador de Estudos e uma aplicacao de linha de comando que permite cadastrar tarefas de estudo por disciplina, acompanhar o que ja foi feito e o que ainda esta pendente, definir prazos e ter uma visao geral do progresso. A ideia e oferecer algo simples, leve e que funcione sem internet.

## Publico-alvo

Estudantes com dificuldade de organizacao, pessoas que preferem ferramentas de terminal e estudantes de computacao que queiram integrar a ferramenta no dia a dia.

## Funcionalidades

- Adicionar tarefa com disciplina, descricao e prazo opcional
- Listar tarefas com filtro por disciplina ou por status (pendente/concluida)
- Marcar tarefa como concluida
- Remover tarefa
- Ver resumo geral com contagem por disciplina
- Persistencia automatica em arquivo JSON

## Tecnologias

- Python 3.9+
- pytest (testes)
- Ruff (linting)
- GitHub Actions (CI)
- JSON para armazenamento local

## Instalacao

Voce precisa ter Python 3.9 ou superior instalado.

```bash
# Clone o repositorio
git clone https://github.com/rexleo111/organizador-estudos.git
cd organizador-estudos

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instale as dependencias
pip install -r requirements.txt
```

## Como executar

```bash
python -m src.main
```

Ao rodar, o programa exibe um menu no terminal:

```
==================================================
  Organizador de Estudos  v1.0.0
==================================================

--- MENU ---
[1] Adicionar tarefa
[2] Listar tarefas
[3] Concluir tarefa
[4] Remover tarefa
[5] Ver resumo
[0] Sair

Escolha uma opcao: 1

--- Adicionar Tarefa ---
Disciplina: Matematica
Descricao: Resolver lista de derivadas
Prazo (DD/MM/AAAA ou Enter para pular): 20/08/2026

Tarefa #1 adicionada com sucesso.
```

## Como rodar os testes

```bash
pytest -v
```

## Como rodar o lint

```bash
ruff check src/ tests/
```

Para corrigir problemas simples automaticamente:

```bash
ruff check src/ tests/ --fix
```

## Versao atual

1.0.0

## Autor

Leonardo C. P. H.

## Repositorio

https://github.com/rexleo111/organizador-estudos

## Licenca

MIT
