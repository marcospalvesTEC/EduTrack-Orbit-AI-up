"""Subjects management page aligned with the approved Figma desktop frames."""

from datetime import date, timedelta

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.core.metrics import calculate_subject_progress
from src.models.subject import Subject
from src.services.data_service import data_service_for_user, load_academic_data
from src.services.xano import XanoError
from src.ui.figma_subjects import (
    deadline_label,
    filter_subjects,
    render_subject_cards,
    render_subject_dialog_theme_marker,
    render_subject_metrics,
    render_subjects_header,
    safe_color,
)
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Disciplinas - EduTrack Orbit AI", page_icon="📚", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)
service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)
dialog = st.dialog if hasattr(st, "dialog") else st.experimental_dialog


def render_new_subject_form() -> None:
    """Create a subject inside a spacious modal dialog."""
    with st.form("form_add_subject", clear_on_submit=True):
        identity, workload = st.columns([2, 1])
        with identity:
            new_name = st.text_input("Nome da disciplina", placeholder="Ex.: Física II")
            new_code = st.text_input("Código", placeholder="Ex.: FIS102")
            new_professor = st.text_input("Professor(a)", placeholder="Ex.: Prof. Roberto")
            new_description = st.text_area("Descrição", placeholder="Resumo da disciplina")
        with workload:
            new_workload = st.number_input(
                "Carga horária (h)", min_value=10, max_value=200, value=60
            )
            new_start = st.date_input("Data de início", value=date.today())
            new_end = st.date_input("Data de término", value=date.today() + timedelta(days=120))
            new_color = st.color_picker("Cor da disciplina", value="#7C3AED")
        submitted = st.form_submit_button("Cadastrar disciplina", type="primary", width="stretch")

    if submitted:
        if not new_name.strip() or not new_code.strip():
            st.error("Preencha o nome e o código da disciplina.")
        elif new_end < new_start:
            st.error("A data de término deve ser igual ou posterior à data de início.")
        else:
            try:
                service.add_subject(
                    Subject(
                        name=new_name.strip(),
                        code=new_code.strip(),
                        professor=new_professor.strip() or "Não informado",
                        workload_hours=int(new_workload),
                        color_hex=new_color,
                        description=new_description.strip(),
                        start_date=new_start,
                        end_date=new_end,
                    )
                )
            except XanoError as error:
                st.error(f"Não foi possível cadastrar: {error}")
            else:
                st.success(f"Disciplina '{new_name.strip()}' adicionada com sucesso!")
                st.rerun()


def render_subject_management() -> None:
    """Render details, editing and deletion inside the management dialog."""
    subject_by_id = {str(subject.id): subject for subject in subjects}
    selected_id = st.selectbox(
        "Disciplina",
        options=list(subject_by_id),
        format_func=lambda subject_id: subject_by_id[subject_id].name,
        key="manage_subject_id",
    )
    subject = subject_by_id[selected_id]
    progress = calculate_subject_progress(tasks, subject.id)
    details_tab, edit_tab, delete_tab = st.tabs(["Detalhes", "Editar", "Excluir"])

    with details_tab:
        st.write(f"Código: **{subject.code}**")
        st.write(f"Professor(a): **{subject.professor}**")
        st.write(f"Carga horária: **{subject.workload_hours} horas**")
        st.write(f"Período: **{subject.start_date:%d/%m/%Y} a {subject.end_date:%d/%m/%Y}**")
        st.write(
            f"Progresso: **{progress['completion_rate']}%** "
            f"({progress['completed_tasks']}/{progress['total_tasks']} tarefas)"
        )
        if subject.description:
            st.write(subject.description)

    with edit_tab:
        with st.form(f"edit_subject_{subject.id}"):
            edit_name = st.text_input("Nome", value=subject.name)
            edit_code = st.text_input("Código", value=subject.code)
            edit_professor = st.text_input("Professor(a)", value=subject.professor)
            edit_workload = st.number_input(
                "Carga horária (h)", min_value=10, max_value=200, value=subject.workload_hours
            )
            edit_description = st.text_area("Descrição", value=subject.description)
            edit_start = st.date_input("Data de início", value=subject.start_date)
            edit_end = st.date_input("Data de término", value=subject.end_date)
            edit_color = st.color_picker("Cor", value=subject.color_hex)
            save_subject = st.form_submit_button(
                "Salvar alterações", type="primary", width="stretch"
            )
        if save_subject:
            if not edit_name.strip() or not edit_code.strip():
                st.error("Nome e código são obrigatórios.")
            elif edit_end < edit_start:
                st.error("A data de término deve ser igual ou posterior à data de início.")
            else:
                try:
                    service.update_subject(
                        subject.id,
                        name=edit_name.strip(),
                        code=edit_code.strip(),
                        professor=edit_professor.strip() or "Não informado",
                        workload_hours=int(edit_workload),
                        description=edit_description.strip(),
                        start_date=edit_start,
                        end_date=edit_end,
                        color_hex=edit_color,
                    )
                except XanoError as error:
                    st.error(f"Não foi possível atualizar: {error}")
                else:
                    st.success("Disciplina atualizada.")
                    st.rerun()

    with delete_tab:
        st.warning(f"A exclusão também removerá {progress['total_tasks']} tarefa(s) vinculada(s).")
        confirm_delete = st.checkbox(
            "Confirmo a exclusão desta disciplina", key=f"confirm_subject_{subject.id}"
        )
        if st.button(
            "Excluir disciplina",
            key=f"delete_subject_{subject.id}",
            disabled=not confirm_delete,
            width="stretch",
        ):
            try:
                service.delete_subject(subject.id)
            except XanoError as error:
                st.error(f"Não foi possível excluir: {error}")
            else:
                st.success("Disciplina excluída.")
                st.rerun()


