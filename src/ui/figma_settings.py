"""Figma-aligned helpers for the desktop Settings screen."""

from __future__ import annotations

import json
from collections.abc import MutableMapping
from copy import deepcopy
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

from src.models.subject import Subject
from src.models.task import Task
from src.ui.figma_dashboard import icon

from src.ui.pets import (
    PET_PROFILES,
    PETS,
    load_pet_choice,
    save_pet_choice,
)
DEFAULT_SETTINGS: dict[str, Any] = {
    "theme": "Seguir sistema",
    "accent": "Roxo Orbit",
    "compact_mode": False,
    "task_reminders": True,
    "deadline_alerts": True,
    "weekly_summary": True,
    "smart_tips": False,
    "personalized_suggestions": True,
    "confirmation_before_action": True,
    "academic_history": True,
    "language": "Português (Brasil)",
    "date_format": "DD/MM/AAAA",
    "timezone": "América/São Paulo",
    "text_size": "Padrão",
    "enhanced_contrast": False,
    "reduce_motion": False,
    "keyboard_navigation": True,
}
ACCENT_COLORS = {
    "Roxo Orbit": "#7C3AED",
    "Azul Nebulosa": "#2563EB",
    "Verde Aurora": "#10B981",
    "Laranja Solar": "#F59E0B",
    "Rosa Pulsar": "#DB2777",
}

PET_SCREEN_LABELS = {
    "home": "Início",
    "disciplinas": "Disciplinas",
    "tarefas": "Tarefas",
    "agenda": "Agenda",
    "relatorios": "Relatórios",
    "assistente": "Assistente",
    "perfil": "Perfil",
    "configuracoes": "Configurações",
}

def safe(value: object) -> str:
    """Escape user-controlled values before including them in HTML."""
    return escape(str(value), quote=True)


def settings_key(user: dict[str, str]) -> str:
    """Return a user-scoped key for Settings data."""
    return f"settings:{user.get('email', 'anonymous').strip().lower()}"


def load_settings(state: MutableMapping[str, Any], user: dict[str, str]) -> dict[str, Any]:
    """Load a complete copy of the user's settings."""
    saved = state.get(settings_key(user), {})
    values = deepcopy(DEFAULT_SETTINGS)
    if isinstance(saved, dict):
        values.update(saved)
    return values


def save_settings(
    state: MutableMapping[str, Any], user: dict[str, str], values: dict[str, Any]
) -> dict[str, Any]:
    """Persist a normalized, user-scoped Settings snapshot."""
    normalized = deepcopy(DEFAULT_SETTINGS)
    normalized.update({key: values[key] for key in normalized if key in values})
    normalized["confirmation_before_action"] = True
    normalized["keyboard_navigation"] = True
    state[settings_key(user)] = normalized
    return deepcopy(normalized)


def export_account_data(
    user: dict[str, str],
    settings: dict[str, Any],
    subjects: list[Subject],
    tasks: list[Task],
) -> bytes:
    """Build a portable JSON export without credentials or session tokens."""
    payload = {
        "account": {"name": user.get("name", ""), "email": user.get("email", "")},
        "settings": settings,
        "subjects": [subject.to_dict() for subject in subjects],
        "tasks": [task.to_dict() for task in tasks],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def install_settings_css(user: dict[str, str]) -> None:
    """Install Settings styles and render the approved desktop header."""
    css = (Path(__file__).parent / "figma_settings.css").read_text(encoding="utf-8")
    theme_class = " orbit-settings-dark" if st.session_state.get("edutrack_dark_mode") else ""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="orbit-settings{theme_class}" aria-label="Configurações">
  <header class="orbit-settings-topbar">
    <div><h1>Boa noite, {first_name}</h1><p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-settings-header-icons">
      <span class="orbit-settings-search">{icon("search", "")} Buscar...</span>
      <span class="orbit-settings-bell">{icon("bell", "Notificações")}</span>
    </div>
  </header>
  <div class="orbit-settings-heading">
    <h2>Configurações</h2>
    <p>Personalize sua experiência, privacidade e preferências do Orbit.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_card_title(title: str) -> None:
    """Render one Figma-style card label."""
    st.markdown(f'<h3 class="orbit-settings-card-title">{safe(title)}</h3>', unsafe_allow_html=True)


def render_locked_setting(label: str, value: str, active: bool = True) -> None:
    """Render a non-editable safety or capability setting."""
    status_class = " active" if active else ""
    st.markdown(
        f'<div class="orbit-settings-locked"><span>{safe(label)}</span>'
        f'<strong class="{status_class.strip()}">{"●" if active else "○"} {safe(value)}</strong></div>',
        unsafe_allow_html=True,
    )
def render_pet_preferences(
    state: MutableMapping[str, Any],
    user: dict[str, Any],
) -> None:
    """Renderiza o seletor de mascote por tela."""

    render_card_title("Mascote Orbit")

    st.caption(
        "Escolha qual mascote acompanhará você em cada área do EduTrack."
    )

    screen_key = st.selectbox(
        "Tela",
        options=list(PET_SCREEN_LABELS.keys()),
        format_func=lambda value: PET_SCREEN_LABELS[value],
        key="orbit_pet_settings_screen",
    )

    current_pet = load_pet_choice(
        state=state,
        user=user,
        screen_key=screen_key,
    )

    if current_pet not in PETS:
        current_pet = "axolote"

    pet_keys = list(PETS.keys())

    selected_pet = st.selectbox(
        "Mascote",
        options=pet_keys,
        index=pet_keys.index(current_pet),
        format_func=lambda value: PET_PROFILES[value]["name"],
        key=f"orbit_pet_settings_pet_{screen_key}",
    )

    profile = PET_PROFILES[selected_pet]

    st.markdown(
        f"""
        **{profile["name"]}**  
        {profile["role"]}

        {profile["description"]}
        """
    )

    if st.button(
        "Salvar mascote",
        type="primary",
        key=f"save_pet_{screen_key}",
    ):
        try:
            save_pet_choice(
                state=state,
                user=user,
                pet=selected_pet,
                screen_key=screen_key,
            )

            st.success(
                f"{profile['name']} definido para "
                f"{PET_SCREEN_LABELS[screen_key]}."
            )

        except Exception as error:
            st.error(
                f"Não foi possível salvar o mascote: {error}"
            )