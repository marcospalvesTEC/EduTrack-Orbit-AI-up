"""Desktop password recovery flow aligned with the approved Figma frames."""

import streamlit as st
from src.core.auth_session import (
    AUTH_USERS_KEY,
    RECOVERY_EMAIL_KEY,
    current_user,
    initialize_auth_state,
)
from src.services.demo_auth import DemoAuthService
from src.services.xano import configured_xano_base_url
from src.ui.figma_recovery import (
    install_recovery_css,
    render_recovery_brand,
    render_recovery_footer,
    render_recovery_visual,
    render_secure_link_notice,
)
from src.ui.theme import inject_custom_css
from streamlit.errors import StreamlitPageNotFoundError

st.set_page_config(
    page_title="Recuperar senha - EduTrack Orbit AI",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_custom_css()
initialize_auth_state(st.session_state)

if current_user(st.session_state) is not None:
    try:
        st.switch_page("app.py")
    except StreamlitPageNotFoundError:
        st.stop()

using_xano = configured_xano_base_url() is not None
service = DemoAuthService(st.session_state[AUTH_USERS_KEY])
theme_class = install_recovery_css()

with st.container(key="recovery_layout"):
    form_column, visual_column = st.columns([620, 820], gap=None)
    with form_column:
        with st.container(key="recovery_form_pane"):
            render_recovery_brand(theme_class)
            with st.form("desktop_password_recovery", clear_on_submit=False):
                email = st.text_input("E-mail", placeholder="nome@exemplo.com")
                render_secure_link_notice()
                requested = st.form_submit_button(
                    "Enviar link de recuperação", type="primary", width="stretch"
                )

            if requested:
                normalized_email = service.normalize_email(email)
                if not using_xano and service.has_user(normalized_email):
                    st.session_state[RECOVERY_EMAIL_KEY] = normalized_email
                else:
                    st.session_state[RECOVERY_EMAIL_KEY] = None
                st.session_state["recovery_request_sent"] = True
                st.success(
                    "Se houver uma conta associada a este e-mail, as instruções de recuperação "
                    "estarão disponíveis."
                )

            if st.session_state.get("recovery_request_sent"):
                try:
                    st.page_link(
                        "pages/0_Redefinicao.py",
                        label="Continuar para criar nova senha",
                        icon="🔑",
                        width="stretch",
                    )
                except StreamlitPageNotFoundError:
                    st.markdown("Continuar para criar nova senha")

            with st.container(key="recovery_login_link"):
                try:
                    st.page_link("app.py", label="←  Voltar para o Login", width="stretch")
                except StreamlitPageNotFoundError:
                    st.markdown("←  Voltar para o Login")

            with st.container(key="recovery_support"):
                st.caption("Não reconhece o e-mail?")
                try:
                    st.page_link(
                        "pages/0_Suporte.py",
                        label="Falar com o suporte",
                        width="stretch",
                    )
                except StreamlitPageNotFoundError:
                    st.markdown(
                        '<a class="orbit-recovery-support-fallback" href="/Suporte" '
                        'target="_self">Falar com o suporte</a>',
                        unsafe_allow_html=True,
                    )
            render_recovery_footer()
    with visual_column:
        with st.container(key="recovery_visual_pane"):
            render_recovery_visual()
