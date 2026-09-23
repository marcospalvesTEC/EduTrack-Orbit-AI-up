"""Tests for the Figma-aligned desktop Orbit assistant."""

from datetime import date, timedelta
from pathlib import Path

from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.services.demo_auth import DEMO_EMAIL
from src.ui.figma_assistant import (
    assistant_reply,
    conversation_key,
    pending_action_key,
)
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _data():
    subject = Subject("Banco de Dados", "BD", "Prof.", 60, id="sub-1")
    tasks = [
        Task(
            "Consultas SQL",
            subject.id,
            subject.name,
            date.today() - timedelta(days=1),
            TaskStatus.ATRASADA,
        )
    ]
    return [subject], tasks


def _authenticated_app() -> AppTest:
    app = AppTest.from_file(PROJECT_ROOT / "pages/6_Assistente.py", default_timeout=15)
    app.session_state["auth_current_user"] = {
        "name": "Estudante Demo",
        "email": DEMO_EMAIL,
    }
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    return app.run()


def test_assistant_keys_are_scoped_to_the_authenticated_user():
    user = {"email": "Aluno@Example.com"}

    assert conversation_key(user) == "assistant_messages:aluno@example.com"
    assert pending_action_key(user) == "assistant_pending:aluno@example.com"


def test_assistant_replies_use_academic_data_and_preview_writes():
    subjects, tasks = _data()

    overdue_answer, overdue_action = assistant_reply("Ver tarefas atrasadas", subjects, tasks)
    focus_answer, focus_action = assistant_reply("Criar sessão de foco", subjects, tasks)

    assert "Consultas SQL" in overdue_answer
    assert overdue_action is None
    assert "confirme" in focus_answer.lower()
    assert focus_action == {"type": "focus", "subject": "Banco de Dados", "duration": "45"}


def test_assistant_css_contains_light_dark_and_desktop_rules():
    css = (PROJECT_ROOT / "src/ui/figma_assistant.css").read_text(encoding="utf-8")

    assert ".orbit-assistant-dark" in css
    assert "background: #7c3aed !important" in css
    assert "border-color: #f5f3ff !important" in css
    assert "@media" not in css


def test_assistant_page_renders_and_confirms_focus_event():
    app = _authenticated_app()

    assert not app.exception
    assert any("Assistente <em>Orbit</em>" in item.value for item in app.markdown)
    assert any(button.label == "Criar sessão de foco" for button in app.button)
    assert len(app.text_input) == 1

    next(button for button in app.button if button.label == "Criar sessão de foco").click().run()
    assert not app.exception
    assert any(button.label == "Confirmar" for button in app.button)
    assert f"agenda_events:{DEMO_EMAIL}" not in app.session_state

    next(button for button in app.button if button.label == "Confirmar").click().run()
    assert not app.exception
    events = app.session_state[f"agenda_events:{DEMO_EMAIL}"]
    assert len(events) == 1
    assert events[0]["category"] == "Sessão de foco"
    assert events[0]["title"].startswith("Sessão de foco")
