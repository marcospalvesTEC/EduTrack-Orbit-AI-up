"""Figma-aligned helpers for the desktop registration screen."""

from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st
from streamlit.errors import StreamlitPageNotFoundError

COURSE_OPTIONS = (
    "Selecione",
    "Ciência da Computação",
    "Sistemas de Informação",
    "Análise e Desenvolvimento de Sistemas",
    "Engenharia de Software",
    "Outro",
)


def safe(value: object) -> str:
    """Escape text rendered inside the registration HTML."""
    return escape(str(value), quote=True)


def password_strength(password: str) -> tuple[str, str]:
    """Return the visual password status and its semantic CSS class."""
    if not password:
        return "Crie uma senha", "empty"
    has_number = any(character.isdigit() for character in password)
    has_symbol = any(not character.isalnum() for character in password)
    if len(password) >= 8 and has_number and has_symbol:
        return "Senha forte", "strong"
    if len(password) >= 8:
        return "Senha média", "medium"
    return "Senha curta", "weak"


def install_registration_css() -> str:
    """Install the approved desktop styles and return the active theme class."""
    css = (Path(__file__).parent / "figma_registration.css").read_text(encoding="utf-8")
    theme_class = " orbit-registration-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme_class


def render_registration_brand(theme_class: str) -> None:
    """Render the Orbit brand and the visible page marker."""
    st.markdown(
        f"""
<div class="orbit-registration-page{theme_class}" aria-label="Cadastro do estudante">
  <a class="orbit-registration-brand" href="/" target="_self" aria-label="Voltar ao EduTrack Orbit AI">
    <span class="orbit-registration-mark" aria-hidden="true"><i></i></span>
    <strong>EduTrack<br><em>Orbit AI</em></strong>
  </a>
  <div class="orbit-registration-intro">
    <span>COMECE SUA JORNADA</span>
    <h1>Crie sua conta</h1>
    <p>Leva menos de dois minutos. Depois você personaliza o restante.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_strength(password: str) -> None:
    """Render the password requirements using the current field value."""
    label, status = password_strength(password)
    st.markdown(
        f"""
<div class="orbit-registration-strength {safe(status)}">
  <strong>●&nbsp; {safe(label)}</strong><span>8+ caracteres, número e símbolo</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_registration_visual() -> None:
    """Render the non-interactive right pane from the approved Figma frames."""
    st.markdown(
        """
<section class="orbit-registration-visual" aria-label="Etapas da jornada acadêmica">
  <span class="orbit-registration-eyebrow">✦&nbsp; SUA CONTA, SUA ÓRBITA</span>
  <h2>Organize desde o primeiro dia.<br>Evolua em cada entrega.</h2>
  <p>Crie seu perfil acadêmico e prepare uma jornada feita para você.</p>
  <div class="orbit-registration-orbit-card">
    <div class="orbit-registration-shape one"></div>
    <div class="orbit-registration-shape two"></div>
    <strong class="orbit-registration-step">01<br>perfil</strong>
    <div class="orbit-registration-steps">
      <span>1&nbsp; Crie seu perfil</span>
      <span>2&nbsp; Organize suas matérias</span>
      <span>3&nbsp; Evolua com o Orbit</span>
    </div>
  </div>
  <div class="orbit-registration-insight">✦&nbsp; Você configura o essencial agora e personaliza o restante depois.</div>
</section>
""",
        unsafe_allow_html=True,
    )


def render_registration_footer() -> None:
    """Render functional privacy, terms and brand actions in the footer."""
    with st.container(key="registration_footer"):
        privacy_column, terms_column, brand_column = st.columns([1, 1, 1.7])
        with privacy_column:
            try:
                st.page_link("pages/0_Privacidade.py", label="Política de Privacidade")
            except StreamlitPageNotFoundError:
                st.markdown("Política de Privacidade")
        with terms_column:
            try:
                st.page_link("pages/0_Termos.py", label="Termos de Uso")
            except StreamlitPageNotFoundError:
                st.markdown("Termos de Uso")
        with brand_column:
            st.markdown(
                '<a class="orbit-registration-footer-brand" href="/" target="_self">© 2026 EduTrack Orbit AI</a>',
                unsafe_allow_html=True,
            )
