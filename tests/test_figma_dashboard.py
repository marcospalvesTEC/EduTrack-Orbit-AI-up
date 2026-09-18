"""Dashboard HTML keeps Figma hierarchy without inventing academic data."""

from datetime import date, timedelta

from src.models.subject import Subject
from src.models.task import Task
from src.ui import figma_dashboard


def test_dashboard_escapes_user_and_subject_data(monkeypatch):
    rendered = []
    monkeypatch.setattr(figma_dashboard.st, "markdown", lambda html, **_: rendered.append(html))
    monkeypatch.setattr(figma_dashboard.st, "session_state", {"edutrack_dark_mode": False})
    subject = Subject(name="<Banco & Dados>", code="BD", professor="Prof. <A>", workload_hours=40)
    metrics = {"completion_rate": 0.0}

    figma_dashboard.render_dashboard({"name": "Marcos<script>"}, [subject], [], metrics)

    html = rendered[-1]
    assert "Marcos&lt;script&gt;" in html
    assert "&lt;Banco &amp; Dados&gt;" in html
    assert "<Banco & Dados>" not in html
    assert "Sem entregas para hoje." in html
    assert "Ver dicas" in html
    assert "Cadastre uma tarefa para receber uma recomendação de prioridade." in html


def test_dashboard_shows_actual_deadline_and_dark_theme(monkeypatch):
    rendered = []
    monkeypatch.setattr(figma_dashboard.st, "markdown", lambda html, **_: rendered.append(html))
    monkeypatch.setattr(figma_dashboard.st, "session_state", {"edutrack_dark_mode": True})
    subject = Subject(name="Banco de Dados", code="BD", professor="Prof. Ana", workload_hours=40)
    due = date.today() + timedelta(days=2)
    task = Task(title="Revisar SQL", subject_id=subject.id, subject_name=subject.name, due_date=due)

    figma_dashboard.render_dashboard({"name": "Marcos"}, [subject], [task], {"completion_rate": 0})

    html = rendered[-1]
    assert "orbit-dashboard-dark" in html
    assert "Revisar SQL" in html
    assert due.strftime("%d/%m") in html
    assert "Marcos Silva" not in html
    assert "Comece por Revisar SQL" in html
