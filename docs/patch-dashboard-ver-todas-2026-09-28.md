# Correção — “Ver todas” do Dashboard

**Data:** 28/09/2026

## Problema

Os textos `Ver todas` dos cards **Minhas disciplinas** e **Tarefas prioritárias**
eram renderizados como conteúdo visual e não executavam navegação.

## Correção

Os dois atalhos agora usam `st.page_link`, componente nativo do Streamlit:

- `Minhas disciplinas → Ver todas → pages/2_Disciplinas.py`
- `Tarefas prioritárias → Ver todas → pages/3_Tarefas.py`

Isso evita navegação por `href` bruto, preservando a sessão autenticada do usuário.

## Arquivo alterado

```text
src/ui/figma_dashboard.py
```

## Validação

1. Abrir a tela inicial.
2. Clicar em `Ver todas` no card **Minhas disciplinas**.
3. Confirmar que abre **Disciplinas** sem pedir login novamente.
4. Voltar ao Início.
5. Clicar em `Ver todas` no card **Tarefas prioritárias**.
6. Confirmar que abre **Tarefas** sem pedir login novamente.


## Ajuste dos testes

O Dashboard passou a renderizar mais de um bloco Markdown/Streamlit para permitir `st.page_link` nativo dentro dos cards. Por isso, os testes foram atualizados para validar o HTML completo renderizado (`\n`.join(rendered)) em vez de apenas o último bloco (`rendered[-1]`).

Isso preserva as verificações de nome do usuário, datas e tarefas, eventos da agenda, tema escuro e navegação segura.


## Ajuste final de rótulos

Os testes esperavam os textos `Ver todas as disciplinas` e `Ver todas as tarefas`, mas a interface aprovada usa apenas `Ver todas` nos dois cards.

As expectativas automatizadas foram alinhadas ao rótulo real da interface, mantendo a validação dos destinos `pages/2_Disciplinas.py` e `pages/3_Tarefas.py`.
