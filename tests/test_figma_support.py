"""Tests for the public desktop support and contact flow."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_support_page_renders_public_contact_form_and_faq():
    support_page = PROJECT_ROOT / "pages/0_Suporte.py"

    assert support_page.exists()
    app = AppTest.from_file(support_page, default_timeout=15).run()

    assert not app.exception
    assert any('aria-label="Suporte do EduTrack Orbit AI"' in item.value for item in app.markdown)
    assert {field.label for field in app.text_input} >= {"Nome", "E-mail", "Assunto"}
    assert any(field.label == "Descrição" for field in app.text_area)
    assert any(field.label == "Categoria" for field in app.selectbox)
    assert any(button.label == "Enviar solicitação" for button in app.button)
    assert len(app.expander) >= 3


def test_support_submission_is_validated_and_remains_demonstrative():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Suporte.py", default_timeout=15).run()

    submit = next(button for button in app.button if button.label == "Enviar solicitação")
    submit.click().run()
    assert any("Informe um e-mail válido" in warning.value for warning in app.warning)

    next(field for field in app.text_input if field.label == "Nome").input("Marcos Alves")
    next(field for field in app.text_input if field.label == "E-mail").input("marcos@example.com")
    next(field for field in app.text_input if field.label == "Assunto").input(
        "Dúvida sobre minha conta"
    )
    next(field for field in app.text_area if field.label == "Descrição").input(
        "Preciso de ajuda para revisar meu acesso ao aplicativo."
    )
    submit = next(button for button in app.button if button.label == "Enviar solicitação")
    submit.click().run()

    assert not app.exception
    assert any("Nenhuma mensagem externa foi enviada" in item.value for item in app.success)


def test_support_dark_theme_keeps_dark_fields_and_light_borders():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Suporte.py", default_timeout=15)
    app.session_state["edutrack_dark_mode"] = True
    app.run()

    assert not app.exception
    html = "\n".join(item.value for item in app.markdown)
    assert "orbit-support-dark" in html
    assert "background: #111827" in html
    assert "border-color: #f5f3ff" in html


def test_recovery_links_to_the_public_support_page():
    app = AppTest.from_file(PROJECT_ROOT / "pages/0_Recuperacao.py", default_timeout=15).run()

    assert not app.exception
    support_links = [link for link in app.get("page_link") if link.label == "Falar com o suporte"]
    support_fallback = any(
        'href="/Suporte"' in item.value and "Falar com o suporte" in item.value
        for item in app.markdown
    )
    assert support_links or support_fallback
