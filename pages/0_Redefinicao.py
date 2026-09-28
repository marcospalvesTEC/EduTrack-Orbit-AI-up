"""Desktop password reset flow aligned with the approved Figma frames."""

import streamlit as st
from src.core.auth_session import (
    AUTH_USERS_KEY,
    RECOVERY_EMAIL_KEY,
    current_user,
    initialize_auth_state,
)
from src.services.demo_auth import DemoAuthService
from src.services.xano import configured_xano_base_url
from src.ui.figma_password_reset import (
    install_password_reset_css,
    render_password_criteria,
    render_reset_brand,
    render_reset_footer,
    render_reset_visual,
    render_secure_session,
)
from src.ui.theme import inject_custom_css
from streamlit.errors import StreamlitPageNotFoundError

st.set_page_config(
    page_title="Redefinir senha - EduTrack Orbit AI",
    page_icon="🔑",
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
recovery_email = st.session_state.get(RECOVERY_EMAIL_KEY)
theme_class = install_password_reset_css()

with st.container(key="reset_layout"):
    form_column, visual_column = st.columns([620, 820], gap=None)
    with form_column:
        with st.container(key="reset_form_pane"):
            render_reset_brand(theme_class)
            with st.form("desktop_password_reset", clear_on_submit=False):
                password = st.text_input("Nova senha", type="password")
                confirmation = st.text_input("Confirmar nova senha", type="password")
                render_password_criteria(password)
                render_secure_session()
                submitted = st.form_submit_button(
                    "Salvar nova senha", type="primary", width="stretch"
                )

            if submitted:
                if using_xano:
                    st.info("A redefinição pelo Xano será conectada na etapa de integração.")
                elif not recovery_email:
                    st.error("A sessão de recuperação é inválida ou expirou.")
                else:
                    result = service.reset_password(recovery_email, password, confirmation)
                    if result.success:
                        st.session_state[RECOVERY_EMAIL_KEY] = None
                        st.success(result.message)
                    else:
                        st.error(result.message)

            with st.container(key="reset_login_link"):
                try:
                    st.page_link("app.py", label="←  Voltar para o Login", width="stretch")
                except StreamlitPageNotFoundError:
                    st.markdown("←  Voltar para o Login")
            render_reset_footer()
    with visual_column:
        with st.container(key="reset_visual_pane"):
            render_reset_visual()
