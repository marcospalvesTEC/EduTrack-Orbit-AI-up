"""Desktop Settings screen aligned with the approved Figma frames."""

import streamlit as st

from src.core.auth_session import (
    render_session_sidebar,
    require_authenticated,
)
from src.services.data_service import (
    data_service_for_user,
    load_academic_data,
)
from src.ui.figma_profile import (
    DEFAULT_PROFILE_PREFERENCES,
    load_profile_section,
    save_profile_section,
)
from src.ui.figma_settings import (
    ACCENT_COLORS,
    export_account_data,
    install_settings_css,
    load_settings,
    render_card_title,
    render_locked_setting,
    render_pet_preferences,
    save_settings,
    settings_key,
)
from src.ui.orbit_global_actions import render_global_actions
from src.ui.theme import inject_custom_css


st.set_page_config(
    page_title="Configurações - EduTrack Orbit AI",
    page_icon="⚙️",
    layout="wide",
)

# ---------------------------------------------------------
# TEMA PENDENTE
# ---------------------------------------------------------

pending_theme = st.session_state.pop(
    "_settings_pending_theme",
    None,
)

if isinstance(pending_theme, bool):
    st.session_state["edutrack_dark_mode"] = pending_theme
    st.session_state["_edutrack_dark_mode_widget"] = pending_theme

# ---------------------------------------------------------
# ESTILOS GLOBAIS
# ---------------------------------------------------------

inject_custom_css()

# ---------------------------------------------------------
# AUTENTICAÇÃO
# ---------------------------------------------------------

user = require_authenticated()
render_session_sidebar(user)

# ---------------------------------------------------------
# DADOS ACADÊMICOS COM CACHE DE SESSÃO
# ---------------------------------------------------------

academic_cache_key = (
    "settings_academic_data:"
    f"{user.get('email', 'anonymous').strip().lower()}"
)

if academic_cache_key not in st.session_state:
    service = data_service_for_user(user)
    subjects, tasks = load_academic_data(service)
    st.session_state[academic_cache_key] = (subjects, tasks)
else:
    subjects, tasks = st.session_state[academic_cache_key]

# ---------------------------------------------------------
# CONFIGURAÇÕES DO USUÁRIO
# ---------------------------------------------------------

settings = load_settings(
    st.session_state,
    user,
)

prefix = settings_key(user)


def widget_key(name: str) -> str:
    """Build a stable, user-scoped widget key."""
    return f"{prefix}:{name}"


def current_value(name: str):
    """Read the current widget value or its persisted fallback."""
    return st.session_state.get(
        widget_key(name),
        settings[name],
    )


def apply_theme(dark: bool) -> None:
    """Preview a theme immediately while keeping controls synchronized."""
    st.session_state["edutrack_dark_mode"] = dark
    st.session_state["_edutrack_dark_mode_widget"] = dark
    st.session_state[widget_key("theme")] = "Escuro" if dark else "Claro"


# ---------------------------------------------------------
# CABEÇALHO
# ---------------------------------------------------------

install_settings_css(user)

render_global_actions(
    subjects,
    tasks,
    key_prefix="settings",
)

if st.session_state.pop(
    "_settings_saved_notice",
    False,
):
    st.success("Configurações salvas com sucesso.")

# =========================================================
# MASCOTES ORBIT
# =========================================================

with st.container(
    key="settings_pets",
):
    render_pet_preferences(
        st.session_state,
        user,
    )

# =========================================================
# COLUNAS PRINCIPAIS
# =========================================================

left, right = st.columns(2)

# =========================================================
# COLUNA ESQUERDA
# =========================================================

