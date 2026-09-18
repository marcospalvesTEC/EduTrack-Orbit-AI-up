"""Figma-aligned profile helpers for account data and preferences."""

from __future__ import annotations

import base64
from collections.abc import MutableMapping
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

from src.core.metrics import calculate_dashboard_metrics
from src.models.subject import Subject
from src.models.task import Task
from src.ui.figma_dashboard import icon

DEFAULT_PROFILE_DETAILS = {
    "course": "Não informado",
    "institution": "Não informada",
    "semester": "Não informado",
    "photo_data_url": "",
}
DEFAULT_PROFILE_PREFERENCES = {
    "weekly_goal": 18,
    "language": "Português (Brasil)",
    "theme": "Seguir sistema",
    "task_notifications": "Ativadas",
    "agenda_reminder": "30 min antes",
    "study_hours": 0,
}


def safe(value: object) -> str:
    """Escape a user-provided value before rendering it as HTML."""
    return escape(str(value), quote=True)


def profile_state_key(user: dict[str, str], section: str) -> str:
    """Return a stable user-scoped key for profile-only prototype data."""
    email = user.get("email", "anonymous").strip().lower()
    return f"profile:{section}:{email}"


def load_profile_section(
    state: MutableMapping[str, Any],
    user: dict[str, str],
    section: str,
    defaults: dict[str, Any],
) -> dict[str, Any]:
    """Load a profile section without sharing values between users."""
    key = profile_state_key(user, section)
    current = state.setdefault(key, dict(defaults))
    if not isinstance(current, dict):
        current = dict(defaults)
        state[key] = current
    return {**defaults, **current}


def save_profile_section(
    state: MutableMapping[str, Any],
    user: dict[str, str],
    section: str,
    values: dict[str, Any],
) -> None:
    """Persist one profile section in the current prototype session."""
    state[profile_state_key(user, section)] = dict(values)


def profile_photo_data_url(filename: str, content_type: str, content: bytes) -> str:
    """Validate an uploaded profile photo and return a safe embeddable data URL."""
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if content_type not in allowed_types:
        raise ValueError("Use uma imagem PNG, JPG, JPEG ou WebP.")
    if not content:
        raise ValueError("A imagem selecionada está vazia.")
    if len(content) > 5 * 1024 * 1024:
        raise ValueError("A foto deve ter no máximo 5 MB.")
    encoded = base64.b64encode(content).decode("ascii")
    return f"data:{content_type};base64,{encoded}"


def profile_metrics(
    tasks: list[Task], subjects: list[Subject], study_hours: int = 0
) -> dict[str, int]:
    """Return the three real values displayed in the profile summary."""
    metrics = calculate_dashboard_metrics(tasks, subjects)
    return {
        "completion_rate": round(float(metrics["completion_rate"])),
        "completed_tasks": int(metrics["completed_tasks"]),
        "study_hours": max(0, int(study_hours)),
    }


def render_profile_header(user: dict[str, str]) -> None:
    """Install profile CSS and render the approved desktop top bar."""
    css = (Path(__file__).parent / "figma_profile.css").read_text(encoding="utf-8")
    theme_class = " orbit-profile-dark" if st.session_state.get("edutrack_dark_mode") else ""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="orbit-profile-page{theme_class}" aria-label="Perfil do estudante">
  <header class="orbit-profile-topbar">
    <div class="orbit-profile-greeting"><h1>Boa noite, {first_name}</h1>
      <p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-profile-header-icons"><span class="orbit-profile-search">
      {icon("search", "")} Buscar...</span>
      <span class="orbit-profile-bell">{icon("bell", "Notificações")}</span></div>
  </header>
</div>
""",
        unsafe_allow_html=True,
    )


def render_profile_avatar(photo_data_url: str = "") -> None:
    """Render the saved profile photo or the purple prototype avatar."""
    avatar = (
        f'<img class="orbit-profile-avatar" src="{safe(photo_data_url)}" alt="Foto do perfil">'
        if photo_data_url.startswith("data:image/")
        else '<span class="orbit-profile-avatar" aria-hidden="true"></span>'
    )
    st.markdown(avatar, unsafe_allow_html=True)


def render_summary_card(metrics: dict[str, int]) -> None:
    """Render the student summary from actual academic data."""
    st.markdown(
        f"""
<div class="orbit-profile-card-copy orbit-profile-summary">
  <p class="orbit-profile-kicker">PERFIL DO ESTUDANTE</p>
  <p class="orbit-profile-account">Conta acadêmica ativa</p>
  <dl>
    <div><dt>{metrics["completion_rate"]}%</dt><dd>Progresso do semestre</dd></div>
    <div><dt>{metrics["completed_tasks"]}</dt><dd>Tarefas concluídas</dd></div>
    <div><dt>{metrics["study_hours"]} h</dt><dd>Tempo de estudo</dd></div>
  </dl>
</div>
""",
        unsafe_allow_html=True,
    )


def render_personal_data(user: dict[str, str], details: dict[str, Any]) -> None:
    """Render public account fields without exposing any credential data."""
    rows = (
        ("Nome", user.get("name", "Não informado")),
        ("E-mail", user.get("email", "Não informado")),
        ("Curso", details["course"]),
        ("Instituição", details["institution"]),
        ("Semestre atual", details["semester"]),
    )
    content = "".join(
        f"<div><dt>{safe(label)}</dt><dd>{safe(value)}</dd></div>" for label, value in rows
    )
    st.markdown(
        '<div class="orbit-profile-card-copy"><p class="orbit-profile-kicker">'
        f'DADOS PESSOAIS</p><dl class="orbit-profile-data">{content}</dl></div>',
        unsafe_allow_html=True,
    )


def render_preferences(preferences: dict[str, Any]) -> None:
    """Render the saved preference summary shown in the Figma card."""
    rows = (
        ("Meta semanal de estudos", f"{preferences['weekly_goal']} horas"),
        ("Idioma do aplicativo", preferences["language"]),
        ("Tema", preferences["theme"]),
        ("Notificações de tarefas", preferences["task_notifications"]),
        ("Lembretes da agenda", preferences["agenda_reminder"]),
    )
    content = "".join(
        f"<div><dt>{safe(label)}</dt><dd>{safe(value)}</dd></div>" for label, value in rows
    )
    st.markdown(
        '<div class="orbit-profile-card-copy"><p class="orbit-profile-kicker">'
        f'PREFERÊNCIAS ACADÊMICAS</p><dl class="orbit-profile-preferences">{content}</dl></div>',
        unsafe_allow_html=True,
    )


def render_security_summary() -> None:
    """Render only safe session metadata and the security status."""
    st.markdown(
        """
<div class="orbit-profile-card-copy"><p class="orbit-profile-kicker">SEGURANÇA</p>
  <dl class="orbit-profile-security">
    <div><dt>Senha</dt><dd>Protegida</dd></div>
    <div><dt>Autenticação</dt><dd>Sessão protegida</dd></div>
    <div><dt>Dispositivos</dt><dd>1 dispositivo ativo</dd></div>
  </dl>
</div>
""",
        unsafe_allow_html=True,
    )
