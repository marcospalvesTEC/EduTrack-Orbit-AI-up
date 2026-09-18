"""Tasks management page aligned with the approved Figma desktop frame."""

from datetime import date, timedelta

import streamlit as st

from src.core.auth_session import render_session_sidebar, require_authenticated
from src.models.task import Task, TaskPriority, TaskStatus
from src.services.data_service import data_service_for_user, load_academic_data
from src.services.xano import XanoError
from src.ui.figma_tasks import (
    filter_tasks,
    render_task_board,
    render_task_dialog_theme_marker,
    render_task_metrics,
    render_tasks_header,
    safe,
)
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Tarefas - EduTrack Orbit AI", page_icon="📝", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)
service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)
dialog = st.dialog if hasattr(st, "dialog") else st.experimental_dialog


def render_new_task_form() -> None:
    """Create a task without compressing the Kanban board."""
    subject_options = {subject.name: subject.id for subject in subjects}
    if not subject_options:
        st.info("Cadastre uma disciplina antes de adicionar tarefas.")
        return
    with st.form("form_add_task", clear_on_submit=True):
        identity, planning = st.columns([2, 1])
        with identity:
            title = st.text_input("Título da tarefa", placeholder="Ex.: Exercícios 1 a 10")
            subject_name = st.selectbox("Disciplina", options=list(subject_options))
            description = st.text_area(
                "Descrição", placeholder="Instruções ou observações..."
            )
        with planning:
            due_date = st.date_input("Data de entrega", value=date.today() + timedelta(days=3))
            priority = st.selectbox(
                "Prioridade", options=[item.value for item in TaskPriority], index=1
            )
            status = st.selectbox(
                "Status",
                options=[TaskStatus.PENDENTE.value, TaskStatus.EM_ANDAMENTO.value],
            )
        submitted = st.form_submit_button("Cadastrar tarefa", type="primary", width="stretch")
    if submitted:
        if not title.strip():
            st.error("O título da tarefa é obrigatório.")
            return
        try:
            service.add_task(
                Task(
                    title=title.strip(),
                    subject_id=subject_options[subject_name],
                    subject_name=subject_name,
                    due_date=due_date,
                    priority=TaskPriority(priority),
                    status=TaskStatus(status),
                    description=description.strip(),
                )
            )
        except XanoError as error:
            st.error(f"Não foi possível cadastrar: {error}")
        else:
            st.success(f"Tarefa '{title.strip()}' adicionada com sucesso!")
            st.rerun()


def render_task_details(task: Task) -> None:
    """Show task details, edit controls and destructive action."""
    render_task_dialog_theme_marker()
    details_tab, edit_tab, delete_tab = st.tabs(["Detalhes", "Editar", "Excluir"])
    with details_tab:
        st.subheader(task.title)
        st.caption(task.description or "Sem descrição adicional.")
        st.markdown(
            '<div class="orbit-task-dialog-meta">'
            f'<div><span>Disciplina</span><strong>{safe(task.subject_name)}</strong></div>'
            f'<div><span>Entrega</span><strong>{task.due_date:%d/%m/%Y}</strong></div>'
            f'<div><span>Prioridade</span><strong>{task.priority.value}</strong></div>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.write(f"**Status:** {task.status.value}")
        toggle_label = (
            "Reabrir tarefa"
            if task.status == TaskStatus.CONCLUIDA
            else "Concluir tarefa"
        )
        if st.button(toggle_label, type="primary", width="stretch", key=f"toggle_task_{task.id}"):
            service.toggle_task_status(task.id)
            st.rerun()

    with edit_tab:
        subject_names = [subject.name for subject in subjects]
        current_subject = (
            subject_names.index(task.subject_name)
            if task.subject_name in subject_names
            else 0
        )
        status_values = [item.value for item in TaskStatus]
        priority_values = [item.value for item in TaskPriority]
        with st.form(f"edit_task_{task.id}"):
            edit_title = st.text_input("Título", value=task.title)
            edit_subject = st.selectbox("Disciplina", subject_names, index=current_subject)
            edit_due = st.date_input("Data de entrega", value=task.due_date)
            edit_status = st.selectbox(
                "Status", status_values, index=status_values.index(task.status.value)
            )
            edit_priority = st.selectbox(
                "Prioridade", priority_values, index=priority_values.index(task.priority.value)
            )
            edit_description = st.text_area("Descrição", value=task.description)
            save_task = st.form_submit_button(
                "Salvar alterações", type="primary", width="stretch"
            )
        if save_task:
            if not edit_title.strip():
                st.error("O título da tarefa é obrigatório.")
            else:
                selected_subject = next(
                    subject for subject in subjects if subject.name == edit_subject
                )
                try:
                    service.update_task(
                        task.id,
                        title=edit_title.strip(),
                        subject_id=selected_subject.id,
                        subject_name=selected_subject.name,
                        due_date=edit_due,
                        status=TaskStatus(edit_status),
                        priority=TaskPriority(edit_priority),
                        description=edit_description.strip(),
                    )
                except XanoError as error:
                    st.error(f"Não foi possível atualizar: {error}")
                else:
                    st.success("Tarefa atualizada.")
                    st.rerun()

    with delete_tab:
        st.warning("Esta ação não pode ser desfeita.")
        confirmed = st.checkbox(
            "Confirmo a exclusão desta tarefa", key=f"confirm_task_{task.id}"
        )
        if st.button(
            "Excluir tarefa",
            key=f"delete_task_{task.id}",
            disabled=not confirmed,
            width="stretch",
        ):
            try:
                service.delete_task(task.id)
            except XanoError as error:
                st.error(f"Não foi possível excluir: {error}")
            else:
                st.success("Tarefa excluída.")
                st.rerun()


@dialog("Nova tarefa", width="large")
def render_new_task_dialog() -> None:
    """Open the task creation form in a modal."""
    render_task_dialog_theme_marker()
    render_new_task_form()


@dialog("Detalhes da tarefa", width="large")
def render_task_dialog(task: Task) -> None:
    """Open details, editing and deletion for a selected task."""
    render_task_details(task)


render_tasks_header(user)
intro, action = st.columns([5, 1])
with intro:
    st.markdown(
        '<div class="orbit-task-intro"><h1>Tarefas</h1>'
        "<p>Planeje entregas, acompanhe prioridades e conclua atividades.</p></div>",
        unsafe_allow_html=True,
    )
with action:
    new_clicked = st.button("+ Nova tarefa", key="new_task_action", use_container_width=True)

if new_clicked:
    render_new_task_dialog()

search_column, status_column, priority_column = st.columns([2.5, 1, 1])
with search_column:
    query = st.text_input(
        "Buscar tarefa ou disciplina",
        placeholder="⌕  Buscar tarefa ou disciplina...",
        label_visibility="collapsed",
    )
with status_column:
    status_filter = st.selectbox(
        "Status",
        ("Todos os status", "A fazer", "Em andamento", "Concluídas"),
        label_visibility="collapsed",
    )
with priority_column:
    priority_filter = st.selectbox(
        "Prioridade",
        ("Todas as prioridades", "Baixa", "Média", "Alta"),
        label_visibility="collapsed",
    )

render_task_metrics(tasks)
visible_tasks = filter_tasks(tasks, query, status_filter, priority_filter)
selected_task = render_task_board(visible_tasks)
if selected_task is not None:
    render_task_dialog(selected_task)

if not tasks:
    st.info("Você ainda não cadastrou tarefas. Use “Nova tarefa” para começar.")
