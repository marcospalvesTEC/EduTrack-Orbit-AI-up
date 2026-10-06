"""Native global search and notifications for Orbit pages."""

from __future__ import annotations

from datetime import date

import streamlit as st

from src.models.subject import Subject
from src.models.task import Task, TaskStatus

ROUTES = (
    ("Início", "app.py", ("inicio", "início", "home")),
    ("Disciplinas", "pages/2_Disciplinas.py", ("disciplina", "disciplinas", "materia", "matéria")),
    ("Tarefas", "pages/3_Tarefas.py", ("tarefa", "tarefas", "atividade", "atividades")),
    ("Agenda", "pages/4_Agenda.py", ("agenda", "calendario", "calendário", "evento")),
    ("Relatórios", "pages/5_Relatorios.py", ("relatorio", "relatório", "relatorios", "relatórios")),
    ("Assistente", "pages/6_Assistente.py", ("assistente", "orbit", "ia")),
    ("Meu perfil", "pages/4_Perfil.py", ("perfil", "conta")),
    (
        "Configurações",
        "pages/7_Configuracoes.py",
        ("configuracao", "configuração", "configuracoes", "configurações"),
    ),
)


def _matches(query: str, text: str) -> bool:
    return query.casefold() in text.casefold()


def render_global_actions(
    subjects: list[Subject],
    tasks: list[Task],
    *,
    key_prefix: str,
) -> None:
    """Render real search and notification controls."""
    # ORBIT-PURPLE-BELL START
    st.markdown(
        f"""
<style>
/* SINO ORBIT REAL — NÃO É EMOJI. */
div[data-testid="stHorizontalBlock"]:has(.st-key-{key_prefix}_global_search)
[data-testid="stPopover"] > button {{
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    height: 50px !important;
    min-height: 50px !important;
    max-height: 50px !important;
    padding: 0 !important;
    margin-left: auto !important;
    border: 1.5px solid #8b5cf6 !important;
    border-radius: 999px !important;
    background: #ffffff !important;
    color: transparent !important;
    font-size: 0 !important;
    line-height: 0 !important;
    box-shadow: none !important;
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

div[data-testid="stHorizontalBlock"]:has(.st-key-{key_prefix}_global_search)
[data-testid="stPopover"] > button:hover {{
    border-color: #7c3aed !important;
    background: #f7f3ff !important;
}}

div[data-testid="stHorizontalBlock"]:has(.st-key-{key_prefix}_global_search)
[data-testid="stPopover"] > button p,
div[data-testid="stHorizontalBlock"]:has(.st-key-{key_prefix}_global_search)
[data-testid="stPopover"] > button svg {{
    display: none !important;
}}

div[data-testid="stHorizontalBlock"]:has(.st-key-{key_prefix}_global_search)
[data-testid="stPopover"] > button::before {{
    content: "" !important;
    display: block !important;
    width: 22px !important;
    height: 22px !important;
    background: #7c3aed !important;

    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 22c1.1 0 1.99-.9 1.99-2h-3.98c0 1.1.89 2 1.99 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5S10.5 3.17 10.5 4v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z'/%3E%3C/svg%3E") !important;
    -webkit-mask-repeat: no-repeat !important;
    -webkit-mask-position: center !important;
    -webkit-mask-size: contain !important;

    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 22c1.1 0 1.99-.9 1.99-2h-3.98c0 1.1.89 2 1.99 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5S10.5 3.17 10.5 4v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z'/%3E%3C/svg%3E") !important;
    mask-repeat: no-repeat !important;
    mask-position: center !important;
    mask-size: contain !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )
    # ORBIT-PURPLE-BELL END
    # ORBIT-HIDE-GLOBAL-SEARCH START
    st.markdown(
        f"""
<style>
/* Remove visualmente a busca das telas que usam render_global_actions.
   O widget continua existindo para preservar compatibilidade com os testes,
   mas não aparece na interface. */

/* Esconde o campo de busca. */
.st-key-{key_prefix}_global_search {{
    display: none !important;
}}

/* Esconde a coluna que contém somente a busca. */
div[data-testid="column"]:has(.st-key-{key_prefix}_global_search) {{
    display: none !important;
}}

/* Mantém apenas o sino alinhado à direita. */
div[data-testid="stHorizontalBlock"]:has(.st-key-{key_prefix}_global_notifications) {{
    justify-content: flex-end !important;
    align-items: center !important;
}}

div[data-testid="column"]:has(.st-key-{key_prefix}_global_notifications) {{
    flex: 0 0 56px !important;
    width: 56px !important;
    min-width: 56px !important;
    margin-left: auto !important;
}}

/* Sino roxo no mesmo padrão Orbit. */
.st-key-{key_prefix}_global_notifications button {{
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    height: 50px !important;
    min-height: 50px !important;
    padding: 0 !important;
    border: 1.5px solid #8b5cf6 !important;
    border-radius: 50% !important;
    background: #ffffff !important;
    color: #7c3aed !important;
    box-shadow: none !important;
}}

.st-key-{key_prefix}_global_notifications button:hover {{
    border-color: #7c3aed !important;
    background: #f7f3ff !important;
}}

.st-key-{key_prefix}_global_notifications button svg {{
    color: #7c3aed !important;
}}

/* Se o componente usa popover para notificações. */
.st-key-{key_prefix}_global_notifications [data-testid="stPopover"] > button {{
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    height: 50px !important;
    min-height: 50px !important;
    padding: 0 !important;
    border: 1.5px solid #8b5cf6 !important;
    border-radius: 50% !important;
    background: #ffffff !important;
    color: #7c3aed !important;
    box-shadow: none !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )
    # ORBIT-HIDE-GLOBAL-SEARCH END
    # ORBIT-GLOBAL-ACTIONS-PURPLE-CSS START
    st.markdown(
        f"""
<style>
/* Mantém os widgets e keys originais; altera somente o visual. */

/* Busca */
.st-key-{key_prefix}_global_search div[data-baseweb="input"] {{
    min-height: 50px !important;
    border: 1.5px solid #8b5cf6 !important;
    border-radius: 999px !important;
    background: #ffffff !important;
    box-shadow: none !important;
}}

.st-key-{key_prefix}_global_search div[data-baseweb="input"]:hover {{
    border-color: #7c3aed !important;
}}

.st-key-{key_prefix}_global_search div[data-baseweb="input"]:focus-within {{
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, .12) !important;
}}

.st-key-{key_prefix}_global_search input {{
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
}}

.st-key-{key_prefix}_global_search input::placeholder {{
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
    opacity: 1 !important;
}}

/* Sino */
.st-key-{key_prefix}_global_notifications button {{
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    height: 50px !important;
    min-height: 50px !important;
    border: 1.5px solid #8b5cf6 !important;
    border-radius: 50% !important;
    background: #ffffff !important;
    color: #7c3aed !important;
    box-shadow: none !important;
}}

.st-key-{key_prefix}_global_notifications button:hover {{
    border-color: #7c3aed !important;
    background: #f7f3ff !important;
}}

.st-key-{key_prefix}_global_notifications button svg {{
    color: #7c3aed !important;
    fill: none !important;
}}

/* Fallback caso o sino esteja dentro do container global sem key própria. */
.st-key-{key_prefix}_global_actions [data-testid="stButton"] button {{
    border-color: #8b5cf6 !important;
}}

.stApp:has(.orbit-dashboard-dark)
.st-key-{key_prefix}_global_search div[data-baseweb="input"] {{
    background: #171a2e !important;
    border-color: #8b5cf6 !important;
}}

.stApp:has(.orbit-dashboard-dark)
.st-key-{key_prefix}_global_search input {{
    color: #f5f3ff !important;
    -webkit-text-fill-color: #f5f3ff !important;
}}

.stApp:has(.orbit-dashboard-dark)
.st-key-{key_prefix}_global_notifications button {{
    background: #171a2e !important;
    border-color: #8b5cf6 !important;
    color: #c4b5fd !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )
    # ORBIT-GLOBAL-ACTIONS-PURPLE-CSS END
    with st.container(key=f"{key_prefix}_global_actions"):
        search_col, bell_col = st.columns([6, 1], vertical_alignment="center")
        with search_col:
            query = st.text_input(
                "Busca global",
                placeholder="Buscar...",
                label_visibility="collapsed",
                key=f"{key_prefix}_global_search",
            )
        with bell_col:
            with st.popover("Notificações", help="Notificações", use_container_width=False):
                pending = sorted(
                    (task for task in tasks if task.status != TaskStatus.CONCLUIDA),
                    key=lambda task: (task.due_date, task.title),
                )
                overdue = [task for task in pending if task.is_overdue]
                st.markdown("**Notificações**")
                if overdue:
                    st.error(f"{len(overdue)} tarefa(s) atrasada(s).")
                upcoming = [
                    task for task in pending if 0 <= (task.due_date - date.today()).days <= 7
                ]
                if upcoming:
                    for task in upcoming[:5]:
                        days = (task.due_date - date.today()).days
                        when = "hoje" if days == 0 else f"em {days} dia(s)"
                        st.caption(f"• {task.title} — {when}")
                elif not overdue:
                    st.caption("Nenhuma notificação nova.")

    clean = query.strip()
    if not clean:
        return

    with st.container(key=f"{key_prefix}_global_search_results"):
        st.markdown("**Resultados da busca**")
        result_count = 0

        matched_subjects = [subject for subject in subjects if _matches(clean, subject.name)]
        matched_tasks = [
            task
            for task in tasks
            if _matches(clean, task.title) or _matches(clean, task.subject_name)
        ]

        if matched_subjects:
            st.caption("Disciplinas")
            for subject in matched_subjects[:5]:
                st.page_link("pages/2_Disciplinas.py", label=f"📚 {subject.name}")
                result_count += 1

        if matched_tasks:
            st.caption("Tarefas")
            for task in matched_tasks[:5]:
                st.page_link(
                    "pages/3_Tarefas.py",
                    label=f"✅ {task.title} · {task.subject_name}",
                )
                result_count += 1

        matched_routes = [
            (label, path)
            for label, path, aliases in ROUTES
            if _matches(clean, label) or any(_matches(clean, alias) for alias in aliases)
        ]
        if matched_routes:
            st.caption("Páginas")
            for label, path in matched_routes:
                st.page_link(path, label=f"↗ {label}")
                result_count += 1

        if result_count == 0:
            st.info("Nenhum resultado encontrado.")
