"""Figma-aligned agenda views built from academic tasks and personal events."""

from __future__ import annotations

import calendar
import uuid
from dataclasses import dataclass, replace
from datetime import date, datetime, time, timedelta
from html import escape
from pathlib import Path

import streamlit as st

from src.models.task import Task
from src.ui.figma_dashboard import icon

MONTHS = (
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)
WEEKDAYS = ("SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM")
CATEGORY_COLORS = {
    "Aula": "purple",
    "Entrega": "pink",
    "Sessão de foco": "orange",
    "Trabalho em grupo": "green",
}


def safe(value: object) -> str:
    """Escape user-controlled values before including them in HTML."""
    return escape(str(value), quote=True)


@dataclass(frozen=True)
class AgendaEvent:
    """Small presentation model for one calendar event."""

    title: str
    starts_at: datetime
    category: str = "Aula"
    details: str = ""
    id: str = ""
    source_task_id: str | None = None

    def __post_init__(self) -> None:
        if not self.id:
            object.__setattr__(self, "id", str(uuid.uuid4()))

    def to_dict(self) -> dict[str, str | None]:
        """Serialize an event for Streamlit session state."""
        return {
            "id": self.id,
            "title": self.title,
            "starts_at": self.starts_at.isoformat(),
            "category": self.category,
            "details": self.details,
            "source_task_id": self.source_task_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> AgendaEvent:
        """Restore an event stored in Streamlit session state."""
        raw_start = value["starts_at"]
        return cls(
            id=str(value.get("id", "")),
            title=str(value["title"]),
            starts_at=datetime.fromisoformat(str(raw_start)),
            category=str(value.get("category", "Aula")),
            details=str(value.get("details", "")),
            source_task_id=(str(value["source_task_id"]) if value.get("source_task_id") else None),
        )


def add_months(value: date, offset: int) -> date:
    """Return the first day of the month at ``offset`` from ``value``."""
    absolute_month = value.year * 12 + value.month - 1 + offset
    year, month_index = divmod(absolute_month, 12)
    return date(year, month_index + 1, 1)


def task_events(tasks: list[Task]) -> list[AgendaEvent]:
    """Convert task deadlines into read-only agenda events."""
    return [
        AgendaEvent(
            id=f"task:{task.id}",
            title=task.title,
            starts_at=datetime.combine(task.due_date, time(18)),
            category="Entrega",
            details=task.subject_name,
            source_task_id=task.id,
        )
        for task in tasks
    ]


def demo_events(reference: date) -> list[AgendaEvent]:
    """Create the Figma example rhythm around the current week."""
    monday = reference - timedelta(days=reference.weekday())
    examples = (
        (0, 8, "Projeto de BD", "Aula", "Sala 204"),
        (1, 18, "Exercícios SQL", "Sessão de foco", "60 min"),
        (1, 21, "Grupo de estudos", "Trabalho em grupo", "Online"),
        (2, 10, "Inteligência Artificial", "Aula", "Sala 102"),
        (3, 14, "Revisar SQL", "Sessão de foco", "60 min"),
        (4, 8, "Engenharia de Software", "Aula", "Sala 204 · Bloco B"),
        (5, 10, "Sessão de foco", "Sessão de foco", "Revisão semanal"),
        (5, 19, "Preparar apresentação", "Trabalho em grupo", "Engenharia de Software"),
    )
    return [
        AgendaEvent(
            id=f"demo:{day}:{hour}:{title}",
            title=title,
            starts_at=datetime.combine(monday + timedelta(days=day), time(hour)),
            category=category,
            details=details,
        )
        for day, hour, title, category, details in examples
    ]


def events_for_month(events: list[AgendaEvent], month: date) -> list[AgendaEvent]:
    """Filter events to the selected month and sort chronologically."""
    return sorted(
        (
            event
            for event in events
            if event.starts_at.year == month.year and event.starts_at.month == month.month
        ),
        key=lambda event: event.starts_at,
    )


def upcoming_events(
    events: list[AgendaEvent], reference: datetime, limit: int = 5
) -> list[AgendaEvent]:
    """Return the next visible events, excluding already elapsed items."""
    return sorted(
        (event for event in events if event.starts_at >= reference),
        key=lambda event: event.starts_at,
    )[:limit]


def events_on_day(events: list[AgendaEvent], selected_day: date) -> list[AgendaEvent]:
    """Return every event scheduled for one day in chronological order."""
    return sorted(
        (event for event in events if event.starts_at.date() == selected_day),
        key=lambda event: event.starts_at,
    )


def event_store_key(user: dict[str, str]) -> str:
    """Return the user-scoped session key for custom events."""
    return f"agenda_events:{user['email'].strip().lower()}"


def load_custom_events(user: dict[str, str]) -> list[AgendaEvent]:
    """Load personal events from Streamlit session state."""
    raw_events = st.session_state.setdefault(event_store_key(user), [])
    return [AgendaEvent.from_dict(item) for item in raw_events]


def save_custom_event(user: dict[str, str], event: AgendaEvent) -> None:
    """Append one personal event to Streamlit session state."""
    key = event_store_key(user)
    current = list(st.session_state.setdefault(key, []))
    current.append(event.to_dict())
    st.session_state[key] = current


def render_agenda_header(user: dict[str, str]) -> None:
    """Install Agenda CSS and render the official desktop top bar."""
    css = (Path(__file__).parent / "figma_agenda.css").read_text(encoding="utf-8")
    first_name = safe(user.get("name", "Estudante").split()[0])
    theme_class = " orbit-agenda-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="orbit-agenda-page{theme_class}" aria-label="Agenda do estudante">
  <header class="orbit-agenda-topbar"><div><h1>Boa noite, {first_name}</h1>
    <p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-agenda-header-icons"><span class="orbit-agenda-global-search">
      {icon("search", "")} Buscar...</span>
      <span class="orbit-agenda-bell">{icon("bell", "Notificações")}</span></div>
  </header>
</div>
""",
        unsafe_allow_html=True,
    )


def render_agenda_dialog_theme_marker() -> None:
    """Expose dark mode inside Streamlit's portal-based dialog."""
    if st.session_state.get("edutrack_dark_mode"):
        st.markdown(
            '<span class="orbit-agenda-dialog-dark" aria-hidden="true"></span>',
            unsafe_allow_html=True,
        )


def _event_pill(event: AgendaEvent) -> str:
    color = CATEGORY_COLORS.get(event.category, "purple")
    return (
        f'<span class="orbit-agenda-event event-{color}" title="{safe(event.details)}">'
        f"{safe(event.title)}</span>"
    )


def render_month_calendar(events: list[AgendaEvent], selected_month: date) -> date | None:
    """Render the monthly calendar and return the day clicked by the user."""
    grouped: dict[date, list[AgendaEvent]] = {}
    for event in events:
        grouped.setdefault(event.starts_at.date(), []).append(event)
    weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(
        selected_month.year, selected_month.month
    )
    if len(weeks) < 6:
        next_week = [day + timedelta(days=7) for day in weeks[-1]]
        weeks.append(next_week)

    selected_day = None
    today = date.today()
    with st.container(border=True, key="agenda_calendar_grid"):
        headers = "".join(f"<div>{day}</div>" for day in WEEKDAYS)
        st.markdown(
            f'<div class="orbit-agenda-weekdays">{headers}</div>',
            unsafe_allow_html=True,
        )
        for week in weeks:
            columns = st.columns(7, gap="small")
            for column, day in zip(columns, week, strict=True):
                with column:
                    cell_key = f"agenda_day_cell_{day:%Y%m%d}"
                    with st.container(border=True, key=cell_key):
                        classes = ["orbit-agenda-day-content"]
                        if day.month != selected_month.month:
                            classes.append("outside")
                        if day == today:
                            classes.append("today")
                        day_events = grouped.get(day, [])
                        pills = "".join(_event_pill(event) for event in day_events[:2])
                        overflow = len(day_events) - 2
                        overflow_label = ""
                        if overflow > 0:
                            event_label = "evento" if overflow == 1 else "eventos"
                            overflow_label = (
                                f'<small class="orbit-agenda-more">'
                                f"(+{overflow} {event_label})</small>"
                            )
                        st.markdown(
                            f'<div class="{" ".join(classes)}">'
                            f"<header><strong>{day.day}</strong>{overflow_label}</header>"
                            f"{pills}</div>",
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"Abrir agenda de {day:%d/%m/%Y}",
                            key=f"open_agenda_day_{day:%Y%m%d}",
                            use_container_width=True,
                        ):
                            selected_day = day
    return selected_day


def _day_label(value: date) -> str:
    return f"{WEEKDAYS[value.weekday()]} {value.day}"


def render_detailed_week(events: list[AgendaEvent], reference: date) -> tuple[date | None, bool]:
    """Render the detailed week and return its selected day or group-work card."""
    monday = reference - timedelta(days=reference.weekday())
    days = [monday + timedelta(days=offset) for offset in range(7)]
    event_map: dict[date, list[AgendaEvent]] = {}
    for event in events:
        event_map.setdefault(event.starts_at.date(), []).append(event)

    mini_days = " ".join(str(day.day) for day in days)
    filters = "".join(
        f'<span><i class="event-{color}"></i>{safe(category)}s</span>'
        for category, color in CATEGORY_COLORS.items()
    )
    selected_day = None
    today = date.today()
    mini_column, week_column = st.columns([1, 5], gap="small")
    with mini_column:
        st.markdown(
            '<aside class="orbit-agenda-mini"><strong>'
            f"{MONTHS[reference.month - 1].upper()} {reference.year}</strong>"
            f"<p>{' '.join(WEEKDAYS)}</p><p>{mini_days}</p>"
            f"<h3>MINHA AGENDA</h3><div>{filters}</div></aside>",
            unsafe_allow_html=True,
        )
    with week_column:
        day_columns = st.columns(7, gap="small")
        for column, day in zip(day_columns, days, strict=True):
            with column:
                day_key = f"agenda_week_day_{day:%Y%m%d}"
                with st.container(border=True, key=day_key):
                    sorted_events = sorted(event_map.get(day, []), key=lambda item: item.starts_at)
                    entries = "".join(
                        "<article>"
                        f"<time>{event.starts_at:%H:%M}</time>"
                        f"<strong>{safe(event.title)}</strong>"
                        f"<small>{safe(event.details)}</small>"
                        "</article>"
                        for event in sorted_events
                    )
                    empty = '<p class="orbit-agenda-empty">Sem eventos</p>' if not entries else ""
                    current = " current" if day == today else ""
                    st.markdown(
                        f'<div class="orbit-agenda-week-day-content{current}">'
                        f"<h3>{_day_label(day)}</h3>{entries}{empty}</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        f"Abrir agenda de {day:%d/%m/%Y}",
                        key=f"open_agenda_week_day_{day:%Y%m%d}",
                        use_container_width=True,
                    ):
                        selected_day = day
        group_events = sorted(
            (event for event in events if event.category == "Trabalho em grupo"),
            key=lambda item: item.starts_at,
        )
        first_group = group_events[0] if group_events else None
        group_summary = (
            f"<span>{safe(first_group.title)}</span>"
            f"<small>{first_group.starts_at:%d/%m às %H:%M} · "
            f"{safe(first_group.details or 'Sem observações')}</small>"
            if first_group
            else "<span>Nenhum trabalho em grupo agendado</span>"
        )
        extra_groups = len(group_events) - 1
        if extra_groups > 0:
            label = "trabalho" if extra_groups == 1 else "trabalhos"
            group_summary += f"<small>(+{extra_groups} {label})</small>"
        with st.container(key="agenda_group_footer"):
            st.markdown(
                '<div class="orbit-agenda-group-footer"><strong>TRABALHO EM GRUPO</strong>'
                f"{group_summary}</div>",
                unsafe_allow_html=True,
            )
            group_clicked = st.button(
                "Abrir trabalhos em grupo",
                key="open_agenda_group_work",
                use_container_width=True,
            )
    return selected_day, group_clicked


def render_upcoming_panel(events: list[AgendaEvent], reference: datetime) -> None:
    """Render the upcoming-event card from the monthly Figma view."""
    upcoming = upcoming_events(events, reference)
    rows: list[str] = []
    previous_label = ""
    for event in upcoming:
        event_date = event.starts_at.date()
        if event_date == reference.date():
            label = "HOJE"
        elif event_date == reference.date() + timedelta(days=1):
            label = "AMANHÃ"
        else:
            label = event_date.strftime("%d/%m")
        heading = f"<h3>{label}</h3>" if label != previous_label else ""
        previous_label = label
        color = CATEGORY_COLORS.get(event.category, "purple")
        rows.append(
            f'{heading}<article><i class="event-{color}"></i>'
            f"<time>{event.starts_at:%H:%M}</time><div><strong>{safe(event.title)}</strong>"
            f"<small>{safe(event.details or event.category)}</small></div></article>"
        )
    if not rows:
        rows.append('<p class="orbit-agenda-upcoming-empty">Nenhum evento futuro.</p>')
    st.markdown(
        f'<aside class="orbit-agenda-upcoming"><h2>Próximos eventos</h2>{"".join(rows)}</aside>',
        unsafe_allow_html=True,
    )


def move_event(event: AgendaEvent, new_start: datetime) -> AgendaEvent:
    """Return a copy with a new start; useful to keep immutable event values."""
    return replace(event, starts_at=new_start)
