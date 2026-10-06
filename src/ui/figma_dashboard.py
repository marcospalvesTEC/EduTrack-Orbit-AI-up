"""Approved Desktop Light Figma home overview, rendered with real application data.

Source: EduTrack Figma frame 46:2. The local SVGs are exact Figma exports.
"""

from __future__ import annotations


from textwrap import dedent
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
from src.ui.pets import (
    PET_PROFILES,
    load_pet_choice,
    pet_data_uri,
)

if TYPE_CHECKING:
    from src.ui.figma_agenda import AgendaEvent



def _html_block(value: str) -> str:
    """Normalize HTML so Streamlit Markdown never treats indentation as code."""
    return "\n".join(
        line.lstrip()
        for line in value.splitlines()
    ).strip()


ASSETS = Path(__file__).parent / "assets"


def icon(name: str, alt: str = "") -> str:
    """Return an exported Figma icon as a durable, self-contained image."""
    svg = (ASSETS / f"{name}.svg").read_bytes()
    encoded = base64.b64encode(svg).decode("ascii")
    return (
        f'<img src="data:image/svg+xml;base64,{encoded}" '
        f'alt="{escape(alt)}">'
    )


def safe(value: object) -> str:
    """Escape values inserted into HTML."""
    return escape(str(value), quote=True)


