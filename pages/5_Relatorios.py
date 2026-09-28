"""Desktop academic reports aligned with the approved Figma frames."""

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.services.data_service import data_service_for_user, load_academic_data
from src.ui.figma_profile import DEFAULT_PROFILE_PREFERENCES, load_profile_section
from src.ui.figma_reports import (
    build_report_pdf,
    install_reports_css,
    render_distribution,
    render_performance,
    render_recent_history,
    render_recommended_plan,
    render_report_metrics,
    report_insight,
    report_metrics,
)
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Relatórios - EduTrack Orbit AI", page_icon="📊", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)

service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)
preferences = load_profile_section(
    st.session_state,
    user,
    "preferences",
    DEFAULT_PROFILE_PREFERENCES,
)
install_reports_css(user)

with st.container(key="reports_controls"):
    semester_column, subject_column, spacer_column, export_column = st.columns([1, 1.18, 2.2, 0.85])
    with semester_column:
        st.selectbox("Período", ("Semestre atual",), label_visibility="collapsed")
    with subject_column:
        selected_subject = st.selectbox(
            "Disciplina",
            ("Todas as disciplinas", *(subject.name for subject in subjects)),
            label_visibility="collapsed",
        )

filtered_subjects = subjects
filtered_tasks = tasks
if selected_subject != "Todas as disciplinas":
    filtered_subjects = [subject for subject in subjects if subject.name == selected_subject]
    filtered_ids = {subject.id for subject in filtered_subjects}
    filtered_tasks = [task for task in tasks if task.subject_id in filtered_ids]

metrics = report_metrics(filtered_tasks, filtered_subjects, preferences["study_hours"])
pdf = build_report_pdf(user, filtered_subjects, filtered_tasks, metrics)
with export_column:
    st.download_button(
        "Exportar PDF",
        data=pdf,
        file_name="relatorio-edutrack-orbit.pdf",
        mime="application/pdf",
        type="primary",
        width="stretch",
    )

render_report_metrics(metrics)

performance_column, distribution_column = st.columns([1.62, 1])
with performance_column:
    render_performance(filtered_subjects, filtered_tasks)
with distribution_column:
    render_distribution(filtered_tasks)

insight_column, history_column = st.columns([1, 1.62])
with insight_column:
    with st.container(key="reports_insight"):
        st.markdown(
            f"### ✦ Insight do Orbit\n\n{report_insight(filtered_subjects, filtered_tasks)}"
        )
        if st.button("Ver plano recomendado", type="primary"):
            render_recommended_plan(filtered_subjects, filtered_tasks)
with history_column:
    render_recent_history(filtered_tasks)
