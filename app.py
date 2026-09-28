"""EduTrack Orbit AI - Entry Point & Navigation Layout."""

import streamlit as st
from src.core.auth_session import current_user, initialize_auth_state, render_session_sidebar
from src.core.metrics import calculate_dashboard_metrics
from src.services.data_service import data_service_for_user, load_academic_data
from src.ui.auth import render_auth_portal
from src.ui.figma_dashboard import render_dashboard
from src.ui.theme import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="EduTrack Orbit AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Custom Visual Identity CSS
inject_custom_css()
initialize_auth_state(st.session_state)

user = current_user(st.session_state)
if user is None:
    render_auth_portal()
    st.stop()

# Initialize Simulated Data Service (persisted in st.session_state)
service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)


def render_demo_tools() -> None:
    """Keep prototype data actions available without expanding the Orbit shell."""
    if not getattr(service, "is_remote", False):
        if st.button("Carregar dados demonstrativos", width="stretch"):
            service.reset_to_defaults()
            st.success("Dados demonstrativos carregados.")
            st.rerun()

        if subjects:
            if st.button("Limpar meus dados", width="stretch"):
                st.session_state["confirm_clear_data"] = True
            if st.session_state.get("confirm_clear_data"):
                st.warning(f"Isso excluirá {len(subjects)} disciplina(s) e todas as tarefas.")
                confirm, cancel = st.columns(2)
                if confirm.button("Confirmar", type="primary", width="stretch"):
                    service.clear_all()
                    st.session_state["confirm_clear_data"] = False
                    st.rerun()
                if cancel.button("Cancelar", width="stretch"):
                    st.session_state["confirm_clear_data"] = False
                    st.rerun()


render_session_sidebar(user, demo_tools=render_demo_tools)

# The Figma overview provides its own visible heading and accessible main label.
render_dashboard(user, subjects, tasks, calculate_dashboard_metrics(tasks, subjects))

if not subjects:
    if getattr(service, "is_remote", False):
        st.info("Sua conta está pronta. Cadastre sua primeira disciplina para começar.")
    else:
        st.info(
            "Sua conta está pronta. Cadastre a primeira disciplina ou carregue dados demonstrativos pelo menu lateral."
        )
    action_subject, action_demo = st.columns(2)
    with action_subject:
        if st.button("Cadastrar primeira disciplina", type="primary", width="stretch"):
            st.switch_page("pages/2_Disciplinas.py")
    with action_demo:
        if getattr(service, "is_remote", False):
            st.caption("Seus dados serão salvos com segurança no Xano.")
        else:
            if st.button("Explorar com dados de exemplo", width="stretch"):
                service.reset_to_defaults()
                st.rerun()
