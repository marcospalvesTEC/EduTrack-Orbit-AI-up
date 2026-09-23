"""Presentation helpers for the public desktop support page."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from streamlit.errors import StreamlitPageNotFoundError

SUPPORT_CATEGORIES = (
    "Acesso e senha",
    "Disciplinas",
    "Tarefas",
    "Agenda",
    "Perfil",
    "Outro assunto",
)


def install_support_css() -> str:
    """Install support styles and return the active theme class."""
    css = (Path(__file__).parent / "figma_support.css").read_text(encoding="utf-8")
    theme_class = " orbit-support-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme_class


def render_support_header(theme_class: str) -> None:
    """Render the Orbit brand and support introduction."""
    st.markdown(
        f"""
<div class="orbit-support-page{theme_class}" aria-label="Suporte do EduTrack Orbit AI">
  <a class="orbit-support-brand" href="/" target="_self" aria-label="EduTrack Orbit AI">
    <span class="orbit-support-mark" aria-hidden="true"><i></i></span>
    <strong>EduTrack<br><em>Orbit AI</em></strong>
  </a>
  <div class="orbit-support-intro">
    <span>CENTRAL DE AJUDA</span>
    <h1>Como podemos ajudar?</h1>
    <p>Descreva sua dúvida com clareza. Nunca envie sua senha, código de acesso ou token.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_support_sidebar() -> None:
    """Render frequently asked questions and safe public shortcuts."""
    st.markdown(
        """
<section class="orbit-support-aside" aria-label="Ajuda rápida">
  <span>✦&nbsp; AJUDA RÁPIDA</span>
  <h2>Talvez sua resposta<br>já esteja aqui.</h2>
  <p>Consulte as dúvidas frequentes ou acesse diretamente uma opção segura.</p>
</section>
""",
        unsafe_allow_html=True,
    )
    with st.container(key="support_faq"):
        with st.expander("Não consigo entrar na minha conta"):
            st.write(
                "Confirme o e-mail digitado e use a recuperação de senha. "
                "A resposta nunca revela se uma conta existe."
            )
        with st.expander("Meus dados ficam salvos no modo demonstrativo?"):
            st.write(
                "No modo demonstrativo, alterações permanecem somente na sessão atual "
                "e não substituem os dados do Xano."
            )
        with st.expander("Como informar um erro?"):
            st.write(
                "Selecione a área relacionada, descreva o que aconteceu e informe a ação "
                "realizada antes do erro, sem incluir credenciais."
            )

    st.markdown(
        '<p class="orbit-support-shortcuts-title">ATALHOS SEGUROS</p>', unsafe_allow_html=True
    )
    with st.container(key="support_shortcuts"):
        links = (
            ("pages/0_Recuperacao.py", "Recuperar minha senha", "🔐"),
            ("pages/0_Termos.py", "Termos de Uso", "📄"),
            ("pages/0_Privacidade.py", "Política de Privacidade", "🛡️"),
        )
        for path, label, icon in links:
            try:
                st.page_link(path, label=label, icon=icon, width="stretch")
            except StreamlitPageNotFoundError:
                st.markdown(f"**{label}**")


def render_support_footer() -> None:
    """Render a public return path and the product signature."""
    with st.container(key="support_footer"):
        back_column, brand_column = st.columns([1, 1.7])
        with back_column:
            try:
                st.page_link("app.py", label="←  Voltar ao login")
            except StreamlitPageNotFoundError:
                st.markdown("←  Voltar ao login")
        with brand_column:
            st.markdown(
                '<span class="orbit-support-footer-brand">© 2026 EduTrack Orbit AI</span>',
                unsafe_allow_html=True,
            )


def is_valid_support_email(email: str) -> bool:
    """Apply the small local validation needed by the demonstrative form."""
    normalized = email.strip()
    local, separator, domain = normalized.partition("@")
    return bool(local and separator and "." in domain and not domain.startswith("."))
