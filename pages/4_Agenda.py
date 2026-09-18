"""Academic agenda aligned with the approved Figma desktop frames."""

from datetime import date, datetime

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.services.data_service import data_service_for_user, load_academic_data
from src.ui.figma_agenda import (
    CATEGORY_COLORS,
    MONTHS,
    AgendaEvent,
    add_months,
    demo_events,
    events_for_month,
    events_on_day,
    load_custom_events,
    render_agenda_dialog_theme_marker,
    render_agenda_header,
    render_detailed_week,
    render_month_calendar,
    render_upcoming_panel,
    safe,
    save_custom_event,
    task_events,
)
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Agenda - EduTrack Orbit AI", page_icon="📅", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)
service = data_service_for_user(user)
_, tasks = load_academic_data(service)
dialog = st.dialog if hasattr(st, "dialog") else st.experimental_dialog


@dialog("Novo evento", width="large")
def render_new_event_dialog() -> None:
    """Create a personal event in the current user's agenda."""
    render_agenda_dialog_theme_marker()
    with st.form("agenda_new_event", clear_on_submit=True):
        title = st.text_input("Título do evento", placeholder="Ex.: Grupo de estudos")
        first, second = st.columns(2)
        with first:
            event_date = st.date_input("Data", value=date.today())
            event_time = st.time_input(
                "Horário", value=datetime.now().time().replace(second=0, microsecond=0)
            )
        with second:
            category = st.selectbox("Categoria", tuple(CATEGORY_COLORS))
            details = st.text_input("Local ou observação", placeholder="Ex.: Sala 204 · Bloco B")
        submitted = st.form_submit_button("Cadastrar evento", type="primary", width="stretch")
    if submitted:
        if not title.strip():
            st.error("Informe o título do evento.")
            return
        save_custom_event(
            user,
            AgendaEvent(
                title=title.strip(),
                starts_at=datetime.combine(event_date, event_time),
                category=category,
                details=details.strip(),
            ),
        )
        st.success("Evento adicionado à agenda.")
        st.rerun()


def render_day_drawer(selected_day: date, day_events: list[AgendaEvent]) -> None:
    """Show the selected day in a compact, non-blocking side drawer."""
    with st.container(key="agenda_day_drawer"):
        heading, close = st.columns([5, 1], vertical_alignment="center")
        with heading:
            st.markdown("<h2>Agenda do dia</h2>", unsafe_allow_html=True)
        with close:
            if st.button("×", key="close_agenda_day_drawer", help="Fechar painel"):
                st.session_state["agenda_drawer_kind"] = None
                st.rerun()
        st.markdown(
            f'<div class="orbit-agenda-dialog-date"><strong>{selected_day:%d/%m/%Y}</strong>'
            f"<span>{len(day_events)} evento(s)</span></div>",
            unsafe_allow_html=True,
        )
        if not day_events:
            st.info("Nenhum evento cadastrado para este dia.")
            return
        for event in day_events:
            color = CATEGORY_COLORS.get(event.category, "purple")
            st.markdown(
                f'<article class="orbit-agenda-dialog-event event-{color}">'
                f"<time>{event.starts_at:%H:%M}</time><div><strong>{safe(event.title)}</strong>"
                f"<span>{safe(event.category)}</span>"
                f"<p>{safe(event.details or 'Sem observações adicionais.')}</p>"
                "</div></article>",
                unsafe_allow_html=True,
            )


def render_group_drawer(group_events: list[AgendaEvent]) -> None:
    """Show every group-work event in the same right-side drawer."""
    with st.container(key="agenda_day_drawer"):
        heading, close = st.columns([5, 1], vertical_alignment="center")
        with heading:
            st.markdown("<h2>Trabalhos em grupo</h2>", unsafe_allow_html=True)
        with close:
            if st.button("×", key="close_agenda_group_drawer", help="Fechar painel"):
                st.session_state["agenda_drawer_kind"] = None
                st.rerun()
        st.markdown(
            f'<div class="orbit-agenda-dialog-date"><strong>Minha agenda</strong>'
            f"<span>{len(group_events)} trabalho(s)</span></div>",
            unsafe_allow_html=True,
        )
        if not group_events:
            st.info("Nenhum trabalho em grupo agendado.")
            return
        for event in group_events:
            st.markdown(
                '<article class="orbit-agenda-dialog-event event-green">'
                f"<time>{event.starts_at:%d/%m}<br>{event.starts_at:%H:%M}</time>"
                f"<div><strong>{safe(event.title)}</strong>"
                f"<span>{safe(event.category)}</span>"
                f"<p>{safe(event.details or 'Sem observações adicionais.')}</p>"
                "</div></article>",
                unsafe_allow_html=True,
            )


render_agenda_header(user)
intro, action = st.columns([5, 1])
with intro:
    st.markdown(
        '<div class="orbit-agenda-intro"><h1>Agenda</h1>'
        "<p>Visualize aulas, entregas e sessões de estudo em um só lugar.</p></div>",
        unsafe_allow_html=True,
    )
with action:
    if st.button("+ Novo evento", key="new_agenda_event", use_container_width=True):
        render_new_event_dialog()

st.session_state.setdefault("agenda_month", date.today().replace(day=1))
selected_month = st.session_state["agenda_month"]
previous, month_title, following, spacer, view_switcher = st.columns([0.35, 1.7, 0.35, 3, 2.3])
with previous:
    if st.button("‹", key="agenda_previous_month", help="Mês anterior", width="stretch"):
        st.session_state["agenda_month"] = add_months(selected_month, -1)
        st.rerun()
with month_title:
    st.markdown(
        f'<div class="orbit-agenda-month-title">{MONTHS[selected_month.month - 1]} de {selected_month.year}</div>',
        unsafe_allow_html=True,
    )
with following:
    if st.button("›", key="agenda_next_month", help="Próximo mês", width="stretch"):
        st.session_state["agenda_month"] = add_months(selected_month, 1)
        st.rerun()
with view_switcher:
    view = st.radio(
        "Visualização",
        ("Calendário", "Semana detalhada"),
        horizontal=True,
        label_visibility="collapsed",
    )

all_events = task_events(tasks) + load_custom_events(user)
if user.get("email", "").endswith("@edutrack.ai"):
    all_events += demo_events(date.today())

st.session_state.setdefault("agenda_selected_day", None)
st.session_state.setdefault("agenda_drawer_kind", None)
selected_day = None
group_clicked = False
if view == "Semana detalhada":
    selected_day, group_clicked = render_detailed_week(all_events, date.today())
else:
    calendar_column, upcoming_column = st.columns([3.4, 1])
    with calendar_column:
        selected_day = render_month_calendar(
            events_for_month(all_events, selected_month), selected_month
        )
    with upcoming_column:
        render_upcoming_panel(all_events, datetime.now().replace(second=0, microsecond=0))

if selected_day is not None:
    st.session_state["agenda_selected_day"] = selected_day
    st.session_state["agenda_drawer_kind"] = "day"
if group_clicked:
    st.session_state["agenda_drawer_kind"] = "group"

drawer_kind = st.session_state.get("agenda_drawer_kind")
drawer_day = st.session_state.get("agenda_selected_day")
if drawer_kind == "day" and drawer_day is not None:
    render_day_drawer(drawer_day, events_on_day(all_events, drawer_day))
elif drawer_kind == "group":
    group_events = sorted(
        (event for event in all_events if event.category == "Trabalho em grupo"),
        key=lambda event: event.starts_at,
    )
    render_group_drawer(group_events)
