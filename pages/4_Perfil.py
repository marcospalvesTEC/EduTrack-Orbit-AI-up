"""Student profile aligned with the approved Figma desktop frames."""

import streamlit as st
from src.core.auth_session import (
    AUTH_USERS_KEY,
    render_session_sidebar,
    require_authenticated,
    sign_out,
    update_current_user_name,
)
from src.services.data_service import data_service_for_user, load_academic_data
from src.services.demo_auth import DemoAuthService
from src.ui.figma_profile import (
    DEFAULT_PROFILE_DETAILS,
    DEFAULT_PROFILE_PREFERENCES,
    load_profile_section,
    profile_metrics,
    profile_photo_data_url,
    render_personal_data,
    render_preferences,
    render_profile_avatar,
    render_profile_header,
    render_security_summary,
    render_summary_card,
    save_profile_section,
)
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Meu Perfil - EduTrack Orbit AI", page_icon="👤", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)
service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)


def render_edit_profile_dialog() -> None:
    """Update the public name and prototype-only academic details."""
    details = load_profile_section(st.session_state, user, "details", DEFAULT_PROFILE_DETAILS)
    with st.form("profile_details_form"):
        if details["photo_data_url"]:
            st.image(details["photo_data_url"], width=96, caption="Foto atual")
        photo = st.file_uploader(
            "Foto do perfil",
            type=["png", "jpg", "jpeg", "webp"],
            help="Envie uma imagem PNG, JPG, JPEG ou WebP de até 5 MB.",
        )
        name = st.text_input("Nome completo", value=user["name"])
        st.text_input("E-mail", value=user["email"], disabled=True)
        first, second = st.columns(2)
        with first:
            course = st.text_input("Curso", value=details["course"])
            semester = st.text_input("Semestre atual", value=details["semester"])
        with second:
            institution = st.text_input("Instituição", value=details["institution"])
        submitted = st.form_submit_button(
            "Salvar informações do perfil", type="primary", width="stretch"
        )
    if submitted:
        photo_data_url = details["photo_data_url"]
        if photo is not None:
            try:
                photo_data_url = profile_photo_data_url(
                    photo.name, photo.type or "", photo.getvalue()
                )
            except ValueError as error:
                st.error(str(error))
                return
        if update_current_user_name(st.session_state, name) is None:
            st.error("Informe um nome válido.")
            return
        save_profile_section(
            st.session_state,
            user,
            "details",
            {
                "course": course.strip() or "Não informado",
                "institution": institution.strip() or "Não informada",
                "semester": semester.strip() or "Não informado",
                "photo_data_url": photo_data_url,
            },
        )
        st.success("Perfil atualizado.")
        st.session_state["profile_active_dialog"] = None
        st.rerun()


def render_preferences_dialog() -> None:
    """Edit user-scoped profile preferences for the prototype session."""
    preferences = load_profile_section(
        st.session_state, user, "preferences", DEFAULT_PROFILE_PREFERENCES
    )
    languages = ("Português (Brasil)", "English (US)", "Español")
    themes = ("Seguir sistema", "Claro", "Escuro")
    notifications = ("Ativadas", "Desativadas")
    reminders = ("No horário", "15 min antes", "30 min antes", "1 h antes", "Desativados")
    with st.form("profile_preferences_form"):
        first, second = st.columns(2)
        with first:
            weekly_goal = st.number_input(
                "Meta semanal de estudos (h)",
                min_value=1,
                max_value=80,
                value=int(preferences["weekly_goal"]),
            )
            language = st.selectbox(
                "Idioma do aplicativo",
                languages,
                index=languages.index(preferences["language"]),
            )
            task_notifications = st.selectbox(
                "Notificações de tarefas",
                notifications,
                index=notifications.index(preferences["task_notifications"]),
            )
        with second:
            theme = st.selectbox("Tema", themes, index=themes.index(preferences["theme"]))
            agenda_reminder = st.selectbox(
                "Lembretes da agenda",
                reminders,
                index=reminders.index(preferences["agenda_reminder"]),
            )
            study_hours = st.number_input(
                "Tempo de estudo registrado (h)",
                min_value=0,
                max_value=10000,
                value=int(preferences["study_hours"]),
            )
        submitted = st.form_submit_button("Salvar preferências", type="primary", width="stretch")
    if submitted:
        save_profile_section(
            st.session_state,
            user,
            "preferences",
            {
                "weekly_goal": weekly_goal,
                "language": language,
                "theme": theme,
                "task_notifications": task_notifications,
                "agenda_reminder": agenda_reminder,
                "study_hours": study_hours,
            },
        )
        if theme in {"Claro", "Escuro"}:
            is_dark = theme == "Escuro"
            st.session_state["edutrack_dark_mode"] = is_dark
            st.session_state["_edutrack_dark_mode_widget"] = is_dark
        st.success("Preferências atualizadas.")
        st.session_state["profile_active_dialog"] = None
        st.rerun()


