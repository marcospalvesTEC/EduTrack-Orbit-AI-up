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
            with st.popover("🔔", help="Notificações", use_container_width=True):
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
