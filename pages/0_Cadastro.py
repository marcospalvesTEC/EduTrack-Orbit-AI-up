"""Desktop registration flow aligned with the approved Figma frames."""

import streamlit as st
from src.core.auth_session import AUTH_USERS_KEY, current_user, initialize_auth_state, sign_in
from src.services.demo_auth import DemoAuthService
from src.services.xano import XanoAuthService, configured_xano_base_url
from src.ui.figma_profile import DEFAULT_PROFILE_DETAILS, save_profile_section
from src.ui.figma_registration import (
    COURSE_OPTIONS,
    install_registration_css,
    render_registration_brand,
    render_registration_footer,
    render_registration_visual,
    render_strength,
)
from src.ui.theme import inject_custom_css
from streamlit.errors import StreamlitPageNotFoundError

st.set_page_config(
    page_title="Criar conta - EduTrack Orbit AI",
    page_icon="✨",
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

base_url = configured_xano_base_url()
using_xano = base_url is not None
service = (
    XanoAuthService(base_url) if base_url else DemoAuthService(st.session_state[AUTH_USERS_KEY])
)
theme_class = install_registration_css()

with st.container(key="registration_layout"):
    form_column, visual_column = st.columns([620, 820], gap=None)
    with form_column:
        with st.container(key="registration_form_pane"):
            render_registration_brand(theme_class)
            with st.form("desktop_registration", clear_on_submit=False):
                identity_name, identity_email = st.columns(2)
                with identity_name:
                    name = st.text_input("Nome completo", placeholder="Nome do estudante")
                with identity_email:
                    email = st.text_input("E-mail", placeholder="email@exemplo.com")

                education_course, education_institution = st.columns(2)
                with education_course:
                    course = st.selectbox("Curso", COURSE_OPTIONS)
                with education_institution:
                    institution = st.text_input("Instituição", placeholder="Digite ou selecione")

                security_password, security_confirmation = st.columns(2)
                with security_password:
                    password = st.text_input("Senha", type="password")
                with security_confirmation:
                    confirmation = st.text_input("Confirmar senha", type="password")

                render_strength(password)
                accepted_terms = st.checkbox(
                    "Li e aceito os Termos de Uso e a Política de Privacidade."
                )
                submitted = st.form_submit_button("Criar conta", type="primary", width="stretch")

            if submitted:
                if not accepted_terms:
                    st.error("Aceite os Termos de Uso e a Política de Privacidade para continuar.")
                else:
                    response = service.register(name, email, password, confirmation)
                    result = response.result if using_xano else response
                    token = response.token if using_xano else None
                    if result.success and result.user:
                        sign_in(st.session_state, result.user, token)
                        details = {
                            **DEFAULT_PROFILE_DETAILS,
                            "course": course if course != COURSE_OPTIONS[0] else "Não informado",
                            "institution": institution.strip() or "Não informada",
                        }
                        save_profile_section(st.session_state, result.user, "details", details)
                        st.success(result.message)
                        try:
                            st.switch_page("app.py")
                        except StreamlitPageNotFoundError:
                            st.stop()
                    else:
                        st.error(result.message)

            with st.container(key="registration_login_link"):
                try:
                    st.page_link("app.py", label="Já possui uma conta?  Entrar", width="stretch")
                except StreamlitPageNotFoundError:
                    st.markdown("Já possui uma conta?  Entrar")
            st.markdown(
                '<div class="orbit-registration-privacy">◇&nbsp; Seus dados serão usados somente para sua experiência acadêmica.</div>',
                unsafe_allow_html=True,
            )
            render_registration_footer()
    with visual_column:
        with st.container(key="registration_visual_pane"):
            render_registration_visual()
