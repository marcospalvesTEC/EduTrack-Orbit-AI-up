"""Tests for the Figma-aligned desktop password reset screen."""

from pathlib import Path

from src.core.auth_session import AUTH_USERS_KEY, RECOVERY_EMAIL_KEY
from src.ui.figma_password_reset import password_criteria
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_password_criteria_reports_each_rule():
    assert password_criteria("Senha@123") == {
        "length": True,
        "number": True,
        "symbol": True,
        "letter": True,
    }
    assert password_criteria("curta") == {
        "length": False,
        "number": False,
        "symbol": False,
        "letter": True,
    }


def test_password_reset_css_obeys_dark_mode_and_primary_button_rules():
    css = (PROJECT_ROOT / "src/ui/figma_password_reset.css").read_text(encoding="utf-8")

    assert "background-color: #111827 !important" in css
    assert "border-color: #f5f3ff !important" in css
    assert ".orbit-reset-dark" in css
    assert 'button[kind="primaryFormSubmit"]' in css
    assert "background: #7c3aed !important" in css
    assert "@media" not in css


def test_password_reset_page_renders_the_complete_desktop_form():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Redefinicao.py", default_timeout=15).run()

    assert not app.exception
    assert [field.label for field in app.text_input] == [
        "Nova senha",
        "Confirmar nova senha",
    ]
    labels = [button.label for button in app.button]
    assert "Salvar nova senha" in labels
    assert "Privacidade" in labels
    assert "Termos de uso" in labels


def test_password_reset_updates_demo_password_after_recovery():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Redefinicao.py", default_timeout=15)
    app.session_state[RECOVERY_EMAIL_KEY] = "demo@edutrack.ai"
    app.run()
    app.text_input[0].set_value("Nova@1234")
    app.text_input[1].set_value("Nova@1234")
    app.button[0].click().run()

    assert app.success[0].value == "Senha demonstrativa redefinida com sucesso."
    assert app.session_state[RECOVERY_EMAIL_KEY] is None
    assert AUTH_USERS_KEY in app.session_state