with left:
    with st.container(
        key="settings_appearance",
    ):
        render_card_title("APARÊNCIA")

        theme_options = (
            "Seguir sistema",
            "Claro",
            "Escuro",
        )

        theme = st.selectbox(
            "Tema do aplicativo",
            theme_options,
            index=theme_options.index(settings["theme"]),
            key=widget_key("theme"),
        )

        accent_names = tuple(ACCENT_COLORS.keys())

        accent = st.selectbox(
            "Cor de destaque",
            accent_names,
            index=(
                accent_names.index(settings["accent"])
                if settings["accent"] in accent_names
                else 0
            ),
            key=widget_key("accent"),
        )

        accent_hex = ACCENT_COLORS[accent]

        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                margin-top:-6px;
                margin-bottom:10px;
            ">
                <span style="
                    width:18px;
                    height:18px;
                    border-radius:50%;
                    background:{accent_hex};
                    border:2px solid rgba(255,255,255,.7);
                    box-shadow:0 0 0 1px rgba(100,100,120,.35);
                "></span>
                <small>Prévia: {accent}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

        compact_mode = st.toggle(
            "Modo compacto",
            value=settings["compact_mode"],
            key=widget_key("compact_mode"),
        )

        clear_column, dark_column = st.columns(2)

        with clear_column:
            st.button(
                "Visualizar tema claro",
                on_click=apply_theme,
                args=(False,),
                width="stretch",
            )

        with dark_column:
            st.button(
                "Visualizar tema escuro",
                on_click=apply_theme,
                args=(True,),
                width="stretch",
            )

    with st.container(
        key="settings_notifications",
    ):
        render_card_title("NOTIFICAÇÕES")

        task_reminders = st.toggle(
            "Lembretes de tarefas",
            value=settings["task_reminders"],
            key=widget_key("task_reminders"),
        )

        deadline_alerts = st.toggle(
            "Prazos próximos",
            value=settings["deadline_alerts"],
            key=widget_key("deadline_alerts"),
        )

        weekly_summary = st.toggle(
            "Resumo semanal",
            value=settings["weekly_summary"],
            key=widget_key("weekly_summary"),
        )

        smart_tips = st.toggle(
            "Dicas inteligentes",
            value=settings["smart_tips"],
            key=widget_key("smart_tips"),
        )

    with st.container(
        key="settings_ai",
    ):
        render_card_title("ASSISTENTE ORBIT AI")

        personalized_suggestions = st.toggle(
            "Sugestões personalizadas",
            value=settings["personalized_suggestions"],
            key=widget_key("personalized_suggestions"),
        )

        render_locked_setting(
            "Confirmação antes de agir",
            "Sempre ativa",
        )

        academic_history = st.toggle(
            "Usar histórico acadêmico",
            value=settings["academic_history"],
            key=widget_key("academic_history"),
        )

        st.caption(
            "A IA nunca altera tarefas ou dados sem sua confirmação."
        )

# =========================================================
# COLUNA DIREITA
# =========================================================

