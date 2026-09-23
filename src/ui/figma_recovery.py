"""Figma-aligned helpers for the desktop password recovery screen."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def install_recovery_css() -> str:
    """Install desktop recovery styles and return the active theme class."""
    css = (Path(__file__).parent / "figma_recovery.css").read_text(encoding="utf-8")
    theme_class = " orbit-recovery-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme_class


def render_recovery_brand(theme_class: str) -> None:
    """Render the clickable Orbit brand and recovery introduction."""
    st.markdown(
        f"""
<div class="orbit-recovery-page{theme_class}" aria-label="Recuperação de senha">
  <a class="orbit-recovery-brand" href="/" target="_self" aria-label="Voltar ao EduTrack Orbit AI">
    <span class="orbit-recovery-mark" aria-hidden="true"><i></i></span>
    <strong>EduTrack<br><em>Orbit AI</em></strong>
  </a>
  <div class="orbit-recovery-intro">
    <span>RECUPERAÇÃO DE ACESSO</span>
    <h1>Esqueceu sua senha?</h1>
    <p>Informe o e-mail da sua conta. Enviaremos um link seguro para você criar uma nova senha.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_secure_link_notice() -> None:
    """Explain the recovery-link behavior shown in the approved frame."""
    st.markdown(
        """
<div class="orbit-recovery-link-notice">
  <strong>◇&nbsp; Link temporário e protegido</strong>
  <span>Ele expira em 30 minutos e pode ser utilizado apenas uma vez.</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_recovery_visual() -> None:
    """Render the explanatory right pane from the approved desktop frames."""
    st.markdown(
        """
<section class="orbit-recovery-visual" aria-label="Etapas da recuperação de senha">
  <span class="orbit-recovery-eyebrow">✦&nbsp; RECUPERE COM SEGURANÇA</span>
  <h2>Volte à sua jornada<br>com tranquilidade.</h2>
  <p>Um processo simples, protegido e sem revelar sua senha atual.</p>
  <div class="orbit-recovery-orbit-card">
    <div class="orbit-recovery-shape one"></div>
    <div class="orbit-recovery-shape two"></div>
    <strong class="orbit-recovery-step">✉<br><span>link seguro</span></strong>
    <div class="orbit-recovery-steps">
      <span>1&nbsp; Informe o e-mail</span>
      <span>2&nbsp; Receba o link</span>
      <span>3&nbsp; Crie nova senha</span>
    </div>
  </div>
  <div class="orbit-recovery-insight">✦&nbsp; Por segurança, o link expira em 30 minutos.</div>
</section>
""",
        unsafe_allow_html=True,
    )


@st.dialog("Política de Privacidade")
def _render_privacy_dialog() -> None:
    st.markdown(
        "O e-mail informado é utilizado somente para localizar a conta e iniciar a recuperação "
        "de acesso. A resposta não confirma se existe uma conta cadastrada."
    )


@st.dialog("Termos de Uso")
def _render_terms_dialog() -> None:
    st.markdown(
        "O link de recuperação é pessoal, temporário e deve ser utilizado somente pelo titular "
        "da conta EduTrack Orbit AI."
    )


@st.dialog("Suporte")
def render_support_dialog() -> None:
    """Show a safe support path without exposing account existence."""
    st.markdown(
        "Se você não reconhece o e-mail ou não consegue recuperar o acesso, procure o responsável "
        "pelo projeto e informe apenas seu nome e instituição. Nunca envie sua senha."
    )


def render_recovery_footer() -> None:
    """Render functional privacy, terms and brand actions."""
    with st.container(key="recovery_footer"):
        privacy_column, terms_column, brand_column = st.columns([1, 1, 1.7])
        with privacy_column:
            if st.button("Privacidade", key="open_recovery_privacy", type="tertiary"):
                _render_privacy_dialog()
        with terms_column:
            if st.button("Termos de uso", key="open_recovery_terms", type="tertiary"):
                _render_terms_dialog()
        with brand_column:
            st.markdown(
                '<a class="orbit-recovery-footer-brand" href="/" target="_self">© 2026 EduTrack Orbit AI</a>',
                unsafe_allow_html=True,
            )
