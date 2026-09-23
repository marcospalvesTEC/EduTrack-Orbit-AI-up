"""Desktop Orbit assistant aligned with the approved Figma frames."""

from datetime import date, datetime, time, timedelta

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.services.data_service import data_service_for_user, load_academic_data
from src.ui.figma_agenda import AgendaEvent, save_custom_event
from src.ui.figma_assistant import (
    SUGGESTED_PROMPTS,
    assistant_reply,
    conversation_key,
    install_assistant_css,
    pending_action_key,
    render_assistant_welcome,
    render_context,
    render_messages,
    render_pending_action,
)
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Assistente - EduTrack Orbit AI", page_icon="🤖", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)
service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)

messages_key = conversation_key(user)
action_key = pending_action_key(user)
messages = st.session_state.setdefault(messages_key, [])
st.session_state.setdefault(action_key, None)


def submit_prompt(prompt: str) -> None:
    """Append one user request and the deterministic Orbit answer."""
    clean_prompt = prompt.strip()
    if not clean_prompt:
        return
    answer, action = assistant_reply(clean_prompt, subjects, tasks)
    current = list(st.session_state.setdefault(messages_key, []))
    current.extend(
        [
            {"role": "user", "content": clean_prompt},
            {"role": "assistant", "content": answer},
        ]
    )
    st.session_state[messages_key] = current
    st.session_state[action_key] = action


install_assistant_css(user)

chat_column, context_column = st.columns([2.28, 1])
with chat_column:
    with st.container(key="assistant_chat"):
        render_assistant_welcome(user)
        render_messages(messages)

        pending_action = st.session_state.get(action_key)
        if isinstance(pending_action, dict):
            render_pending_action(pending_action)
            confirm_column, cancel_column, _ = st.columns([1, 1, 2])
            with confirm_column:
                if st.button("Confirmar", key="assistant_confirm_action", type="primary"):
                    tomorrow = date.today() + timedelta(days=1)
                    save_custom_event(
                        user,
                        AgendaEvent(
                            title=f"Sessão de foco — {pending_action['subject']}",
                            starts_at=datetime.combine(tomorrow, time(19, 0)),
                            category="Sessão de foco",
                            details=f"Planejada pelo Orbit · {pending_action['duration']} min",
                        ),
                    )
                    st.session_state[action_key] = None
                    st.session_state[messages_key] = [
                        *st.session_state[messages_key],
                        {
                            "role": "assistant",
                            "content": "Sessão de foco confirmada e adicionada à Agenda.",
                        },
                    ]
                    st.rerun()
            with cancel_column:
                if st.button("Cancelar", key="assistant_cancel_action"):
                    st.session_state[action_key] = None
                    st.rerun()

        st.markdown(
            "<h3 class='orbit-assistant-suggestions-title'>Sugestões rápidas</h3>",
            unsafe_allow_html=True,
        )
        suggestion_columns = st.columns(3)
        for column, suggestion in zip(suggestion_columns, SUGGESTED_PROMPTS):
            with column:
                if st.button(suggestion, key=f"assistant_suggestion_{suggestion}", type="tertiary"):
                    submit_prompt(suggestion)
                    st.rerun()

        with st.form("assistant_prompt_form", clear_on_submit=True):
            prompt_column, send_column = st.columns([6, 1])
            with prompt_column:
                prompt = st.text_input(
                    "Pergunte ao Orbit",
                    placeholder="Pergunte ao Orbit...",
                    label_visibility="collapsed",
                )
            with send_column:
                sent = st.form_submit_button("Enviar ➜", type="primary", width="stretch")
        if sent:
            submit_prompt(prompt)
            st.rerun()

with context_column:
    render_context(subjects)
