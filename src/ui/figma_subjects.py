"""Figma-aligned subjects overview rendered with real academic data."""

from __future__ import annotations

import re
from datetime import date
from hashlib import sha1
from html import escape
from pathlib import Path

import streamlit as st

from src.core.metrics import calculate_subject_progress
from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.ui.figma_dashboard import icon


def safe(value: object) -> str:
    """Escape user-controlled content before adding it to the HTML view."""
    return escape(str(value), quote=True)


def safe_color(value: str) -> str:
    """Accept a six-digit hex color and reject unsafe CSS values."""
    return value if re.fullmatch(r"#[0-9a-fA-F]{6}", value) else "#7c3aed"


def weekly_workload(subjects: list[Subject]) -> int:
    """Estimate weekly hours from each subject workload and academic period."""
    total = 0.0
    for subject in subjects:
        period_days = max((subject.end_date - subject.start_date).days, 7)
        total += subject.workload_hours / max(period_days / 7, 1)
    return round(total)


def filter_subjects(subjects: list[Subject], query: str) -> list[Subject]:
    """Filter subjects by name, code or professor without case sensitivity."""
    normalized = query.strip().casefold()
    if not normalized:
        return subjects
    return [
        subject
        for subject in subjects
        if normalized in subject.name.casefold()
        or normalized in subject.code.casefold()
        or normalized in subject.professor.casefold()
    ]


def render_subjects_header(user: dict[str, str]) -> None:
    """Render the shared Figma header for the subjects route."""
    css = (Path(__file__).parent / "figma_subjects.css").read_text(encoding="utf-8")
    first_name = safe(user.get("name", "Estudante").split()[0])
    theme_class = " orbit-subjects-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="orbit-subjects-page{theme_class}" aria-label="Disciplinas do estudante">
  <header class="orbit-subjects-topbar"><div><h1>Boa noite, {first_name}</h1>
    <p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-subjects-header-icons"><span class="orbit-subjects-global-search">
      {icon("search", "")} Buscar...</span>
      <span class="orbit-subjects-bell">{icon("bell", "Notificações")}</span></div>
  </header>
</div>
""",
        unsafe_allow_html=True,
    )


def render_subject_dialog_theme_marker() -> None:
    """Expose the active theme inside Streamlit's portal-based dialog tree."""
    if st.session_state.get("edutrack_dark_mode"):
        st.markdown(
            '<span class="orbit-subject-dialog-dark" aria-hidden="true"></span>',
            unsafe_allow_html=True,
        )


def render_subject_metrics(subjects: list[Subject], tasks: list[Task]) -> None:
    """Render the three Figma summary cards with calculated values."""
    rates = [
        float(calculate_subject_progress(tasks, subject.id)["completion_rate"])
        for subject in subjects
    ]
    average = round(sum(rates) / len(rates)) if rates else 0
    st.markdown(
        f"""
<section class="orbit-subject-metrics" aria-label="Resumo das disciplinas">
  <div><span>Disciplinas ativas</span><strong>{len(subjects)}</strong></div>
  <div><span>Média de progresso</span><strong>{average}%</strong></div>
  <div><span>Carga semanal</span><strong>{weekly_workload(subjects)} h</strong></div>
</section>
""",
        unsafe_allow_html=True,
    )


def deadline_label(subject: Subject, tasks: list[Task]) -> str:
    pending = sorted(
        (
            task
            for task in tasks
            if str(task.subject_id) == str(subject.id) and task.status != TaskStatus.CONCLUIDA
        ),
        key=lambda task: task.due_date,
    )
    if not pending:
        return "Sem entregas pendentes"
    days = (pending[0].due_date - date.today()).days
    if days < 0:
        return "Entrega atrasada"
    if days == 0:
        return "Próxima entrega: hoje"
    if days == 1:
        return "Próxima entrega: amanhã"
    return f"Próxima entrega: {pending[0].due_date:%d/%m}"


def _card_key(subject: Subject) -> str:
    digest = sha1(str(subject.id).encode(), usedforsecurity=False).hexdigest()[:10]
    return f"subject_card_{digest}"


def render_subject_cards(subjects: list[Subject], tasks: list[Task]) -> Subject | None:
    """Render clickable three-column cards and return the selected subject."""
    if not subjects:
        st.markdown(
            '<div class="orbit-subject-empty">Nenhuma disciplina encontrada.</div>',
            unsafe_allow_html=True,
        )
        return None

    selected = None
    st.markdown('<div class="orbit-subject-grid-marker"></div>', unsafe_allow_html=True)
    for offset in range(0, len(subjects), 3):
        columns = st.columns(3)
        for column, subject in zip(columns, subjects[offset : offset + 3], strict=False):
            progress = calculate_subject_progress(tasks, subject.id)
            key = _card_key(subject)
            container_key = key.replace("subject_card", "subject_container")
            color = safe_color(subject.color_hex)
            with column:
                with st.container(border=True, key=container_key):
                    st.markdown(
                        '<article class="orbit-subject-card">'
                        f'<span class="orbit-subject-accent" style="background:{color}"></span>'
                        f"<h2>{safe(subject.name)}</h2>"
                        f"<p>{safe(subject.professor)}</p>"
                        f"<p>{progress['completion_rate']:g}% concluído · "
                        f"{progress['total_tasks']} tarefas</p>"
                        f"<p>{safe(deadline_label(subject, tasks))}</p>"
                        "</article>",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        f"Abrir resumo de {subject.name}",
                        key=key,
                        use_container_width=True,
                    ):
                        selected = subject
    return selected