with right:
    with st.container(
        key="settings_language",
    ):
        render_card_title("IDIOMA E REGIÃO")

        languages = (
            "Português (Brasil)",
            "English (US)",
            "Español",
        )

        language = st.selectbox(
            "Idioma",
            languages,
            index=languages.index(settings["language"]),
            key=widget_key("language"),
        )

        date_formats = (
            "DD/MM/AAAA",
            "MM/DD/AAAA",
            "AAAA-MM-DD",
        )

        date_format = st.selectbox(
            "Formato de data",
            date_formats,
            index=date_formats.index(settings["date_format"]),
            key=widget_key("date_format"),
        )

        timezones = (
            "América/São Paulo",
            "UTC",
            "América/New York",
            "Europa/Lisboa",
        )

        timezone = st.selectbox(
            "Fuso horário",
            timezones,
            index=timezones.index(settings["timezone"]),
            key=widget_key("timezone"),
        )

    with st.container(
        key="settings_accessibility",
    ):
        render_card_title("ACESSIBILIDADE")

        text_sizes = (
            "Padrão",
            "Grande",
            "Muito grande",
        )

        text_size = st.selectbox(
            "Tamanho do texto",
            text_sizes,
            index=text_sizes.index(settings["text_size"]),
            key=widget_key("text_size"),
        )

        enhanced_contrast = st.toggle(
            "Contraste reforçado",
            value=settings["enhanced_contrast"],
            key=widget_key("enhanced_contrast"),
        )

        reduce_motion = st.toggle(
            "Reduzir animações",
            value=settings["reduce_motion"],
            key=widget_key("reduce_motion"),
        )

        render_locked_setting(
            "Navegação por teclado",
            "Ativada",
        )

    with st.container(
        key="settings_account",
    ):
        render_card_title("CONTA E DADOS")

        export_bytes = export_account_data(
            user,
            settings,
            subjects,
            tasks,
        )

        st.download_button(
            "Baixar meus dados",
            data=export_bytes,
            file_name="edutrack-meus-dados.json",
            mime="application/json",
            width="stretch",
        )

        account_columns = st.columns(2)

        with account_columns[0]:
            if st.button(
                "Gerenciar privacidade",
                width="stretch",
            ):
                st.session_state["settings_account_panel"] = "privacy"

        with account_columns[1]:
            if st.button(
                "Revisar dispositivos",
                width="stretch",
            ):
                st.session_state["settings_account_panel"] = "sessions"

        if st.button(
            "Excluir conta",
            key="settings_delete_account",
            width="stretch",
        ):
            st.session_state["settings_account_panel"] = "delete"

        panel = st.session_state.get("settings_account_panel")

        if panel == "privacy":
            st.info(
                "Privacidade: revise abaixo como o Orbit usa seus dados acadêmicos."
            )

            st.page_link(
                "pages/0_Privacidade.py",
                label="Abrir Política de Privacidade",
            )

            if st.button(
                "Fechar privacidade",
                key="close_settings_privacy",
            ):
                st.session_state["settings_account_panel"] = None
                st.rerun()

        elif panel == "sessions":
            st.info(
                "1 dispositivo ativo nesta sessão. Nenhuma outra sessão foi identificada."
            )

            if st.button(
                "Fechar dispositivos",
                key="close_settings_sessions",
            ):
                st.session_state["settings_account_panel"] = None
                st.rerun()

        elif panel == "delete":
            st.warning(
                "A exclusão de conta não será executada no protótipo."
            )

            st.caption(
                "Sua conta de teste continuará disponível."
            )

            if st.button(
                "Cancelar exclusão",
                key="cancel_settings_delete",
            ):
                st.session_state["settings_account_panel"] = None
                st.rerun()

# =========================================================
# DADOS QUE SERÃO SALVOS
# =========================================================

values = {
    "theme": theme,
    "accent": accent,
    "compact_mode": compact_mode,
    "task_reminders": task_reminders,
    "deadline_alerts": deadline_alerts,
    "weekly_summary": weekly_summary,
    "smart_tips": smart_tips,
    "personalized_suggestions": personalized_suggestions,
    "confirmation_before_action": True,
    "academic_history": academic_history,
    "language": language,
    "date_format": date_format,
    "timezone": timezone,
    "text_size": text_size,
    "enhanced_contrast": enhanced_contrast,
    "reduce_motion": reduce_motion,
    "keyboard_navigation": True,
}

# =========================================================
# SALVAR CONFIGURAÇÕES
# =========================================================

if st.button(
    "Salvar configurações",
    type="primary",
    key="save_settings",
    width="content",
):
    saved = save_settings(
        st.session_state,
        user,
        values,
    )

    st.session_state["edutrack_accent_name"] = saved["accent"]
    st.session_state["edutrack_accent_color"] = ACCENT_COLORS[
        saved["accent"]
    ]

    preferences = load_profile_section(
        st.session_state,
        user,
        "preferences",
        DEFAULT_PROFILE_PREFERENCES,
    )

    preferences["language"] = saved["language"]
    preferences["theme"] = saved["theme"]
    preferences["task_notifications"] = (
        "Ativadas"
        if saved["task_reminders"]
        else "Desativadas"
    )

    save_profile_section(
        st.session_state,
        user,
        "preferences",
        preferences,
    )

    if saved["theme"] in {
        "Claro",
        "Escuro",
    }:
        st.session_state["_settings_pending_theme"] = (
            saved["theme"] == "Escuro"
        )

    st.session_state["_settings_saved_notice"] = True
    st.rerun()
    