"""Tests for the Figma-aligned desktop Settings screen."""

import json
from pathlib import Path

from src.models.subject import Subject
from src.services.demo_auth import DEMO_EMAIL
from src.ui.figma_settings import (
    DEFAULT_SETTINGS,
    export_account_data,
    load_settings,
    save_settings,
    settings_key,
)
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _authenticated_app() -> AppTest:
    app = AppTest.from_file(PROJECT_ROOT / "pages/7_Configuracoes.py", default_timeout=15)
    app.session_state["auth_current_user"] = {
        "name": "Estudante Demo",
        "email": DEMO_EMAIL,
    }
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    return app.run()


def test_settings_round_trip_is_user_scoped_and_keeps_safety_rules():
    user = {"email": "Aluno@Example.com"}
    state = {}
    values = load_settings(state, user)
    values["language"] = "Español"
    values["confirmation_before_action"] = False

    saved = save_settings(state, user, values)

    assert settings_key(user) == "settings:aluno@example.com"
    assert saved["language"] == "Español"
    assert saved["confirmation_before_action"] is True
    assert load_settings(state, user) == saved
    assert DEFAULT_SETTINGS["language"] == "Português (Brasil)"


def test_settings_export_contains_public_academic_data_without_credentials():
    user = {"name": "Estudante", "email": "estudante@example.com"}
    subject = Subject("Banco de Dados", "BD", "Prof.", 60)

    payload = json.loads(export_account_data(user, DEFAULT_SETTINGS, [subject], []).decode("utf-8"))

    assert payload["account"] == user
    assert payload["subjects"][0]["name"] == "Banco de Dados"
    assert "password" not in json.dumps(payload).lower()
    assert "token" not in json.dumps(payload).lower()


def test_settings_css_contains_both_desktop_themes_and_dark_fields():
    css = (PROJECT_ROOT / "src/ui/figma_settings.css").read_text(encoding="utf-8")

    assert ".orbit-settings-dark" in css
    assert "background: #7c3aed !important" in css
    assert "border-color: #f5f3ff !important" in css
    assert "@media" not in css


def test_settings_page_renders_actions_and_saves_profile_preferences():
    app = _authenticated_app()

    assert not app.exception
    assert any("Configurações" in item.value for item in app.markdown)
    assert any(button.label == "Baixar meus dados" for button in app.get("download_button"))
    assert any(button.label == "Gerenciar privacidade" for button in app.button)
    assert any(button.label == "Revisar dispositivos" for button in app.button)

    next(box for box in app.selectbox if box.label == "Tema do aplicativo").select("Escuro")
    next(box for box in app.selectbox if box.label == "Idioma").select("Español")
    next(button for button in app.button if button.label == "Salvar configurações").click().run()

    assert not app.exception
    saved = app.session_state[f"settings:{DEMO_EMAIL}"]
    profile = app.session_state[f"profile:preferences:{DEMO_EMAIL}"]
    assert saved["theme"] == "Escuro"
    assert saved["language"] == "Español"
    assert profile["theme"] == "Escuro"
    assert profile["language"] == "Español"
    assert app.session_state["edutrack_dark_mode"] is True
