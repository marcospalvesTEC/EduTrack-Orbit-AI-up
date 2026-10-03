# EduTrack Orbit AI

Aplicação web educacional para gerenciamento de disciplinas, tarefas, prazos e progresso acadêmico.

## Objetivo

Ajudar estudantes a organizar suas atividades, acompanhar o desempenho e visualizar informações por meio de dashboards e relatórios.

## Tecnologias

- Python
- Streamlit
- Xano
- XanoScript
- Pandas
- ReportLab
- Pytest
- Ruff
- OpenSpec
- Git e GitHub

## Situação do projeto

Projeto desenvolvido na disciplina Innovation Lab: Desenvolvimento Avançado No/Low Code.

A primeira versão utilizará dados simulados. A autenticação e o banco de dados serão integrados posteriormente pelo Xano.

## Estrutura

- `docs/`: documentação acadêmica e de negócio
- `openspec/`: especificações e propostas de mudança
- `pages/`: páginas do Streamlit
- `src/`: código da aplicação
- `tests/`: testes automatizados

## Execução local

Ativar o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar as dependências:

```powershell
python -m pip install -r requirements.txt
```

Executar a aplicação:

```powershell
streamlit run app.py
```

## Segurança

Credenciais, tokens e URLs privadas não devem ser adicionados ao GitHub. Configurações sensíveis serão armazenadas em `.streamlit/secrets.toml`.

## Progresso Acadêmico

### Tarefa 07 — Configuração Inicial do Projeto Streamlit ✅

O ambiente de desenvolvimento do EduTrack Orbit AI foi validado com Python e Streamlit.

Foram confirmados:

- ambiente virtual `.venv`;
- dependências registradas em `requirements.txt`;
- aplicação principal em `app.py`;
- estrutura modular com `pages/`, `src/` e `tests/`;
- execução local do EduTrack Orbit AI em `localhost:8501`.

A documentação e a evidência da atividade estão disponíveis em:

- [`docs/tarefas/tarefa-07-streamlit.md`](docs/tarefas/tarefa-07-streamlit.md)
