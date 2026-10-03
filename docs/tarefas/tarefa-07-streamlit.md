# Tarefa 07 — Configuração Inicial do Projeto Streamlit

**Disciplina:** Innovation Lab: Desenvolvimento Avançado No/Low Code  
**Projeto:** EduTrack Orbit AI  
**Status:** ✅ Concluída

## Objetivo

Configurar e validar o ambiente inicial do frontend do EduTrack Orbit AI utilizando Python e Streamlit.

A implementação atual do projeto já se encontra em estágio mais avançado que o setup inicial solicitado pela atividade. Por esse motivo, nesta tarefa foi realizada a validação e documentação da estrutura existente, sem substituir ou simplificar a aplicação atual.

## 1. Ambiente Python

O projeto possui ambiente virtual Python configurado na pasta:

`.venv`

Durante a validação da atividade, o ambiente virtual estava ativo no terminal.

## 2. Dependências

O projeto utiliza o arquivo `requirements.txt` para registrar suas principais dependências.

Dependências atualmente configuradas:

- `streamlit>=1.35.0`
- `pandas>=2.2.0`
- `reportlab>=4.1.0`
- `plotly>=5.20.0`
- `pytest>=8.0.0`
- `ruff>=0.4.0`

Além das dependências da aplicação, o projeto já possui ferramentas para testes automatizados e análise de código.

## 3. Aplicação Streamlit

O ponto de entrada principal da aplicação é:

`app.py`

O arquivo utiliza Streamlit e atualmente já possui recursos além do setup básico da atividade, incluindo:

- configuração da página com `st.set_page_config`;
- layout em modo `wide`;
- gerenciamento de sessão;
- autenticação de usuário;
- carregamento de dados acadêmicos;
- dashboard;
- métricas;
- identidade visual personalizada;
- navegação para outras páginas;
- integração com serviços internos do projeto.

A estrutura também está organizada em módulos como:

- `pages/`
- `src/core/`
- `src/services/`
- `src/ui/`
- `.streamlit/`
- `tests/`

## 4. Execução Local

A aplicação foi executada utilizando:

```powershell
streamlit run app.py