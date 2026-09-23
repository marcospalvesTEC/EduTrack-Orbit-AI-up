"""Shared authenticated sidebar aligned with the Orbit desktop shell."""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path

import streamlit as st

ASSETS = Path(__file__).parent / "assets"


def install_sidebar_css() -> None:
    """Install the shared light and dark sidebar presentation."""
    css = (Path(__file__).parent / "figma_sidebar.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_sidebar_brand() -> None:
    """Render the official Orbit logo and product promise."""
    encoded_logo = base64.b64encode((ASSETS / "orbit-logo.svg").read_bytes()).decode("ascii")
    st.markdown(
        f"""
<a class="orbit-shell-brand" href="/" target="_self" aria-label="EduTrack Orbit AI">
  <img src="data:image/svg+xml;base64,{encoded_logo}" alt="">
  <span><strong>EduTrack <em>Orbit AI</em></strong><small>Organize, acompanhe e evolua</small></span>
</a>
""",
        unsafe_allow_html=True,
    )


def render_sidebar_account(user: dict[str, str], account_label: str) -> None:
    """Render safe account data without exposing credentials or tokens."""
    st.markdown(
        f"""
<section class="orbit-shell-account" aria-label="Conta ativa">
  <div><small>{escape(account_label)}</small><strong>{escape(user["name"])}</strong>
  <a href="mailto:{escape(user["email"], quote=True)}">{escape(user["email"])}</a></div>
</section>
""",
        unsafe_allow_html=True,
    )