def render_password_dialog() -> None:
    """Replace the local demonstration password without exposing the current one."""
    st.caption("A senha atual nunca é exibida.")
    with st.form("profile_password_form", clear_on_submit=True):
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirmar nova senha", type="password")
        submitted = st.form_submit_button("Alterar senha", type="primary", width="stretch")
    if submitted:
        result = DemoAuthService(st.session_state[AUTH_USERS_KEY]).reset_password(
            user["email"], new_password, confirm_password
        )
        if result.success:
            st.success("Senha alterada com sucesso.")
            st.session_state["profile_active_dialog"] = None
            st.rerun()
        else:
            st.error(result.message)


def open_profile_dialog(dialog_name: str) -> None:
    """Open one profile overlay without relying on Streamlit's portal styling."""
    st.session_state["profile_active_dialog"] = dialog_name


def close_profile_dialog() -> None:
    """Close the active profile overlay."""
    st.session_state["profile_active_dialog"] = None


def render_active_profile_dialog() -> None:
    """Render the active modal inside the themed app DOM."""
    dialog_name = st.session_state.get("profile_active_dialog")
    dialogs = {
        "profile": ("Editar perfil", render_edit_profile_dialog),
        "preferences": ("Preferências acadêmicas", render_preferences_dialog),
        "password": ("Alterar senha", render_password_dialog),
    }
    if dialog_name not in dialogs:
        return

    title, renderer = dialogs[dialog_name]
    with st.container(key="profile_dialog_overlay"):
        with st.container(key="profile_dialog_panel"):
            size_class = " orbit-profile-modal-small" if dialog_name == "password" else ""
            with st.container(key="profile_dialog_header"):
                title_column, close_column = st.columns([12, 1], vertical_alignment="center")
                with title_column:
                    st.markdown(
                        f'<div class="orbit-profile-modal-heading{size_class}">'
                        f"<h2>{title}</h2></div>",
                        unsafe_allow_html=True,
                    )
                with close_column:
                    with st.container(key="profile_dialog_close"):
                        st.button(
                            "×",
                            key=f"close_profile_{dialog_name}",
                            help="Fechar",
                            on_click=close_profile_dialog,
                        )
            renderer()


render_profile_header(user)
details = load_profile_section(st.session_state, user, "details", DEFAULT_PROFILE_DETAILS)
preferences = load_profile_section(
    st.session_state, user, "preferences", DEFAULT_PROFILE_PREFERENCES
)
metrics = profile_metrics(tasks, subjects, int(preferences["study_hours"]))

with st.container(key="profile_layout"):
    with st.container(key="profile_intro"):
        st.markdown(
            "<h1>Meu perfil</h1><p>Gerencie seus dados, preferências acadêmicas e segurança.</p>",
            unsafe_allow_html=True,
        )
    with st.container(key="profile_summary_card"):
        render_profile_avatar(str(details["photo_data_url"]))
        st.button(
            "Editar perfil",
            key="open_profile_editor",
            type="primary",
            width="stretch",
            on_click=open_profile_dialog,
            args=("profile",),
        )
        render_summary_card(metrics)
    with st.container(key="profile_personal_card"):
        render_personal_data(user, details)
    with st.container(key="profile_preferences_card"):
        render_preferences(preferences)
        st.button(
            "Editar preferências",
            key="open_profile_preferences",
            on_click=open_profile_dialog,
            args=("preferences",),
        )
    with st.container(key="profile_security_card"):
        render_security_summary()
        with st.container(key="profile_security_actions"):
            password_column, sessions_column = st.columns(2, vertical_alignment="center")
            with password_column:
                with st.container(key="profile_password_action"):
                    st.button(
                        "Alterar senha",
                        key="open_profile_password",
                        on_click=open_profile_dialog,
                        args=("password",),
                    )
            with sessions_column:
                with st.container(key="profile_sessions_action"):
                    if st.button("Encerrar sessões", key="close_profile_sessions"):
                        sign_out(st.session_state)
                        st.switch_page("app.py")

render_active_profile_dialog()

# Backward-compatible semantic hook used by the existing authentication integration test.
with st.container(key="profile_email_test_hook"):
    st.metric("E-mail", user["email"])
