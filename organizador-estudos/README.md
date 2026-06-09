# Organizador de Estudos

Aplicacao publicada: https://organizador-estudos-9mlh.onrender.com

## Descricao do Problema

Muitos estudantes, tanto no ensino medio quanto no superior, tem dificuldade para manter uma rotina de estudos organizada. Sem um planejamento minimo, e comum acumular materia, perder prazos e acabar estudando de forma desorganizada. Esse problema atinge especialmente quem nao tem acesso a aplicativos pagos ou plataformas mais completas de produtividade.

## Proposta da Solucao

O Organizador de Estudos e uma aplicacao de linha de comando (e tambem web) que permite cadastrar tarefas de estudo por disciplina, acompanhar o que ja foi feito e o que ainda esta pendente, definir prazos e ter uma visao geral do progresso. Ao abrir, o programa exibe uma frase motivacional obtida de uma API publica, para incentivar o estudante.

## Publico-alvo

Estudantes com dificuldade de organizacao, pessoas que preferem ferramentas de terminal e estudantes de computacao que queiram integrar a ferramenta no dia a dia.

## Funcionalidades

- Adicionar tarefa com disciplina, descricao e prazo opcional
- Listar tarefas com filtro por disciplina ou por status (pendente/concluida)
- Marcar tarefa como concluida
- Remover tarefa
- Ver resumo geral com contagem por disciplina
- Persistencia automatica em arquivo JSON
- Frase motivacional ao abrir (via API publica zenquotes.io)
- Interface web com Flask (alem da CLI)

## Tecnologias

- Python 3.9+
- pytest (testes)
- Ruff (linting)
- GitHub Actions (CI)
- MongoDB Atlas (Banco de Dados em Nuvem)
- requests (consumo de API)
- Flask (interface web)
- Render (deploy)

## API Publica Utilizada

A aplicacao consome a API do zenquotes.io (https://zenquotes.io) para exibir uma frase motivacional aleatoria ao usuario. A requisicao e feita via HTTP GET ao endpoint /api/random. Caso a API esteja fora do ar ou a conexao falhe, o programa continua funcionando normalmente, apenas sem exibir a frase.

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

# Instale as dependencias
pip install -r requirements.txt

# Configuração do Banco de Dados
Crie um arquivo chamado `.env` na raiz do projeto e adicione a sua URI do MongoDB:
MONGO_URI="sua_string_de_conexao_aqui"

## Como executar

### CLI (terminal)

```bash
python -m src.main
```

### Web (Flask)

```bash
python -m src.app
```

Acesse http://localhost:5000 no navegador.

### Exemplo de uso (CLI)

```
==================================================
  Organizador de Estudos  v1.1.0
==================================================

  "The only way to do great work is to love what you do."
  - Steve Jobs

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

1.1.0

## Autor

Leonardo C. P. H.

## Repositorio

https://github.com/rexleo111/organizador-estudos

## Licenca

MIT

## Equipe de Desenvolvimento
- Leonardo Cespedes P. Huard
- Joao Vitor M. Peres
