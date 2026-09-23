"""Public terms of use for EduTrack Orbit AI."""

import streamlit as st
from src.ui.figma_legal import render_legal_page
from src.ui.theme import inject_custom_css

st.set_page_config(
    page_title="Termos de Uso - EduTrack Orbit AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_custom_css()
render_legal_page("terms")