@dialog("Nova disciplina", width="large")
def render_new_subject_dialog() -> None:
    """Open the creation form without compressing the overview layout."""
    render_subject_dialog_theme_marker()
    render_new_subject_form()


@dialog("Gerenciar disciplinas", width="large")
def render_subject_management_dialog() -> None:
    """Open the complete edit/delete workflow from the header action."""
    render_subject_dialog_theme_marker()
    render_subject_management()


@dialog("Resumo da disciplina", width="large")
def render_subject_summary_dialog(subject: Subject) -> None:
    """Show useful academic details when a discipline card is selected."""
    render_subject_dialog_theme_marker()
    progress = calculate_subject_progress(tasks, subject.id)
    st.markdown(
        f'<div class="orbit-subject-dialog-accent" '
        f'style="background:{safe_color(subject.color_hex)}"></div>',
        unsafe_allow_html=True,
    )
    st.subheader(subject.name)
    st.caption(f"{subject.code} · {subject.professor}")
    st.markdown(
        '<div class="orbit-subject-dialog-metrics">'
        f"<div><span>Tarefas</span><strong>{progress['total_tasks']}</strong></div>"
        f"<div><span>Concluídas</span><strong>{progress['completed_tasks']}</strong></div>"
        f"<div><span>Pendentes</span><strong>{progress['pending_tasks']}</strong></div>"
        f"<div><span>Atrasadas</span><strong>{progress['overdue_tasks']}</strong></div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.progress(float(progress["completion_rate"]) / 100.0)
    st.caption(f"{progress['completion_rate']:g}% de progresso")
    st.write(f"**Carga horária:** {subject.workload_hours} horas")
    st.write(f"**Período:** {subject.start_date:%d/%m/%Y} a {subject.end_date:%d/%m/%Y}")
    st.write(f"**Prazo:** {deadline_label(subject, tasks)}")
    if subject.description:
        st.write(subject.description)


render_subjects_header(user)
intro, action = st.columns([4.25, 2.15])
with intro:
    st.markdown(
        '<div class="orbit-subject-intro"><h1>Disciplinas</h1>'
        "<p>Organize matérias, professores e seu progresso no semestre.</p></div>",
        unsafe_allow_html=True,
    )
with action:
    manage_action, new_action = st.columns(2)
    with manage_action:
        manage_clicked = st.button(
            "Gerenciar disciplinas",
            key="manage_subjects_action",
            use_container_width=True,
        )
    with new_action:
        new_clicked = st.button(
            "+ Nova disciplina",
            key="new_subject_action",
            use_container_width=True,
        )

if manage_clicked:
    render_subject_management_dialog()
if new_clicked:
    render_new_subject_dialog()

search_column, period_column, spacer = st.columns([3.6, 1, 0.75])
with search_column:
    query = st.text_input(
        "Buscar disciplina ou professor",
        placeholder="⌕  Buscar disciplina ou professor...",
        label_visibility="collapsed",
    )
with period_column:
    st.selectbox(
        "Período",
        ("Período atual", "Todos os períodos"),
        label_visibility="collapsed",
    )

render_subject_metrics(subjects, tasks)
visible_subjects = filter_subjects(subjects, query)
selected_subject = render_subject_cards(visible_subjects, tasks)

if selected_subject is not None:
    render_subject_summary_dialog(selected_subject)

if not subjects:
    st.info("Você ainda não cadastrou disciplinas. Use “Nova disciplina” para começar.")
