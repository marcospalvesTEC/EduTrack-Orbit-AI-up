"""Figma-aligned helpers for the desktop login screen."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def install_login_css() -> str:
    """Install the desktop login styles and return the active theme class."""
    css = (Path(__file__).parent / "figma_login.css").read_text(encoding="utf-8")
    theme_class = " orbit-login-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme_class


def render_login_brand(theme_class: str) -> None:
    """Render the product mark and login heading."""
    st.markdown(
        f"""
<div class="orbit-login-page{theme_class}" aria-label="Login do estudante">
  <a class="orbit-login-brand" href="/" target="_self" aria-label="EduTrack Orbit AI">
    <span class="orbit-login-mark" aria-hidden="true"><i></i></span>
    <strong>EduTrack<br><em>Orbit AI</em></strong>
  </a>
  <div class="orbit-login-intro">
    <span>ACESSO DO ESTUDANTE</span>
    <h1>Bem-vindo de volta</h1>
    <p>Entre para continuar organizando sua jornada acadêmica.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_login_visual() -> None:
    """Render the desktop visual pane without inventing student data."""
    st.markdown(
        """
<section class="orbit-login-visual" aria-label="Apresentação do EduTrack Orbit AI">
  <span class="orbit-login-eyebrow">✦&nbsp; SUA ROTINA, SUA ÓRBITA</span>
  <h2>Organize seus estudos.<br>Evolua em cada entrega.</h2>
  <p>Disciplinas, tarefas e agenda reunidas em uma experiência feita para você.</p>
  <div class="orbit-login-orbit-card" aria-hidden="true">
    <div class="orbit-login-ring ring-one"></div>
    <div class="orbit-login-ring ring-two"></div>
    <div class="orbit-login-core"><strong>ORBIT</strong><span>AI</span></div>
    <div class="orbit-login-preview">
      <span><i class="purple"></i> Organize</span>
      <span><i class="green"></i> Acompanhe</span>
      <span><i class="orange"></i> Evolua</span>
    </div>
  </div>
  <div class="orbit-login-insight">✦&nbsp; Seu planejamento acadêmico começa em um único lugar.</div>
</section>
""",
        unsafe_allow_html=True,
    )


def render_login_footer() -> None:
    """Render functional privacy, terms and brand actions."""
    with st.container(key="login_footer"):
        privacy_column, terms_column, brand_column = st.columns([1, 1, 1.7])
        with privacy_column:
            st.page_link("pages/0_Privacidade.py", label="Política de Privacidade")
        with terms_column:
            st.page_link("pages/0_Termos.py", label="Termos de Uso")
        with brand_column:
            st.markdown(
                '<a class="orbit-login-footer-brand" href="/" target="_self">© 2026 EduTrack Orbit AI</a>',
                unsafe_allow_html=True,
            )
