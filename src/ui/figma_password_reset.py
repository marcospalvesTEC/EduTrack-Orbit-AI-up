"""Figma-aligned helpers for the desktop password reset screen."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def password_criteria(password: str) -> dict[str, bool]:
    """Return the password rules displayed by the reset screen."""
    return {
        "length": len(password) >= 8,
        "number": any(character.isdigit() for character in password),
        "symbol": any(not character.isalnum() for character in password),
        "letter": any(character.isalpha() for character in password),
    }


def install_password_reset_css() -> str:
    """Install desktop reset styles and return the active theme class."""
    css = (Path(__file__).parent / "figma_password_reset.css").read_text(encoding="utf-8")
    theme_class = " orbit-reset-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme_class


def render_reset_brand(theme_class: str) -> None:
    """Render the clickable Orbit brand and reset introduction."""
    st.markdown(
        f"""
<div class="orbit-reset-page{theme_class}" aria-label="Redefinição de senha">
  <a class="orbit-reset-brand" href="/" target="_self" aria-label="Voltar ao EduTrack Orbit AI">
    <span class="orbit-reset-mark" aria-hidden="true"><i></i></span>
    <strong>EduTrack<br><em>Orbit AI</em></strong>
  </a>
  <div class="orbit-reset-intro">
    <span>NOVA SENHA</span>
    <h1>Proteja sua conta</h1>
    <p>Crie uma senha nova e diferente das utilizadas anteriormente.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_password_criteria(password: str) -> None:
    """Render live password criteria without exposing the supplied password."""
    criteria = password_criteria(password)
    strong = all(criteria.values())
    status = "Senha forte" if strong else "Crie uma senha forte"
    css_class = "strong" if strong else "pending"

    def marker(rule: str) -> str:
        return "✓" if criteria[rule] else "○"

    st.markdown(
        f"""
<div class="orbit-reset-criteria {css_class}">
  <strong>●&nbsp; {status}</strong>
  <span>{marker("length")}&nbsp; 8 ou mais caracteres&nbsp;&nbsp;&nbsp;
    {marker("number")}&nbsp; número&nbsp;&nbsp;&nbsp;
    {marker("symbol")}&nbsp; símbolo&nbsp;&nbsp;&nbsp;
    {marker("letter")}&nbsp; letras</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_secure_session() -> None:
    """Render the temporary-session message from the Figma frame."""
    st.markdown(
        '<div class="orbit-reset-session">◷&nbsp; Sessão segura — link válido por mais 22 minutos</div>',
        unsafe_allow_html=True,
    )


def render_reset_visual() -> None:
    """Render the explanatory right pane from the approved desktop frames."""
    st.markdown(
        """
<section class="orbit-reset-visual" aria-label="Proteção da nova senha">
  <span class="orbit-reset-eyebrow">✦&nbsp; UMA NOVA CAMADA DE PROTEÇÃO</span>
  <h2>Sua nova senha protege<br>toda a sua jornada.</h2>
  <p>Confirme os critérios e retome seus estudos com segurança.</p>
  <div class="orbit-reset-orbit-card">
    <div class="orbit-reset-shape one"></div>
    <div class="orbit-reset-shape two"></div>
    <strong class="orbit-reset-step">◆<br><span>nova<br>senha</span></strong>
    <div class="orbit-reset-steps">
      <span>1&nbsp; Crie a senha</span>
      <span>2&nbsp; Confirme os critérios</span>
      <span>3&nbsp; Volte ao Login</span>
    </div>
  </div>
  <div class="orbit-reset-insight">✦&nbsp; Depois de salvar, o link será invalidado automaticamente.</div>
</section>
""",
        unsafe_allow_html=True,
    )


@st.dialog("Política de Privacidade")
def _render_privacy_dialog() -> None:
    st.markdown(
        "A senha é processada somente para atualizar a autenticação. Ela não é exibida nem "
        "armazenada em texto puro."
    )


@st.dialog("Termos de Uso")
def _render_terms_dialog() -> None:
    st.markdown(
        "A redefinição deve ser realizada somente pelo titular da conta utilizando uma sessão "
        "de recuperação válida."
    )


def render_reset_footer() -> None:
    """Render functional privacy, terms and brand actions."""
    with st.container(key="reset_footer"):
        privacy_column, terms_column, brand_column = st.columns([1, 1, 1.7])
        with privacy_column:
            if st.button("Privacidade", key="open_reset_privacy", type="tertiary"):
                _render_privacy_dialog()
        with terms_column:
            if st.button("Termos de uso", key="open_reset_terms", type="tertiary"):
                _render_terms_dialog()
        with brand_column:
            st.markdown(
                '<a class="orbit-reset-footer-brand" href="/" target="_self">© 2026 EduTrack Orbit AI</a>',
                unsafe_allow_html=True,
            )
