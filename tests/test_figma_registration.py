"""Tests for the Figma-aligned desktop registration screen."""

from pathlib import Path

from src.ui.figma_registration import password_strength, safe
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_registration_helpers_escape_content_and_describe_password_strength():
    assert safe('<script>alert("x")</script>') == (
        "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;"
    )
    assert password_strength("") == ("Crie uma senha", "empty")
    assert password_strength("curta") == ("Senha curta", "weak")
    assert password_strength("oitoletras") == ("Senha média", "medium")
    assert password_strength("Senha@123") == ("Senha forte", "strong")


def test_registration_css_keeps_dark_fields_dark_with_light_borders():
    css = (PROJECT_ROOT / "src/ui/figma_registration.css").read_text(encoding="utf-8")

    assert "background-color: #111827 !important" in css
    assert "border-color: #f5f3ff !important" in css
    assert ".orbit-registration-dark" in css
    assert 'button[kind="primary"]' in css
    assert "background: #7c3aed !important" in css
    assert "gap: 18px !important" in css
    assert "border: 1px solid #e5e7eb !important" in css
    assert "@media" not in css


def test_registration_page_renders_the_complete_desktop_form():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Cadastro.py", default_timeout=15).run()

    assert not app.exception
    labels = [field.label for field in app.text_input]
    assert labels == [
        "Nome completo",
        "E-mail",
        "Instituição",
        "Senha",
        "Confirmar senha",
    ]
    assert app.selectbox[0].label == "Curso"
    assert app.checkbox[0].label.startswith("Li e aceito")
    assert any(button.label == "Criar conta" for button in app.button)
    footer_copy = "\n".join(item.value for item in app.markdown)
    assert "Política de Privacidade" in footer_copy
    assert "Termos de Uso" in footer_copy
