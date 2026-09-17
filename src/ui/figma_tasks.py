"""Figma-aligned task board rendered with real academic data."""

from __future__ import annotations

from datetime import date
from hashlib import sha1
from html import escape
from pathlib import Path

import streamlit as st

from src.models.task import Task, TaskStatus
from src.ui.figma_dashboard import icon


def safe(value: object) -> str:
    """Escape user-controlled content before rendering it as HTML."""
    return escape(str(value), quote=True)


def board_status(task: Task) -> str:
    """Map domain statuses to the three columns defined by the Figma board."""
    if task.status == TaskStatus.CONCLUIDA:
        return "Concluídas"
    if task.status == TaskStatus.EM_ANDAMENTO:
        return "Em andamento"
    return "A fazer"


def filter_tasks(
    tasks: list[Task],
    query: str = "",
    status: str = "Todos os status",
    priority: str = "Todas as prioridades",
) -> list[Task]:
    """Filter task cards by text, board status and priority."""
    normalized = query.strip().casefold()
    visible = [
        task
        for task in tasks
        if not normalized
        or normalized in task.title.casefold()
        or normalized in task.subject_name.casefold()
        or normalized in task.description.casefold()
    ]
    if status != "Todos os status":
        visible = [task for task in visible if board_status(task) == status]
    if priority != "Todas as prioridades":
        visible = [task for task in visible if task.priority.value == priority]
    return visible


def render_tasks_header(user: dict[str, str]) -> None:
    """Render the Figma desktop header and install route-specific styles."""
    css = (Path(__file__).parent / "figma_tasks.css").read_text(encoding="utf-8")
    first_name = safe(user.get("name", "Estudante").split()[0])
    theme_class = " orbit-tasks-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="orbit-tasks-page{theme_class}" aria-label="Tarefas do estudante">
  <header class="orbit-tasks-topbar"><div><h1>Boa noite, {first_name}</h1>
    <p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-tasks-header-icons"><span class="orbit-tasks-global-search">
      {icon("search", "")} Buscar...</span>
      <span class="orbit-tasks-bell">{icon("bell", "Notificações")}</span></div>
  </header>
</div>
""",
        unsafe_allow_html=True,
    )


def render_task_dialog_theme_marker() -> None:
    """Expose the dark theme inside Streamlit's portal-based dialog tree."""
    if st.session_state.get("edutrack_dark_mode"):
        st.markdown(
            '<span class="orbit-task-dialog-dark" aria-hidden="true"></span>',
            unsafe_allow_html=True,
        )


def render_task_metrics(tasks: list[Task]) -> None:
    """Render the three status totals from the official Figma screen."""
    totals = {label: 0 for label in ("A fazer", "Em andamento", "Concluídas")}
    for task in tasks:
        totals[board_status(task)] += 1
    st.markdown(
        f"""
<section class="orbit-task-metrics" aria-label="Resumo das tarefas">
  <div><span>A fazer</span><strong class="todo">{totals['A fazer']}</strong></div>
  <div><span>Em andamento</span><strong class="doing">{totals['Em andamento']}</strong></div>
  <div><span>Concluídas</span><strong class="done">{totals['Concluídas']}</strong></div>
</section>
""",
        unsafe_allow_html=True,
    )


def _task_key(task: Task) -> str:
    digest = sha1(str(task.id).encode(), usedforsecurity=False).hexdigest()[:10]
    return f"task_card_{digest}"


def deadline_text(task: Task) -> str:
    """Return the compact deadline label used on each card."""
    if task.status == TaskStatus.CONCLUIDA:
        return "Concluída"
    days = (task.due_date - date.today()).days
    if days < 0:
        return "Atrasada"
    if days == 0:
        return "Entrega hoje"
    if days == 1:
        return "Entrega amanhã"
    return f"{days} dias"


def render_task_board(tasks: list[Task]) -> Task | None:
    """Render the three-column Kanban and return a clicked task."""
    selected = None
    columns = st.columns(3)
    groups = ("A fazer", "Em andamento", "Concluídas")
    group_keys = {"A fazer": "todo", "Em andamento": "doing", "Concluídas": "done"}
    for column, group in zip(columns, groups, strict=True):
        grouped = [task for task in tasks if board_status(task) == group]
        with column:
            with st.container(border=True, key=f"task_board_{group_keys[group]}"):
                st.markdown(
                    f'<div class="orbit-task-board-title"><strong>{group}</strong>'
                    f"<span>{len(grouped)}</span></div>",
                    unsafe_allow_html=True,
                )
                if not grouped:
                    st.markdown(
                        '<div class="orbit-task-column-empty">Nenhuma tarefa nesta etapa.</div>',
                        unsafe_allow_html=True,
                    )
                for task in grouped:
                    key = _task_key(task)
                    container_key = key.replace("task_card", "task_container")
                    with st.container(border=True, key=container_key):
                        description = task.description.strip()
                        details = description if description else deadline_text(task)
                        st.markdown(
                            '<article class="orbit-task-card">'
                            f"<h2>{safe(task.title)}</h2>"
                            f"<p>{safe(task.subject_name)} · {safe(deadline_text(task))}</p>"
                            '<span class="orbit-task-priority '
                            f'priority-{task.priority.name.lower()}">'
                            f"Prioridade {safe(task.priority.value.lower())}</span>"
                            f'<small title="{safe(description)}">{safe(details)}</small>'
                            "</article>",
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"Abrir tarefa {task.title}", key=key, use_container_width=True
                        ):
                            selected = task
    return selected
