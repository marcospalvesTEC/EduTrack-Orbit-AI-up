"""Shared presentation for the public legal pages."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from streamlit.errors import StreamlitPageNotFoundError

LEGAL_CONTENT = {
    "privacy": {
        "eyebrow": "TRANSPARÊNCIA E CONTROLE",
        "title": "Política de Privacidade",
        "description": "Como o EduTrack Orbit AI utiliza e protege os dados da experiência acadêmica.",
        "updated": "Atualizada em 24 de setembro de 2026",
        "sections": (
            (
                "1. Dados utilizados",
                "Podemos utilizar nome, e-mail, curso, instituição, preferências, foto de perfil, disciplinas, tarefas e eventos informados pelo estudante. A senha é tratada pelo fluxo de autenticação e nunca é exibida na interface.",
            ),
            (
                "2. Finalidade",
                "Os dados são usados para autenticar o acesso, organizar a rotina acadêmica, calcular indicadores, personalizar a experiência e permitir o funcionamento das páginas escolhidas pelo estudante.",
            ),
            (
                "3. Armazenamento",
                "No modo demonstrativo, as informações permanecem apenas na sessão do aplicativo. Quando a integração com o Xano estiver ativa, os dados serão enviados ao backend configurado para o projeto.",
            ),
            (
                "4. Compartilhamento",
                "O EduTrack Orbit AI não comercializa dados pessoais. Informações somente poderão ser processadas pelos serviços necessários ao funcionamento do aplicativo e conforme a configuração acadêmica do projeto.",
            ),
            (
                "5. Controle do estudante",
                "O estudante pode revisar dados do perfil, atualizar preferências, encerrar sessões e solicitar a correção ou exclusão das informações quando essas funções estiverem disponíveis no ambiente utilizado.",
            ),
            (
                "6. Segurança e contato",
                "Adotamos separação entre dados públicos da sessão e credenciais privadas. Em caso de dúvida, utilize o canal de suporte indicado no aplicativo ou procure a equipe responsável pelo projeto acadêmico.",
            ),
        ),
    },
    "terms": {
        "eyebrow": "USO RESPONSÁVEL",
        "title": "Termos de Uso",
        "description": "Regras essenciais para utilizar o EduTrack Orbit AI com segurança e responsabilidade.",
        "updated": "Atualizados em 24 de setembro de 2026",
        "sections": (
            (
                "1. Objetivo do aplicativo",
                "O EduTrack Orbit AI é um projeto acadêmico voltado à organização de disciplinas, tarefas, agenda, progresso e informações de estudo. Ele não substitui os sistemas oficiais da instituição de ensino.",
            ),
            (
                "2. Conta e acesso",
                "O estudante deve fornecer informações verdadeiras, manter suas credenciais protegidas e não compartilhar o acesso com terceiros. Atividades realizadas durante a sessão serão associadas à conta utilizada.",
            ),
            (
                "3. Uso adequado",
                "Não é permitido utilizar o aplicativo para atividades ilegais, tentar acessar dados de outras pessoas, explorar falhas de segurança ou prejudicar o funcionamento do serviço.",
            ),
            (
                "4. Assistente Orbit",
                "Sugestões produzidas pelo Assistente Orbit servem como apoio à organização acadêmica. Ações que alteram dados devem ser confirmadas pelo estudante, que continua responsável pelas decisões tomadas.",
            ),
            (
                "5. Disponibilidade",
                "Por se tratar de um projeto em evolução, páginas e recursos podem receber ajustes, ficar temporariamente indisponíveis ou utilizar dados demonstrativos durante testes e apresentações.",
            ),
            (
                "6. Atualizações dos termos",
                "Estes termos podem ser atualizados conforme o projeto evoluir. A data da versão vigente será informada nesta página para facilitar o acompanhamento das mudanças.",
            ),
        ),
    },
}


def install_legal_css() -> str:
    """Install shared legal-page styles and return the active theme class."""
    css = (Path(__file__).parent / "figma_legal.css").read_text(encoding="utf-8")
    theme_class = " orbit-legal-dark" if st.session_state.get("edutrack_dark_mode") else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme_class


def render_legal_page(kind: str) -> None:
    """Render one public legal document using the approved Orbit identity."""
    content = LEGAL_CONTENT[kind]
    theme_class = install_legal_css()
    sections = "".join(
        f"<section><h2>{title}</h2><p>{body}</p></section>" for title, body in content["sections"]
    )
    st.markdown(
        f"""
<main class="orbit-legal-page{theme_class}" aria-label="{content["title"]}">
  <header class="orbit-legal-header">
    <a class="orbit-legal-brand" href="/" target="_self" aria-label="EduTrack Orbit AI">
      <span class="orbit-legal-mark" aria-hidden="true"><i></i></span>
      <strong>EduTrack <em>Orbit AI</em></strong>
    </a>
    <span class="orbit-legal-eyebrow">{content["eyebrow"]}</span>
    <h1>{content["title"]}</h1>
    <p>{content["description"]}</p>
    <small>{content["updated"]}</small>
  </header>
  <article class="orbit-legal-document">
    <div class="orbit-legal-note">Documento informativo do protótipo acadêmico EduTrack Orbit AI.</div>
    {sections}
  </article>
</main>
""",
        unsafe_allow_html=True,
    )

    with st.container(key="legal_actions"):
        back_column, related_column = st.columns(2)
        with back_column:
            try:
                st.page_link("app.py", label="Voltar ao login", icon="↩️", width="stretch")
            except StreamlitPageNotFoundError:
                st.markdown("**Voltar ao login**")
        with related_column:
            related_path, related_label = (
                ("pages/0_Termos.py", "Ler Termos de Uso")
                if kind == "privacy"
                else ("pages/0_Privacidade.py", "Ler Política de Privacidade")
            )
            try:
                st.page_link(related_path, label=related_label, width="stretch")
            except StreamlitPageNotFoundError:
                st.markdown(f"**{related_label}**")
