"""Integration tests for the demonstration authentication UI."""

from pathlib import Path

from src.services.demo_auth import DEMO_EMAIL, DEMO_PASSWORD
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_demo_login_opens_authenticated_home():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15).run()

    assert not app.exception
    app.text_input[0].input(DEMO_EMAIL)
    app.text_input[1].input(DEMO_PASSWORD)
    app.button[0].click().run()

    assert not app.exception
    assert app.session_state["auth_current_user"]["email"] == DEMO_EMAIL
    assert any("Início do estudante" in item.value for item in app.markdown)
    assert not app.get("plotly_chart")


def test_dashboard_retains_analytics_separate_from_home():
    app = AppTest.from_file(PROJECT_ROOT / "pages/1_Dashboard.py", default_timeout=15)
    app.session_state["auth_current_user"] = {"name": "Estudante Demo", "email": DEMO_EMAIL}
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    app.run()

    assert not app.exception
    assert any("Dashboard de Desempenho" in item.value for item in app.markdown)
    assert len(app.get("plotly_chart")) == 2
    assert not any("Início do estudante" in item.value for item in app.markdown)


def test_protected_pages_stop_without_login():
    for path in [
        "pages/1_Dashboard.py",
        "pages/2_Disciplinas.py",
        "pages/3_Tarefas.py",
        "pages/4_Perfil.py",
    ]:
        app = AppTest.from_file(PROJECT_ROOT / path, default_timeout=15).run()

        assert not app.exception
        assert any("Faça login" in warning.value for warning in app.warning)


def test_protected_pages_render_with_authenticated_session():
    for path in [
        "pages/1_Dashboard.py",
        "pages/2_Disciplinas.py",
        "pages/3_Tarefas.py",
        "pages/4_Perfil.py",
    ]:
        app = AppTest.from_file(PROJECT_ROOT / path, default_timeout=15)
        app.session_state["auth_current_user"] = {
            "name": "Estudante Demo",
            "email": DEMO_EMAIL,
        }
        app.session_state["auth_demo_users"] = {}
        app.session_state["auth_recovery_email"] = None
        app.run()

        assert not app.exception
        assert any(button.label == "Sair" for button in app.button)


def test_new_account_home_starts_empty():
    """A newly registered user must not inherit the demonstration dataset."""
    email = "nova.conta@example.com"
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15)
    app.session_state["auth_current_user"] = {"name": "Nova Conta", "email": email}
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    app.run()

    assert not app.exception
    assert app.session_state[f"subjects:{email}"] == []
    assert app.session_state[f"tasks:{email}"] == []
    assert any("Sua conta está pronta" in info.value for info in app.info)


def test_profile_shows_account_without_exposing_password():
    """The profile displays public fields and never renders a stored password."""
    app = AppTest.from_file(PROJECT_ROOT / "pages/4_Perfil.py", default_timeout=15)
    app.session_state["auth_current_user"] = {
        "name": "Estudante Teste",
        "email": "estudante@example.com",
    }
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    app.run()

    assert not app.exception
    assert any("estudante@example.com" in metric.value for metric in app.metric)
    assert not any("password_hash" in markdown.value for markdown in app.markdown)


def test_xano_session_is_not_labeled_as_demonstration():
    """A user with a Xano token must be identified as a real account."""
    app = AppTest.from_file(PROJECT_ROOT / "pages/4_Perfil.py", default_timeout=15)
    app.session_state["auth_current_user"] = {
        "name": "Marcos Alves",
        "email": "marcos@example.com",
    }
    app.session_state["auth_token"] = "private-xano-token"
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    app.run()

    assert not app.exception
    assert any("Sua conta" in markdown.value for markdown in app.markdown)
    assert not any("Sessão demonstrativa" in markdown.value for markdown in app.markdown)
