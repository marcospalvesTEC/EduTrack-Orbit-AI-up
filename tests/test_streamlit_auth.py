"""Integration tests for the demonstration authentication UI."""

from pathlib import Path

from src.services.demo_auth import DEMO_EMAIL, DEMO_PASSWORD
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_login_uses_dedicated_desktop_layout_without_tabs():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15).run()

    assert not app.exception
    assert not app.tabs
    assert any('aria-label="Login do estudante"' in item.value for item in app.markdown)
    assert {link.label for link in app.get("page_link")} >= {
        "Criar conta",
        "Esqueci minha senha",
    }


def test_login_dark_theme_keeps_dark_fields_with_light_borders():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15)
    app.session_state["edutrack_dark_mode"] = True
    app.run()

    assert not app.exception
    html = "\n".join(item.value for item in app.markdown)
    assert "orbit-login-dark" in html
    assert "border-color: #f5f3ff" in html
    assert "background: #111827" in html


def test_login_links_to_public_terms_and_privacy_pages():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15).run()

    assert not app.exception
    assert {link.label for link in app.get("page_link")} >= {
        "Política de Privacidade",
        "Termos de Uso",
    }

    for path, marker in [
        ("pages/0_Privacidade.py", "Política de Privacidade"),
        ("pages/0_Termos.py", "Termos de Uso"),
    ]:
        assert (PROJECT_ROOT / path).exists()
        legal_page = AppTest.from_file(PROJECT_ROOT / path, default_timeout=15).run()
        assert not legal_page.exception
        assert any(marker in item.value for item in legal_page.markdown)
        assert any("Voltar ao login" in item.value for item in legal_page.markdown)


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


def test_authenticated_sidebar_uses_the_shared_orbit_shell():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15)
    app.session_state["auth_current_user"] = {
        "name": "Estudante Demo",
        "email": DEMO_EMAIL,
    }
    app.session_state["auth_demo_users"] = {}
    app.session_state["auth_recovery_email"] = None
    app.run()

    assert not app.exception
    assert any(
        'aria-label="EduTrack Orbit AI"' in item.value
        and "Organize, acompanhe e evolua" in item.value
        for item in app.markdown
    )
    assert any(toggle.label == "Modo escuro" for toggle in app.toggle)
    assert {link.label for link in app.get("page_link")} >= {
        "Início",
        "Disciplinas",
        "Tarefas",
        "Agenda",
        "Relatórios",
        "Assistente",
        "Meu perfil",
        "Configurações",
    }
    assert any(expander.label == "Ferramentas de demonstração" for expander in app.expander)
    assert any(button.label == "Sair" for button in app.button)


def test_dashboard_page_and_navigation_entry_are_removed():
    assert not (PROJECT_ROOT / "pages/1_Dashboard.py").exists()
    sidebar_source = (PROJECT_ROOT / "src/core/auth_session.py").read_text(encoding="utf-8")
    assert 'label="Dashboard"' not in sidebar_source
    assert "pages/1_Dashboard.py" not in sidebar_source


def test_protected_pages_stop_without_login():
    for path in [
        "pages/2_Disciplinas.py",
        "pages/3_Tarefas.py",
        "pages/4_Agenda.py",
        "pages/4_Perfil.py",
        "pages/5_Relatorios.py",
        "pages/6_Assistente.py",
        "pages/7_Configuracoes.py",
    ]:
        app = AppTest.from_file(PROJECT_ROOT / path, default_timeout=15).run()

        assert not app.exception
        assert any("Faça login" in warning.value for warning in app.warning)


def test_protected_pages_render_with_authenticated_session():
    for path in [
        "pages/2_Disciplinas.py",
        "pages/3_Tarefas.py",
        "pages/4_Agenda.py",
        "pages/4_Perfil.py",
        "pages/5_Relatorios.py",
        "pages/6_Assistente.py",
        "pages/7_Configuracoes.py",
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
