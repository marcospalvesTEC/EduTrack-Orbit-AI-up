"""Session helpers and route protection for demonstration authentication."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

AUTH_USERS_KEY = "auth_demo_users"
AUTH_USER_KEY = "auth_current_user"
AUTH_TOKEN_KEY = "auth_token"
RECOVERY_EMAIL_KEY = "auth_recovery_email"


def initialize_auth_state(state: MutableMapping[str, Any]) -> None:
    """Initialize all authentication keys without overwriting active state."""
    state.setdefault(AUTH_USERS_KEY, {})
    state.setdefault(AUTH_USER_KEY, None)
    state.setdefault(AUTH_TOKEN_KEY, None)
    state.setdefault(RECOVERY_EMAIL_KEY, None)


def current_user(state: MutableMapping[str, Any]) -> dict[str, str] | None:
    """Return the current public user, if authenticated."""
    initialize_auth_state(state)
    user = state.get(AUTH_USER_KEY)
    return user if isinstance(user, dict) else None


def sign_in(
    state: MutableMapping[str, Any], user: dict[str, Any], token: str | None = None
) -> None:
    """Store a public authenticated user in session state."""
    initialize_auth_state(state)
    state[AUTH_USER_KEY] = dict(user)
    state[AUTH_TOKEN_KEY] = token
    state[RECOVERY_EMAIL_KEY] = None


def sign_out(state: MutableMapping[str, Any]) -> None:
    """Clear authentication and recovery state while preserving local accounts."""
    initialize_auth_state(state)
    state[AUTH_USER_KEY] = None
    state[AUTH_TOKEN_KEY] = None
    state[RECOVERY_EMAIL_KEY] = None


def update_current_user_name(state: MutableMapping[str, Any], name: str) -> dict[str, str] | None:
    """Update the visible name in both the session and local account record."""
    user = current_user(state)
    clean_name = name.strip()
    if user is None or not clean_name:
        return None
    email = user["email"]
    user["name"] = clean_name
    state[AUTH_USER_KEY] = user
    record = state[AUTH_USERS_KEY].get(email)
    if isinstance(record, dict):
        record["name"] = clean_name
    return user


def require_authenticated() -> dict[str, str]:
    """Stop a Streamlit page before protected data is rendered."""
    import streamlit as st

    user = current_user(st.session_state)
    if user is None:
        st.warning("Faça login na página inicial para acessar esta área.")
        st.info("Use a página inicial no menu lateral para entrar.")
        st.stop()
    return user


def render_session_sidebar(user: dict[str, str]) -> None:
    """Render app navigation, current-user context and logout action."""
    import streamlit as st
    from streamlit.errors import StreamlitPageNotFoundError

    def page_link(path: str, label: str, icon: str) -> None:
        """Render a link while allowing pages to run independently in tests."""
        try:
            st.page_link(path, label=label, icon=icon)
        except StreamlitPageNotFoundError:
            st.markdown(f"{icon} {label}")

    with st.sidebar:
        st.markdown("### Navegação")
        page_link("app.py", label="Início", icon="🏠")
        page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
        page_link("pages/2_Disciplinas.py", label="Disciplinas", icon="📚")
        page_link("pages/3_Tarefas.py", label="Tarefas", icon="✅")
        page_link("pages/4_Agenda.py", label="Agenda", icon="📅")
        page_link("pages/4_Perfil.py", label="Meu perfil", icon="👤")
        st.divider()
        account_label = (
            "Sua conta" if st.session_state.get(AUTH_TOKEN_KEY) else "Sessão demonstrativa"
        )
        st.markdown(f"### 👤 {account_label}")
        st.markdown(f"**{user['name']}**")
        st.caption(user["email"])
        if st.button("Sair", width="stretch", key="auth_logout"):
            sign_out(st.session_state)
            st.switch_page("app.py")
        st.divider()
