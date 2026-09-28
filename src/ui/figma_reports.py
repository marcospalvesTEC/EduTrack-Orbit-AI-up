"""Figma-aligned helpers for the desktop academic reports screen."""

from __future__ import annotations

from collections import Counter
from datetime import date
from html import escape
from io import BytesIO
from pathlib import Path

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.core.metrics import calculate_dashboard_metrics, calculate_subject_progress
from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.ui.figma_dashboard import icon


def safe(value: object) -> str:
    """Escape user and academic data before rendering HTML."""
    return escape(str(value), quote=True)


def report_metrics(
    tasks: list[Task], subjects: list[Subject], study_hours: int = 0
) -> dict[str, int]:
    """Return the four real metrics displayed at the top of the report."""
    dashboard = calculate_dashboard_metrics(tasks, subjects)
    rates = [
        float(calculate_subject_progress(tasks, subject.id)["completion_rate"])
        for subject in subjects
    ]
    weekly_average = round(sum(rates) / len(rates)) if rates else 0
    return {
        "semester_progress": round(float(dashboard["completion_rate"])),
        "completed_tasks": int(dashboard["completed_tasks"]),
        "study_hours": max(0, int(study_hours)),
        "weekly_average": weekly_average,
    }


def task_distribution(tasks: list[Task]) -> dict[str, int]:
    """Group task states into the three categories used by the Figma chart."""
    return {
        "completed": sum(task.status == TaskStatus.CONCLUIDA for task in tasks),
        "in_progress": sum(task.status == TaskStatus.EM_ANDAMENTO for task in tasks),
        "to_do": sum(task.status in (TaskStatus.PENDENTE, TaskStatus.ATRASADA) for task in tasks),
    }


def report_insight(subjects: list[Subject], tasks: list[Task]) -> str:
    """Create a concise recommendation from strongest and weakest subjects."""
    if not subjects:
        return "Cadastre disciplinas para receber um plano de estudos recomendado."
    progress = [
        (subject, float(calculate_subject_progress(tasks, subject.id)["completion_rate"]))
        for subject in subjects
    ]
    best_subject, _ = max(progress, key=lambda item: item[1])
    weakest_subject, _ = min(progress, key=lambda item: item[1])
    if best_subject.id == weakest_subject.id:
        return (
            f"Continue avançando em {best_subject.name} e registre novas tarefas para "
            "acompanhar sua evolução."
        )
    return (
        f"Seu melhor desempenho está em {best_subject.name}. Para equilibrar o semestre, "
        f"reserve duas sessões extras para {weakest_subject.name} nesta semana."
    )


def build_report_pdf(
    user: dict[str, str],
    subjects: list[Subject],
    tasks: list[Task],
    metrics: dict[str, int],
) -> bytes:
    """Build a downloadable academic summary using the project's PDF dependency."""
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Relatório Acadêmico - EduTrack Orbit AI",
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("EduTrack Orbit AI", styles["Title"]),
        Paragraph("Relatório acadêmico", styles["Heading1"]),
        Paragraph(
            f"Estudante: {safe(user.get('name', 'Estudante'))}<br/>"
            f"Gerado em: {date.today():%d/%m/%Y}",
            styles["BodyText"],
        ),
        Spacer(1, 0.35 * cm),
    ]
    summary = [
        ["Progresso", "Concluídas", "Horas de estudo", "Média por disciplina"],
        [
            f"{metrics['semester_progress']}%",
            str(metrics["completed_tasks"]),
            f"{metrics['study_hours']} h",
            f"{metrics['weekly_average']}%",
        ],
    ]
    summary_table = Table(summary, colWidths=[4.2 * cm] * 4)
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7C3AED")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend([summary_table, Spacer(1, 0.45 * cm)])
    story.append(Paragraph("Desempenho por disciplina", styles["Heading2"]))
    rows = [["Disciplina", "Tarefas", "Progresso"]]
    rows.extend(
        [
            subject.name,
            str(sum(task.subject_id == subject.id for task in tasks)),
            f"{calculate_subject_progress(tasks, subject.id)['completion_rate']:g}%",
        ]
        for subject in subjects
    )
    if len(rows) == 1:
        rows.append(["Nenhuma disciplina cadastrada", "0", "0%"])
    subject_table = Table(rows, colWidths=[10.5 * cm, 2.5 * cm, 3.8 * cm])
    subject_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDE9FE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F1757")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend(
        [
            subject_table,
            Spacer(1, 0.45 * cm),
            Paragraph("Insight do Orbit", styles["Heading2"]),
            Paragraph(safe(report_insight(subjects, tasks)), styles["BodyText"]),
        ]
    )
    document.build(story)
    return output.getvalue()


