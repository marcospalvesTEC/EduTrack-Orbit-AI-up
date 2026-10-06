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

O EduTrack Orbit AI encontra-se em versão MVP funcional, desenvolvido com Python e Streamlit e integrado ao Xano como backend.

A versão atual possui:

- autenticação e cadastro de usuários;
- persistência de usuários e disciplinas no Xano;
- gerenciamento de disciplinas;
- gerenciamento visual de tarefas acadêmicas;
- agenda acadêmica;
- dashboards e relatórios;
- assistente Orbit;
- personalização por mascotes;
- temas claro e escuro;
- APIs REST para autenticação, disciplinas, tarefas e preferências;
- registro de eventos no backend;
- testes automatizados com Pytest;
- versionamento com Git e GitHub.

Na validação final do projeto, a suíte automatizada apresentou **88 testes aprovados**.

### Observação

Os endpoints CRUD de tarefas acadêmicas estão implementados no backend. Durante a validação final foi identificada uma inconsistência na persistência de uma nova tarefa criada pela interface, permanecendo como ponto de evolução da integração frontend-backend.

## Estrutura

- `docs/`: documentação acadêmica e de negócio
- `openspec/`: especificações e propostas de mudança
- `pages/`: páginas do Streamlit
- `src/`: código da aplicação
- `tests/`: testes automatizados
- `assets/`: recursos visuais da aplicação, incluindo os mascotes Orbit
- `xano/` e `tables/`: arquivos relacionados ao backend e versionamento Xano/XanoScript

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

## Testes

Para executar os testes automatizados:

```powershell
python -m pytest -q
```

Última validação da versão de entrega:

```text
88 passed
```

## Segurança

Credenciais, tokens e URLs privadas não devem ser adicionados ao GitHub. Configurações sensíveis devem permanecer em `.streamlit/secrets.toml` e fora do versionamento público.

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

## Repositório

Projeto disponível em:

https://github.com/marcospalvesTEC/EduTrack-Orbit-AI-up
