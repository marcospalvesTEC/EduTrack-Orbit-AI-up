"""Approved Desktop Light Figma home overview, rendered with real application data.

Source: EduTrack Figma frame 46:2. The local SVGs are exact Figma exports.
"""

from __future__ import annotations

import base64
from datetime import date, timedelta
from html import escape
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

from src.core.metrics import calculate_subject_progress
from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.ui.orbit_global_actions import render_global_actions

if TYPE_CHECKING:
    from src.ui.figma_agenda import AgendaEvent

ASSETS = Path(__file__).parent / "assets"


def icon(name: str, alt: str = "") -> str:
    """Return an exported Figma icon as a durable, self-contained image."""
    svg = (ASSETS / f"{name}.svg").read_bytes()
    encoded = base64.b64encode(svg).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{encoded}" alt="{escape(alt)}">'


def safe(value: object) -> str:
    return escape(str(value), quote=True)


def render_dashboard(
    user: dict[str, str],
    subjects: list[Subject],
    tasks: list[Task],
    metrics: dict[str, float | int],
    agenda_events: list[AgendaEvent] | None = None,
) -> None:
    """Use Figma's desktop structure with data derived from the existing service."""
    theme_class = " orbit-dashboard-dark" if st.session_state.get("edutrack_dark_mode") else ""
    css = (Path(__file__).parent / "figma_dashboard.css").read_text(encoding="utf-8")
    if theme_class:
        css += '[data-testid="stSidebar"] { background: #1b2030; border-color: #323b51; }'
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    render_global_actions(subjects, tasks, key_prefix="dashboard")
    first_name = safe(user.get("name", "Estudante").split()[0])
    completion = round(float(metrics["completion_rate"]))
    today = date.today()
    upcoming = sorted(
        (task for task in tasks if task.status != TaskStatus.CONCLUIDA),
        key=lambda task: (task.due_date, task.title),
    )
    next_delivery = (
        f"{safe(upcoming[0].subject_name)} · {upcoming[0].due_date:%d/%m}"
        if upcoming
        else "Nenhuma entrega pendente"
    )
    focus_task = next(
        (task for task in upcoming if task.priority.value == "Alta"),
        upcoming[0] if upcoming else None,
    )
    focus = safe(focus_task.title) if focus_task else "Cadastre sua primeira tarefa"

    subject_rows = (
        "".join(
            '<div class="orbit-row"><span class="orbit-dot" aria-hidden="true"></span>'
            f'<div class="orbit-row-copy"><span>{safe(subject.name)}</span>'
            f"<small>{safe(subject.professor)}</small></div>"
            f"<strong>{calculate_subject_progress(tasks, subject.id)['completion_rate']:g}%</strong></div>"
            for subject in subjects[:4]
        )
        or '<p class="orbit-empty">Nenhuma disciplina cadastrada.</p>'
    )
    task_rows = (
        "".join(
            '<div class="orbit-row"><span class="orbit-ring" aria-hidden="true"></span>'
            f'<div class="orbit-row-copy"><span>{safe(task.title)}</span>'
            f"<small>{safe(task.subject_name)} · {task.due_date:%d/%m} · "
            f"{safe(task.priority.value)}</small></div></div>"
            for task in upcoming[:4]
        )
        or '<p class="orbit-empty">Nenhuma tarefa pendente.</p>'
    )
    task_today_rows = "".join(
        '<div class="orbit-row"><span class="orbit-time">Hoje</span>'
        f'<div class="orbit-row-copy"><span>{safe(task.title)}</span>'
        f"<small>{safe(task.subject_name)}</small></div></div>"
        for task in upcoming
        if task.due_date == today
    )
    event_today_rows = "".join(
        '<div class="orbit-row"><span class="orbit-time">'
        f"{event.starts_at:%H:%M}</span>"
        f'<div class="orbit-row-copy"><span>{safe(event.title)}</span>'
        f"<small>{safe(event.details or event.category)}</small></div></div>"
        for event in sorted(agenda_events or [], key=lambda item: item.starts_at)
        if event.starts_at.date() == today
    )
    today_rows = task_today_rows + event_today_rows
    if not today_rows:
        today_rows = '<p class="orbit-empty">Sem entregas ou eventos para hoje.</p>'

    monday = today - timedelta(days=today.weekday())
    counts = [sum(task.due_date == monday + timedelta(days=i) for task in tasks) for i in range(7)]
    maximum = max(counts, default=0)
    bars = "".join(
        '<div class="orbit-bar-column">'
        f'<div class="orbit-bar" style="height:{max(3, round(100 * count / maximum)) if maximum else 3}%"></div>'
        f"<span>{day}</span></div>"
        for day, count in zip(("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"), counts)
    )
    graph = (
        f'<div class="orbit-chart" role="img" aria-label="{sum(counts)} entregas nesta semana">'
        f'{bars}</div><div class="orbit-week-total">Meta semanal '
        f"<strong>{completion}%</strong></div>"
    )
    tips = [
        (
            f"Comece por {safe(focus_task.title)} e reserve um bloco curto de concentração."
            if focus_task
            else "Cadastre uma tarefa para receber uma recomendação de prioridade."
        ),
        (
            f"Seu progresso está em {completion}%. Concluir uma tarefa pequena ajuda a manter o ritmo."
            if tasks
            else "Adicione suas tarefas da semana para acompanhar o progresso."
        ),
        (
            "Revise as próximas entregas antes de encerrar o estudo de hoje."
            if upcoming
            else "Sua agenda está livre: aproveite para planejar a próxima semana."
        ),
    ]
    tip_items = "".join(f"<li>{tip}</li>" for tip in tips)
    # Figma's sample numbers are intentionally replaced with user-specific values.
    # The two "Ver todas" actions are native Streamlit page links so navigation
    # preserves the authenticated session instead of reloading the app via raw href.
    native_card_css = """
    .st-key-dashboard_card_grid [data-testid="stHorizontalBlock"] { gap: 12px; }
    .st-key-dashboard_card_subjects,
    .st-key-dashboard_card_tasks,
    .st-key-dashboard_card_agenda,
    .st-key-dashboard_card_progress {
      min-height: 340px;
      padding: 18px 12px !important;
      border: 1px solid #e5e7eb !important;
      border-radius: 16px !important;
      background: #fff !important;
      box-shadow: 0 3px 10px rgba(15,23,87,.03);
    }
    .st-key-dashboard_card_subjects [data-testid="stPageLink"] a,
    .st-key-dashboard_card_tasks [data-testid="stPageLink"] a {
      padding: 0 !important;
      min-height: auto !important;
      color: #7c3aed !important;
      background: transparent !important;
      font-size: 10px !important;
      text-decoration: none !important;
      justify-content: flex-end !important;
    }
    .st-key-dashboard_card_subjects [data-testid="stPageLink"] a:hover,
    .st-key-dashboard_card_tasks [data-testid="stPageLink"] a:hover {
      text-decoration: underline !important;
    }
    .orbit-native-card-title {
      margin: 0;
      color: #0f1757;
      font-size: 14px;
      line-height: 19px;
      font-weight: 700;
    }
    .orbit-native-card-badge {
      margin: 0;
      color: #6b7280;
      font-size: 9px;
      line-height: 19px;
      text-align: right;
      white-space: nowrap;
    }
    .orbit-native-card-body { margin-top: 17px; }

    .stApp:has(.orbit-dashboard-dark) .st-key-dashboard_card_subjects,
    .stApp:has(.orbit-dashboard-dark) .st-key-dashboard_card_tasks,
    .stApp:has(.orbit-dashboard-dark) .st-key-dashboard_card_agenda,
    .stApp:has(.orbit-dashboard-dark) .st-key-dashboard_card_progress {
      background: #171a2e !important;
      border-color: #3c4261 !important;
    }
    .stApp:has(.orbit-dashboard-dark) .orbit-native-card-title {
      color: #f5f3ff !important;
    }
    """
    st.markdown(f"<style>{native_card_css}</style>", unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="orbit-dashboard{theme_class}" aria-label="Início do estudante">
  <header class="orbit-topbar"><div><h1>Boa noite, {first_name}</h1>
    <p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-header-icons"><span class="orbit-search">{icon("search")} Buscar...</span>
      <span class="orbit-bell">{icon("bell", "Notificações")}</span></div></header>
  <div class="orbit-content">
    <section class="orbit-hero">
      <div class="orbit-hero-intro"><span class="orbit-eyebrow">✦ VISÃO GERAL</span>
        <h2>Seu percurso<br><em>acadêmico,</em><br>impulsionado por IA.</h2>
        <p>Insights inteligentes para decisões melhores todos os dias.</p></div>
      <div class="orbit-pet"><div class="orbit-pet-placeholder"><strong>Seu Orbit aparecerá aqui</strong>
        <small>Modelo do pet em preparação</small></div>
        <div class="orbit-bubble"><strong>{completion}%</strong><small>das tarefas</small></div></div>
      <div class="orbit-metrics"><div><span>Progresso semanal</span><strong>{completion}% das tarefas</strong></div>
        <div><span>Próxima entrega</span><strong>{next_delivery}</strong></div>
        <div><span>Foco recomendado</span><strong>{focus}</strong></div></div>
    </section>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.container(key="dashboard_card_grid"):
        subject_col, task_col, agenda_col, progress_col = st.columns(4, gap="small")

        with subject_col:
            with st.container(key="dashboard_card_subjects"):
                title_col, link_col = st.columns([3, 1], vertical_alignment="center")
                with title_col:
                    st.markdown(
                        '<h2 class="orbit-native-card-title">Minhas disciplinas</h2>',
                        unsafe_allow_html=True,
                    )
                with link_col:
                    st.page_link("pages/2_Disciplinas.py", label="Ver todas")
                st.markdown(
                    f'<div class="orbit-native-card-body">{subject_rows}</div>',
                    unsafe_allow_html=True,
                )

        with task_col:
            with st.container(key="dashboard_card_tasks"):
                title_col, link_col = st.columns([3, 1], vertical_alignment="center")
                with title_col:
                    st.markdown(
                        '<h2 class="orbit-native-card-title">Tarefas prioritárias</h2>',
                        unsafe_allow_html=True,
                    )
                with link_col:
                    st.page_link("pages/3_Tarefas.py", label="Ver todas")
                st.markdown(
                    f'<div class="orbit-native-card-body">{task_rows}</div>',
                    unsafe_allow_html=True,
                )

        with agenda_col:
            with st.container(key="dashboard_card_agenda"):
                title_col, badge_col = st.columns([3, 1], vertical_alignment="center")
                with title_col:
                    st.markdown(
                        '<h2 class="orbit-native-card-title">Agenda de hoje</h2>',
                        unsafe_allow_html=True,
                    )
                with badge_col:
                    st.markdown(
                        f'<p class="orbit-native-card-badge">{today:%d/%m}</p>',
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f'<div class="orbit-native-card-body">{today_rows}</div>',
                    unsafe_allow_html=True,
                )

        with progress_col:
            with st.container(key="dashboard_card_progress"):
                title_col, badge_col = st.columns([3, 1], vertical_alignment="center")
                with title_col:
                    st.markdown(
                        '<h2 class="orbit-native-card-title">Progresso semanal</h2>',
                        unsafe_allow_html=True,
                    )
                with badge_col:
                    st.markdown(
                        '<p class="orbit-native-card-badge">Esta semana</p>',
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f'<div class="orbit-native-card-body">{graph}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown(
        f"""
<div class="orbit-dashboard{theme_class}">
  <div class="orbit-content">
    <div class="orbit-tip">{icon("tip", "Dica do dia")}
      <div class="orbit-tip-copy"><strong>Dica do dia</strong>
        <span>Pequenos avanços diários geram grandes conquistas.</span></div>
      <details class="orbit-tips"><summary>Ver dicas</summary>
        <div class="orbit-tip-panel"><strong>Recomendações para você</strong><ul>{tip_items}</ul></div>
      </details></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
