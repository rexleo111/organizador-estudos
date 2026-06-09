# Changelog

Registro de mudancas do projeto.

## [1.2.0] - 2026-06-09

### Adicionado
- Integração com Banco de Dados em nuvem (MongoDB Atlas).
- Configuração de variáveis de ambiente (`.env`) para segurança da string de conexão.

### Alterado
- O armazenamento de tarefas passou de arquivo `.json` local para nuvem.
- `README.md` atualizado com instruções de `.env` e equipe de desenvolvimento.

## [1.1.0] - 2026-05-16

### Adicionado

- Integracao com API publica zenquotes.io para frases motivacionais
- Interface web com Flask
- Frase motivacional exibida ao abrir o CLI e na pagina web
- 4 testes de integracao para o modulo de frases (sucesso, API offline, JSON invalido, timeout)
- Deploy da aplicacao no Render
- Procfile para deploy com gunicorn
- Dependencias: requests, flask, gunicorn

### Alterado

- README atualizado com link do deploy e documentacao da API
- Versao atualizada para 1.1.0

## [1.0.0] - 2026-04-12

### Adicionado

- Interface CLI com menu interativo
- Cadastro de tarefas com disciplina, descricao e prazo opcional
- Listagem com filtro por disciplina e status
- Marcacao de tarefa como concluida
- Remocao de tarefas
- Resumo geral com contagem por disciplina
- Persistencia em arquivo JSON
- 17 testes automatizados com pytest
- Linting com Ruff
- Pipeline de CI com GitHub Actions
- README com instrucoes de uso
- Licenca MIT
