"""Public support and contact page for EduTrack Orbit AI."""

import streamlit as st
from src.core.auth_session import current_user, initialize_auth_state
from src.ui.figma_support import (
    SUPPORT_CATEGORIES,
    install_support_css,
    is_valid_support_email,
    render_support_footer,
    render_support_header,
    render_support_sidebar,
)
from src.ui.theme import inject_custom_css

st.set_page_config(
    page_title="Suporte - EduTrack Orbit AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_custom_css()
initialize_auth_state(st.session_state)
theme_class = install_support_css()
user = current_user(st.session_state) or {}

with st.container(key="support_layout"):
    form_column, help_column = st.columns([620, 820], gap=None)
    with form_column:
        with st.container(key="support_form_pane"):
            render_support_header(theme_class)
            with st.form("desktop_support_request", clear_on_submit=False):
                name = st.text_input("Nome", value=user.get("name", ""), placeholder="Seu nome")
                email = st.text_input(
                    "E-mail", value=user.get("email", ""), placeholder="nome@exemplo.com"
                )
                category = st.selectbox("Categoria", SUPPORT_CATEGORIES)
                subject = st.text_input("Assunto", placeholder="Resuma sua dúvida")
                description = st.text_area(
                    "Descrição",
                    placeholder="Conte o que aconteceu e como podemos ajudar.",
                    height=130,
                )
                requested = st.form_submit_button(
                    "Enviar solicitação", type="primary", width="stretch"
                )

            if requested:
                if not is_valid_support_email(email):
                    st.warning("Informe um e-mail válido para receber orientações.")
                elif not subject.strip() or len(description.strip()) < 10:
                    st.warning(
                        "Preencha o assunto e descreva sua dúvida com pelo menos 10 caracteres."
                    )
                else:
                    st.success(
                        f"Solicitação de {category.lower()} registrada para demonstração. "
                        "Nenhuma mensagem externa foi enviada."
                    )
            render_support_footer()
    with help_column:
        with st.container(key="support_help_pane"):
            render_support_sidebar()