def render_dashboard_topbar(
    first_name: str,
    subjects: list[Subject],
    tasks: list[Task],
) -> None:
    """Render the Home top bar with notification bell only."""
    del subjects, tasks

    with st.container(key="dashboard_topbar"):
        greeting_col, bell_col = st.columns(
            [5, 1],
            vertical_alignment="center",
        )

        with greeting_col:
            st.markdown(
                (
                    f'<div class="orbit-native-greeting">'
                    f"<h1>Boa noite, {first_name}</h1>"
                    "<p>Organize, acompanhe e evolua</p>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with bell_col:
            st.button(
                "Notificações",
                key="dashboard_notifications",
                help="Notificações",
                width="stretch",
            )








def render_dashboard(
    user: dict[str, str],
    subjects: list[Subject],
    tasks: list[Task],
    metrics: dict[str, float | int],
    agenda_events: list[AgendaEvent] | None = None,
) -> None:
    """Use Figma's desktop structure with real application data."""

    theme_class = (
        " orbit-dashboard-dark"
        if st.session_state.get("edutrack_dark_mode")
        else ""
    )

    css = (
        Path(__file__).parent / "figma_dashboard.css"
    ).read_text(encoding="utf-8")

    if theme_class:
        css += """
        [data-testid="stSidebar"] {
            background: #1b2030;
            border-color: #323b51;
        }
        """

    st.markdown(
        _html_block(f"<style>{css}</style>"),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # USER / TOP BAR
    # ------------------------------------------------------------------

    first_name = safe(
        user.get("name", "Estudante").split()[0]
    )

    render_dashboard_topbar(
        first_name,
        subjects,
        tasks,
    )

    # ------------------------------------------------------------------
    # ORBIT PET
    # ------------------------------------------------------------------

    selected_pet_key = load_pet_choice(
        st.session_state,
        user,
    )

    if selected_pet_key:
        selected_pet = PET_PROFILES[selected_pet_key]

        pet_name = safe(selected_pet["name"])
        pet_role = safe(selected_pet["role"])
        pet_image = pet_data_uri(selected_pet_key)

        pet_html = f"""
        <div class="orbit-pet-stage orbit-pet-selected">
            <img
                src="{pet_image}"
                alt="{pet_name}"
            >
            <div class="orbit-pet-selected-copy">
                <strong>{pet_name}</strong>
                <small>{pet_role}</small>
            </div>
        </div>
        """

    else:
        pet_html = f"""
        <div class="orbit-pet-stage orbit-pet-selected">
            <img
                src="{pet_data_uri('axolote')}"
                alt="Axalote Mago"
            >
            <div class="orbit-pet-selected-copy">
                <strong>Escolha seu companheiro Orbit</strong>
                <small>Personalize sua jornada acadêmica</small>
            </div>
        </div>
        """

    # ------------------------------------------------------------------
    # DASHBOARD DATA
    # ------------------------------------------------------------------

    completion = round(
        float(metrics["completion_rate"])
    )

    today = date.today()

    upcoming = sorted(
        (
            task
            for task in tasks
            if task.status != TaskStatus.CONCLUIDA
        ),
        key=lambda task: (
            task.due_date,
            task.title,
        ),
    )

    next_delivery = (
        f"{safe(upcoming[0].subject_name)} · "
        f"{upcoming[0].due_date:%d/%m}"
        if upcoming
        else "Nenhuma entrega pendente"
    )

    focus_task = next(
        (
            task
            for task in upcoming
            if task.priority.value == "Alta"
        ),
        upcoming[0] if upcoming else None,
    )

    focus = (
        safe(focus_task.title)
        if focus_task
        else "Cadastre sua primeira tarefa"
    )

    # ------------------------------------------------------------------
    # SUBJECT CARD
    # ------------------------------------------------------------------

    subject_rows = (
        "".join(
            (
                '<div class="orbit-row">'
                '<span class="orbit-dot" aria-hidden="true"></span>'
                '<div class="orbit-row-copy">'
                f"<span>{safe(subject.name)}</span>"
                f"<small>{safe(subject.professor)}</small>"
                "</div>"
                "<strong>"
                f"{calculate_subject_progress(tasks, subject.id)['completion_rate']:g}%"
                "</strong>"
                "</div>"
            )
            for subject in subjects[:4]
        )
        or '<p class="orbit-empty">Nenhuma disciplina cadastrada.</p>'
    )

    # ------------------------------------------------------------------
    # TASK CARD
    # ------------------------------------------------------------------

    task_rows = (
        "".join(
            (
                '<div class="orbit-row">'
                '<span class="orbit-ring" aria-hidden="true"></span>'
                '<div class="orbit-row-copy">'
                f"<span>{safe(task.title)}</span>"
                f"<small>{safe(task.subject_name)} · "
                f"{task.due_date:%d/%m} · "
                f"{safe(task.priority.value)}</small>"
                "</div>"
                "</div>"
            )
            for task in upcoming[:4]
        )
        or '<p class="orbit-empty">Nenhuma tarefa pendente.</p>'
    )

    # ------------------------------------------------------------------
    # TODAY CARD
    # ------------------------------------------------------------------

    task_today_rows = "".join(
        (
            '<div class="orbit-row">'
            '<span class="orbit-time">Hoje</span>'
            '<div class="orbit-row-copy">'
            f"<span>{safe(task.title)}</span>"
            f"<small>{safe(task.subject_name)}</small>"
            "</div>"
            "</div>"
        )
        for task in upcoming
        if task.due_date == today
    )

    event_today_rows = "".join(
        (
            '<div class="orbit-row">'
            f'<span class="orbit-time">{event.starts_at:%H:%M}</span>'
            '<div class="orbit-row-copy">'
            f"<span>{safe(event.title)}</span>"
            f"<small>{safe(event.details or event.category)}</small>"
            "</div>"
            "</div>"
        )
        for event in sorted(
            agenda_events or [],
            key=lambda item: item.starts_at,
        )
        if event.starts_at.date() == today
    )

    today_rows = (
        task_today_rows
        + event_today_rows
    )

    if not today_rows:
        today_rows = (
            '<p class="orbit-empty">'
            "Sem entregas ou eventos para hoje."
            "</p>"
        )

    # ------------------------------------------------------------------
    # WEEKLY GRAPH
    # ------------------------------------------------------------------

    monday = today - timedelta(
        days=today.weekday()
    )

    counts = [
        sum(
            task.due_date
            == monday + timedelta(days=i)
            for task in tasks
        )
        for i in range(7)
    ]

    maximum = max(
        counts,
        default=0,
    )

    bars = "".join(
        (
            '<div class="orbit-bar-column">'
            f'<div class="orbit-bar" style="height:'
            f'{max(3, round(100 * count / maximum)) if maximum else 3}%">'
            "</div>"
            f"<span>{day}</span>"
            "</div>"
        )
        for day, count in zip(
            (
                "Seg",
                "Ter",
                "Qua",
                "Qui",
                "Sex",
                "Sáb",
                "Dom",
            ),
            counts,
        )
    )

    graph = (
        f'<div class="orbit-chart" role="img" '
        f'aria-label="{sum(counts)} entregas nesta semana">'
        f"{bars}"
        "</div>"
        '<div class="orbit-week-total">'
        "Meta semanal "
        f"<strong>{completion}%</strong>"
        "</div>"
    )

    # ------------------------------------------------------------------
    # TIPS
    # ------------------------------------------------------------------

    tips = [
        (
            f"Comece por {safe(focus_task.title)} "
            "e reserve um bloco curto de concentração."
            if focus_task
            else (
                "Cadastre uma tarefa para receber "
                "uma recomendação de prioridade."
            )
        ),
        (
            f"Seu progresso está em {completion}%. "
            "Concluir uma tarefa pequena ajuda a manter o ritmo."
            if tasks
            else (
                "Adicione suas tarefas da semana "
                "para acompanhar o progresso."
            )
        ),
        (
            "Revise as próximas entregas antes de "
            "encerrar o estudo de hoje."
            if upcoming
            else (
                "Sua agenda está livre: aproveite "
                "para planejar a próxima semana."
            )
        ),
    ]

    tip_items = "".join(
        f"<li>{tip}</li>"
        for tip in tips
    )

    # ------------------------------------------------------------------
    # NATIVE CARD CSS
    # ------------------------------------------------------------------

    native_card_css = """
    .st-key-dashboard_card_grid
    [data-testid="stHorizontalBlock"] {
        gap: 12px;
    }

    .st-key-dashboard_card_subjects,
    .st-key-dashboard_card_tasks,
    .st-key-dashboard_card_agenda,
    .st-key-dashboard_card_progress {
        min-height: 340px;
        padding: 18px 12px !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 16px !important;
        background: #fff !important;
        box-shadow: 0 3px 10px rgba(15, 23, 87, .03);
    }

    .st-key-dashboard_card_subjects
    [data-testid="stPageLink"] a,
    .st-key-dashboard_card_tasks
    [data-testid="stPageLink"] a {
        padding: 0 !important;
        min-height: auto !important;
        color: #7c3aed !important;
        background: transparent !important;
        font-size: 10px !important;
        text-decoration: none !important;
        justify-content: flex-end !important;
    }

    .st-key-dashboard_card_subjects
    [data-testid="stPageLink"] a:hover,
    .st-key-dashboard_card_tasks
    [data-testid="stPageLink"] a:hover {
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

    .orbit-native-card-body {
        margin-top: 17px;
    }

    .st-key-dashboard_card_grid {
        padding: 0 24px 16px !important;
        box-sizing: border-box !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .st-key-dashboard_card_subjects,
    .stApp:has(.orbit-dashboard-dark)
    .st-key-dashboard_card_tasks,
    .stApp:has(.orbit-dashboard-dark)
    .st-key-dashboard_card_agenda,
    .stApp:has(.orbit-dashboard-dark)
    .st-key-dashboard_card_progress {
        background: #171a2e !important;
        border-color: #3c4261 !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, .16) !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .orbit-native-card-title {
        color: #f7f5ff !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .orbit-native-card-badge {
        color: #a7aabd !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .orbit-row-copy,
    .stApp:has(.orbit-dashboard-dark)
    .orbit-row-copy span,
    .stApp:has(.orbit-dashboard-dark)
    .orbit-row strong {
        color: #f5f3ff !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .orbit-row-copy small,
    .stApp:has(.orbit-dashboard-dark)
    .orbit-empty,
    .stApp:has(.orbit-dashboard-dark)
    .orbit-time,
    .stApp:has(.orbit-dashboard-dark)
    .orbit-bar-column,
    .stApp:has(.orbit-dashboard-dark)
    .orbit-week-total {
        color: #a7aabd !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .orbit-week-total strong {
        color: #c4b5fd !important;
    }

    .stApp:has(.orbit-dashboard-dark)
    .st-key-dashboard_card_subjects
    [data-testid="stPageLink"] a,
    .stApp:has(.orbit-dashboard-dark)
    .st-key-dashboard_card_tasks
    [data-testid="stPageLink"] a {
        color: #c4b5fd !important;
        background: transparent !important;
    }
    """

    st.markdown(
        _html_block(f"<style>{native_card_css}</style>"),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # CARD ALIGNMENT PATCH
    # ------------------------------------------------------------------

    st.markdown(
        _html_block("""
        <style>
        .st-key-dashboard_card_grid {
            padding: 0 28px 18px !important;
            box-sizing: border-box !important;
        }

        .st-key-dashboard_card_grid > div,
        .st-key-dashboard_card_grid
        [data-testid="stHorizontalBlock"] {
            align-items: stretch !important;
        }

        .st-key-dashboard_card_subjects,
        .st-key-dashboard_card_tasks,
        .st-key-dashboard_card_agenda,
        .st-key-dashboard_card_progress {
            height: 420px !important;
            min-height: 420px !important;
            max-height: 420px !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            border-radius: 18px !important;
            border-color: #d8dee9 !important;
        }

        .st-key-dashboard_card_subjects
        .orbit-native-card-title,
        .st-key-dashboard_card_tasks
        .orbit-native-card-title,
        .st-key-dashboard_card_agenda
        .orbit-native-card-title,
        .st-key-dashboard_card_progress
        .orbit-native-card-title {
            min-height: 62px !important;
            margin: 0 !important;
            display: flex !important;
            align-items: flex-start !important;
            line-height: 1.12 !important;
        }

        .st-key-dashboard_card_subjects
        [data-testid="stHorizontalBlock"]:first-of-type,
        .st-key-dashboard_card_tasks
        [data-testid="stHorizontalBlock"]:first-of-type,
        .st-key-dashboard_card_agenda
        [data-testid="stHorizontalBlock"]:first-of-type,
        .st-key-dashboard_card_progress
        [data-testid="stHorizontalBlock"]:first-of-type {
            min-height: 72px !important;
            height: 72px !important;
            align-items: flex-start !important;
        }

        .st-key-dashboard_card_subjects
        [data-testid="stPageLink"] a,
        .st-key-dashboard_card_tasks
        [data-testid="stPageLink"] a {
            min-height: 28px !important;
            padding-top: 4px !important;
            align-items: flex-start !important;
            justify-content: flex-end !important;
        }

        .st-key-dashboard_card_agenda
        .orbit-native-card-badge,
        .st-key-dashboard_card_progress
        .orbit-native-card-badge {
            margin: 4px 0 0 !important;
            line-height: 20px !important;
        }

        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_subjects,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_tasks,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_agenda,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_progress {
            border: 1px solid rgba(255, 255, 255, .72) !important;
            background: #171a2e !important;
            box-shadow: 0 5px 18px rgba(0, 0, 0, .18) !important;
        }

        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_subjects
        .orbit-native-card-title,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_tasks
        .orbit-native-card-title,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_agenda
        .orbit-native-card-title,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_progress
        .orbit-native-card-title {
            color: #ffffff !important;
        }

        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_subjects
        [data-testid="stPageLink"] a,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_tasks
        [data-testid="stPageLink"] a {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_agenda
        .orbit-native-card-badge,
        .stApp:has(.orbit-dashboard-dark)
        .st-key-dashboard_card_progress
        .orbit-native-card-badge {
            color: #cdd2e5 !important;
        }

        .st-key-dashboard_card_subjects
        .orbit-native-card-body,
        .st-key-dashboard_card_tasks
        .orbit-native-card-body,
        .st-key-dashboard_card_agenda
        .orbit-native-card-body,
        .st-key-dashboard_card_progress
        .orbit-native-card-body {
            overflow: hidden !important;
        }

        @media (max-width: 1200px) {
            .st-key-dashboard_card_subjects,
            .st-key-dashboard_card_tasks,
            .st-key-dashboard_card_agenda,
            .st-key-dashboard_card_progress {
                height: auto !important;
                min-height: 360px !important;
                max-height: none !important;
            }
        }
        </style>
        """),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # HERO
    # ------------------------------------------------------------------

    st.markdown(
        _html_block(f"""
        <div
            class="orbit-dashboard{theme_class}"
            aria-label="Início do estudante"
        >
            <div class="orbit-content">
                <section class="orbit-hero">

                    <div class="orbit-hero-intro">
                        <span class="orbit-eyebrow">
                            ✦ VISÃO GERAL
                        </span>

                        <h2>
                            Seu percurso<br>
                            <em>acadêmico,</em><br>
                            impulsionado por IA.
                        </h2>

                        <p>
                            Insights inteligentes para decisões
                            melhores todos os dias.
                        </p>
                    </div>

                    <div class="orbit-pet">
                        {pet_html}

                        <div class="orbit-bubble">
                            <strong>{completion}%</strong>
                            <small>das tarefas</small>
                        </div>
                    </div>

                    <div class="orbit-metrics">
                        <div>
                            <span>Progresso semanal</span>
                            <strong>{completion}% das tarefas</strong>
                        </div>

                        <div>
                            <span>Próxima entrega</span>
                            <strong>{next_delivery}</strong>
                        </div>

                        <div>
                            <span>Foco recomendado</span>
                            <strong>{focus}</strong>
                        </div>
                    </div>

                </section>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # DASHBOARD CARDS
    # ------------------------------------------------------------------

    with st.container(
        key="dashboard_card_grid"
    ):
        (
            subject_col,
            task_col,
            agenda_col,
            progress_col,
        ) = st.columns(
            4,
            gap="small",
        )

        # --------------------------------------------------------------
        # SUBJECTS
        # --------------------------------------------------------------

        with subject_col:
            with st.container(
                key="dashboard_card_subjects"
            ):
                title_col, link_col = st.columns(
                    [3, 1],
                    vertical_alignment="center",
                )

                with title_col:
                    st.markdown(
                        (
                            _html_block('<h2 class="orbit-native-card-title">'
                            "Minhas disciplinas"
                            "</h2>")
                        ),
                        unsafe_allow_html=True,
                    )

                with link_col:
                    st.page_link(
                        "pages/2_Disciplinas.py",
                        label="Ver todas",
                    )

                st.markdown(
                    (
                        _html_block('<div class="orbit-native-card-body">'
                        f"{subject_rows}"
                        "</div>")
                    ),
                    unsafe_allow_html=True,
                )

        # --------------------------------------------------------------
        # TASKS
        # --------------------------------------------------------------

        with task_col:
            with st.container(
                key="dashboard_card_tasks"
            ):
                title_col, link_col = st.columns(
                    [3, 1],
                    vertical_alignment="center",
                )

                with title_col:
                    st.markdown(
                        (
                            _html_block('<h2 class="orbit-native-card-title">'
                            "Tarefas prioritárias"
                            "</h2>")
                        ),
                        unsafe_allow_html=True,
                    )

                with link_col:
                    st.page_link(
                        "pages/3_Tarefas.py",
                        label="Ver todas",
                    )

                st.markdown(
                    (
                        _html_block('<div class="orbit-native-card-body">'
                        f"{task_rows}"
                        "</div>")
                    ),
                    unsafe_allow_html=True,
                )

        # --------------------------------------------------------------
        # AGENDA
        # --------------------------------------------------------------

        with agenda_col:
            with st.container(
                key="dashboard_card_agenda"
            ):
                title_col, badge_col = st.columns(
                    [3, 1],
                    vertical_alignment="center",
                )

                with title_col:
                    st.markdown(
                        (
                            _html_block('<h2 class="orbit-native-card-title">'
                            "Agenda de hoje"
                            "</h2>")
                        ),
                        unsafe_allow_html=True,
                    )

                with badge_col:
                    st.markdown(
                        (
                            _html_block('<p class="orbit-native-card-badge">'
                            f"{today:%d/%m}"
                            "</p>")
                        ),
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    (
                        _html_block('<div class="orbit-native-card-body">'
                        f"{today_rows}"
                        "</div>")
                    ),
                    unsafe_allow_html=True,
                )

        # --------------------------------------------------------------
        # PROGRESS
        # --------------------------------------------------------------

        with progress_col:
            with st.container(
                key="dashboard_card_progress"
            ):
                title_col, badge_col = st.columns(
                    [3, 1],
                    vertical_alignment="center",
                )

                with title_col:
                    st.markdown(
                        (
                            _html_block('<h2 class="orbit-native-card-title">'
                            "Progresso semanal"
                            "</h2>")
                        ),
                        unsafe_allow_html=True,
                    )

                with badge_col:
                    st.markdown(
                        (
                            _html_block('<p class="orbit-native-card-badge">'
                            "Esta semana"
                            "</p>")
                        ),
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    (
                        _html_block('<div class="orbit-native-card-body">'
                        f"{graph}"
                        "</div>")
                    ),
                    unsafe_allow_html=True,
                )

    # ------------------------------------------------------------------
    # TIP OF THE DAY
    # ------------------------------------------------------------------

    st.markdown(
        _html_block(f"""
        <div class="orbit-dashboard{theme_class}">
            <div class="orbit-content">

                <div class="orbit-tip">
                    {icon("tip", "Dica do dia")}

                    <div class="orbit-tip-copy">
                        <strong>Dica do dia</strong>
                        <span>
                            Pequenos avanços diários geram
                            grandes conquistas.
                        </span>
                    </div>

                    <details class="orbit-tips">
                        <summary>Ver dicas</summary>

                        <div class="orbit-tip-panel">
                            <strong>
                                Recomendações para você
                            </strong>

                            <ul>
                                {tip_items}
                            </ul>
                        </div>
                    </details>
                </div>

            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )
