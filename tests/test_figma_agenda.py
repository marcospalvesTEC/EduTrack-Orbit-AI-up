"""Tests for the Figma-aligned Agenda helpers."""

from datetime import date, datetime
from pathlib import Path

from src.models.task import Task
from src.ui.figma_agenda import (
    AgendaEvent,
    add_months,
    events_for_month,
    events_on_day,
    task_events,
    upcoming_events,
)


def event(title: str, starts_at: datetime) -> AgendaEvent:
    return AgendaEvent(id=title, title=title, starts_at=starts_at)


def test_add_months_handles_year_boundaries():
    assert add_months(date(2026, 1, 18), -1) == date(2025, 12, 1)
    assert add_months(date(2026, 12, 18), 1) == date(2027, 1, 1)


def test_task_events_become_delivery_deadlines():
    task = Task(
        id="task-1",
        title="Projeto final",
        subject_id="subject-1",
        subject_name="Engenharia de Software",
        due_date=date(2026, 9, 22),
    )

    result = task_events([task])

    assert result[0].title == "Projeto final"
    assert result[0].category == "Entrega"
    assert result[0].starts_at == datetime(2026, 9, 22, 18)
    assert result[0].source_task_id == "task-1"


def test_month_and_upcoming_filters_are_chronological():
    september = event("Setembro", datetime(2026, 9, 20, 19))
    october = event("Outubro", datetime(2026, 10, 1, 8))
    earlier = event("Mais cedo", datetime(2026, 9, 18, 10))
    values = [october, september, earlier]

    assert events_for_month(values, date(2026, 9, 1)) == [earlier, september]
    assert events_on_day(values, date(2026, 9, 20)) == [september]
    assert upcoming_events(values, datetime(2026, 9, 19)) == [september, october]


def test_event_round_trip_preserves_values():
    original = AgendaEvent(
        id="event-1",
        title="Grupo de estudos",
        starts_at=datetime(2026, 9, 19, 21),
        category="Trabalho em grupo",
        details="Online",
    )

    assert AgendaEvent.from_dict(original.to_dict()) == original


def test_calendar_cards_keep_full_click_targets_and_right_drawer():
    css = (Path(__file__).parents[1] / "src/ui/figma_agenda.css").read_text(encoding="utf-8")

    assert 'class*="st-key-open_agenda_day_"' in css
    assert 'class*="st-key-open_agenda_week_day_"' in css
    assert ".st-key-open_agenda_group_work" in css
    assert "position: absolute !important; inset: 0 !important" in css
    assert "transform: translateX(100%)" in css
