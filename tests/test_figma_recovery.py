"""Tests for the Figma-aligned desktop password recovery screen."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_recovery_css_obeys_light_and_dark_field_rules():
    css = (PROJECT_ROOT / "src/ui/figma_recovery.css").read_text(encoding="utf-8")

    assert "background-color: #111827 !important" in css
    assert "border-color: #f5f3ff !important" in css
    assert ".orbit-recovery-dark" in css
    assert 'button[kind="primary"]' in css
    assert 'button[kind="primaryFormSubmit"]' in css
    assert '[data-testid="stFormSubmitButton"] button' in css
    assert "background: #7c3aed !important" in css
    assert ".st-key-recovery_support { margin-top: 18px; }" in css
    assert "border: 1px solid #e5e7eb !important" in css
    assert "@media" not in css


def test_recovery_page_renders_complete_desktop_flow():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Recuperacao.py", default_timeout=15).run()

    assert not app.exception
    assert [field.label for field in app.text_input] == ["E-mail"]
    labels = [button.label for button in app.button]
    assert "Enviar link de recuperação" in labels
    assert "Privacidade" in labels
    assert "Termos de uso" in labels
    support_links = [link.label for link in app.get("page_link")]
    support_fallback = any(
        'href="/Suporte"' in item.value and "Falar com o suporte" in item.value
        for item in app.markdown
    )
    assert "Falar com o suporte" in support_links or support_fallback


def test_recovery_response_is_neutral_for_known_and_unknown_accounts():
    known = AppTest.from_file(PROJECT_ROOT / "pages/0_Recuperacao.py", default_timeout=15).run()
    known.text_input[0].set_value("demo@edutrack.ai")
    known.button[0].click().run()

    unknown = AppTest.from_file(PROJECT_ROOT / "pages/0_Recuperacao.py", default_timeout=15).run()
    unknown.text_input[0].set_value("nao-existe@exemplo.com")
    unknown.button[0].click().run()

    assert known.success[0].value == unknown.success[0].value
