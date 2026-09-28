"""Streamlit components for the local demonstration authentication flow."""

from __future__ import annotations

import streamlit as st

from src.core.auth_session import (
    AUTH_USERS_KEY,
    initialize_auth_state,
    sign_in,
)
from src.services.demo_auth import DEMO_EMAIL, DEMO_PASSWORD, DemoAuthService
from src.services.xano import XanoAuthService, configured_xano_base_url
from src.ui.figma_login import (
    install_login_css,
    render_login_brand,
    render_login_footer,
    render_login_visual,
)


def _service() -> DemoAuthService:
    initialize_auth_state(st.session_state)
    return DemoAuthService(st.session_state[AUTH_USERS_KEY])


def _render_login(service: DemoAuthService | XanoAuthService, using_xano: bool) -> None:
    if not using_xano:
        st.markdown(
            f'<div class="orbit-login-notice">Conta de demonstração: '
            f"<strong>{DEMO_EMAIL}</strong> · senha: <strong>{DEMO_PASSWORD}</strong></div>",
            unsafe_allow_html=True,
        )
    with st.form("auth_login"):
        email = st.text_input("E-mail", placeholder=DEMO_EMAIL)
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submitted = st.form_submit_button("Entrar", type="primary", width="stretch")

    if submitted:
        response = service.authenticate(email, password)
        result = response.result if using_xano else response
        token = response.token if using_xano else None
        if result.success and result.user:
            sign_in(st.session_state, result.user, token)
            st.success(result.message)
            st.rerun()
        st.error(result.message)


def render_auth_portal() -> None:
    """Render the dedicated desktop login and its account actions."""
    base_url = configured_xano_base_url()
    using_xano = base_url is not None
    service = XanoAuthService(base_url) if base_url else _service()
    theme_class = install_login_css()

    with st.container(key="login_layout"):
        form_pane, visual_pane = st.columns([0.86, 1.14], gap=None)
        with form_pane:
            with st.container(key="login_form_pane"):
                render_login_brand(theme_class)
                if using_xano:
                    st.markdown(
                        '<div class="orbit-login-notice">Conectado ao backend seguro do EduTrack.</div>',
                        unsafe_allow_html=True,
                    )
                _render_login(service, using_xano)
                with st.container(key="login_actions"):
                    recovery_column, registration_column = st.columns(2)
                    with recovery_column:
                        st.page_link(
                            "pages/0_Recuperacao.py",
                            label="Esqueci minha senha",
                            width="stretch",
                        )
                    with registration_column:
                        st.page_link(
                            "pages/0_Cadastro.py",
                            label="Criar conta",
                            width="stretch",
                        )
                render_login_footer()
        with visual_pane:
            with st.container(key="login_visual_pane"):
                render_login_visual()
