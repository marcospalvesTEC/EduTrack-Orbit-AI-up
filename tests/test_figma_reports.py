"""Tests for the Figma-aligned desktop reports screen."""

from datetime import date
from pathlib import Path

from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.services.demo_auth import DEMO_EMAIL
from src.ui.figma_reports import (
    build_report_pdf,
    report_insight,
    report_metrics,
    task_distribution,
)
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _data():
    subject = Subject(
        id="sub-1",
        name="Banco de Dados",
        code="BD",
        professor="Prof.",
        workload_hours=60,
        color_hex="#7C3AED",
    )
    tasks = [
        Task("Modelo ER", subject.id, subject.name, date.today(), TaskStatus.CONCLUIDA),
        Task("Consultas", subject.id, subject.name, date.today(), TaskStatus.EM_ANDAMENTO),
    ]
    return [subject], tasks


def test_report_helpers_use_real_academic_data():
    subjects, tasks = _data()

    assert report_metrics(tasks, subjects, 12) == {
        "semester_progress": 50,
        "completed_tasks": 1,
        "study_hours": 12,
        "weekly_average": 50,
    }
    assert task_distribution(tasks) == {"completed": 1, "in_progress": 1, "to_do": 0}
    assert "Banco de Dados" in report_insight(subjects, tasks)


def test_report_pdf_is_generated_as_a_real_pdf():
    subjects, tasks = _data()
    metrics = report_metrics(tasks, subjects, 12)
    pdf = build_report_pdf({"name": "Estudante Teste"}, subjects, tasks, metrics)

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000


def test_reports_css_contains_both_desktop_themes_and_purple_actions():
    css = (PROJECT_ROOT / "src/ui/figma_reports.css").read_text(encoding="utf-8")

    assert ".orbit-reports-dark" in css
    assert "background: #7c3aed !important" in css
    assert "border-color: #374151 !important" in css
    assert "@media" not in css


def test_reports_page_renders_filters_export_and_plan_action():
    app = AppTest.from_file(PROJECT_ROOT / "pages/5_Relatorios.py", default_timeout=15)
    app.session_state["auth_current_user"] = {
        "name": "Estudante Demo",
        "email": DEMO_EMAIL,
    }
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    app.run()

    assert not app.exception
    assert len(app.selectbox) == 2
    assert app.selectbox[0].value == "Semestre atual"
    assert app.selectbox[1].value == "Todas as disciplinas"
    assert any(button.label == "Exportar PDF" for button in app.get("download_button"))
    assert any(button.label == "Ver plano recomendado" for button in app.button)