def install_reports_css(user: dict[str, str]) -> None:
    """Install report styles and render the approved desktop header."""
    css = (Path(__file__).parent / "figma_reports.css").read_text(encoding="utf-8")
    theme_class = " orbit-reports-dark" if st.session_state.get("edutrack_dark_mode") else ""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="orbit-reports{theme_class}" aria-label="Relatórios acadêmicos">
  <header class="orbit-reports-topbar">
    <div><h1>Boa noite, {first_name}</h1><p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-reports-header-icons">
      <span class="orbit-reports-search">{icon("search", "")} Buscar...</span>
      <span class="orbit-reports-bell">{icon("bell", "Notificações")}</span>
    </div>
  </header>
  <div class="orbit-reports-heading">
    <h2>Relatórios</h2>
    <p>Acompanhe sua evolução e identifique onde concentrar seus estudos.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_report_metrics(metrics: dict[str, int]) -> None:
    """Render the four report KPI cards."""
    cards = (
        ("Progresso do semestre", f"{metrics['semester_progress']}%", "purple"),
        ("Tarefas concluídas", metrics["completed_tasks"], "green"),
        ("Horas de estudo", f"{metrics['study_hours']} h", "orange"),
        ("Média semanal", f"{metrics['weekly_average']}%", "pink"),
    )
    content = "".join(
        f'<div class="orbit-report-metric {color}"><span>{safe(label)}</span>'
        f"<strong>{safe(value)}</strong></div>"
        for label, value, color in cards
    )
    st.markdown(
        f'<section class="orbit-report-metrics">{content}</section>', unsafe_allow_html=True
    )


def render_performance(subjects: list[Subject], tasks: list[Task]) -> None:
    """Render real subject completion bars."""
    palette = ("purple", "lavender", "green", "orange")
    rows = "".join(
        '<div class="orbit-performance-row">'
        f"<span>{safe(subject.name)}</span>"
        f'<div class="orbit-performance-track"><i class="{palette[index % len(palette)]}" '
        f'style="width:{calculate_subject_progress(tasks, subject.id)["completion_rate"]}%"></i></div>'
        f"<strong>{calculate_subject_progress(tasks, subject.id)['completion_rate']:g}%</strong></div>"
        for index, subject in enumerate(subjects[:4])
    )
    if not rows:
        rows = '<p class="orbit-report-empty">Nenhuma disciplina cadastrada.</p>'
    st.markdown(
        '<section class="orbit-report-card orbit-performance"><h3>Desempenho por disciplina</h3>'
        f"{rows}</section>",
        unsafe_allow_html=True,
    )


def render_distribution(tasks: list[Task]) -> None:
    """Render a CSS donut and accessible task distribution legend."""
    distribution = task_distribution(tasks)
    total = len(tasks)
    completed = round(100 * distribution["completed"] / total) if total else 0
    progress = round(100 * distribution["in_progress"] / total) if total else 0
    todo = max(0, 100 - completed - progress) if total else 0
    legend = (
        ("green", "Concluídas", distribution["completed"], completed),
        ("orange", "Em andamento", distribution["in_progress"], progress),
        ("purple", "A fazer", distribution["to_do"], todo),
    )
    legend_html = "".join(
        f'<li><i class="{color}"></i>{label} · {count} ({percent}%)</li>'
        for color, label, count, percent in legend
    )
    st.markdown(
        f"""
<section class="orbit-report-card orbit-distribution">
  <h3>Distribuição das tarefas</h3>
  <div class="orbit-donut-wrap">
    <div class="orbit-donut" style="--completed:{completed};--progress:{progress}">
      <strong>{total}</strong><span>tarefas</span>
    </div>
    <ul>{legend_html}</ul>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )


def render_recent_history(tasks: list[Task]) -> None:
    """Render the four most recent task events."""
    recent = sorted(tasks, key=lambda task: (task.due_date, task.title), reverse=True)[:4]
    rows = "".join(
        '<div class="orbit-history-row">'
        f"<time>{task.due_date:%d %b}</time><span>{safe(task.subject_name)}</span>"
        f"<span>{safe(task.title)}</span><strong>{safe(task.status.value)}</strong></div>"
        for task in recent
    )
    if not rows:
        rows = '<p class="orbit-report-empty">Nenhuma atividade recente.</p>'
    st.markdown(
        '<section class="orbit-report-card orbit-history"><h3>Histórico recente</h3>'
        f"{rows}</section>",
        unsafe_allow_html=True,
    )


@st.dialog("Plano recomendado")
def render_recommended_plan(subjects: list[Subject], tasks: list[Task]) -> None:
    """Show the recommendation behind the Figma call-to-action."""
    st.markdown(f"### ✦ Insight do Orbit\n\n{report_insight(subjects, tasks)}")
    if subjects:
        counts = Counter(task.subject_id for task in tasks if task.status != TaskStatus.CONCLUIDA)
        focus = max(subjects, key=lambda subject: counts[subject.id])
        st.markdown(
            f"**Plano desta semana:** reserve dois blocos de 45 minutos para "
            f"**{focus.name}** e finalize uma tarefa pendente por bloco."
        )
