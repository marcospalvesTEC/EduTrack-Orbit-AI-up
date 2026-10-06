"""Figma-aligned helpers for the desktop Orbit assistant screen."""

from __future__ import annotations


from textwrap import dedent
from html import escape
from pathlib import Path

import streamlit as st

from src.core.metrics import calculate_dashboard_metrics
from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.ui.figma_dashboard import icon

SUGGESTED_PROMPTS = (
    "Planejar minha semana",
    "Ver tarefas atrasadas",
    "Criar sessão de foco",
)


def safe(value: object) -> str:
    """Escape conversation and academic content before rendering HTML."""
    return escape(str(value), quote=True)


def conversation_key(user: dict[str, str]) -> str:
    """Return a user-scoped key for the demonstrative conversation."""
    return f"assistant_messages:{user.get('email', 'anonymous').strip().lower()}"


def pending_action_key(user: dict[str, str]) -> str:
    """Return a user-scoped key for actions awaiting confirmation."""
    return f"assistant_pending:{user.get('email', 'anonymous').strip().lower()}"


def assistant_reply(
    prompt: str, subjects: list[Subject], tasks: list[Task]
) -> tuple[str, dict[str, str] | None]:
    """Generate a safe deterministic answer using current academic data."""
    normalized = prompt.strip().lower()
    pending = sorted(
        (task for task in tasks if task.status != TaskStatus.CONCLUIDA),
        key=lambda task: (task.due_date, task.priority.value, task.title),
    )
    overdue = [task for task in pending if task.status == TaskStatus.ATRASADA or task.is_overdue]

    greetings = ("oi", "olá", "ola", "hey", "e aí", "eai", "bom dia", "boa tarde", "boa noite")
    if normalized in greetings or any(normalized.startswith(term + " ") for term in greetings):
        return (
            "Oi! 👋 Posso ajudar com tarefas, atrasos, progresso, planejamento da semana "
            "e sessões de foco. Experimente perguntar: “o que tenho hoje?”.",
            None,
        )

    if any(term in normalized for term in ("obrigado", "obrigada", "valeu", "vlw", "thanks")):
        return (
            "Por nada! Posso continuar daqui e te ajudar a escolher o próximo passo nos estudos.",
            None,
        )

    if any(
        term in normalized
        for term in ("o que você faz", "o que voce faz", "me ajuda", "ajuda", "help")
    ):
        return (
            "Posso priorizar tarefas, mostrar atrasos, resumir seu progresso, planejar a semana "
            "e preparar uma sessão de foco. Ações que alteram sua agenda pedem confirmação.",
            None,
        )

    if "hoje" in normalized or "o que tenho" in normalized:
        from datetime import date

        today_items = [task for task in pending if task.due_date == date.today()]
        if not today_items:
            return (
                "Hoje você não tem tarefas com vencimento marcado. "
                "Posso verificar atrasadas ou montar uma prioridade para a semana.",
                None,
            )
        items = "; ".join(f"{task.title} ({task.subject_name})" for task in today_items[:5])
        return f"Para hoje encontrei {len(today_items)} tarefa(s): {items}.", None

    if "foco" in normalized:
        subject = (
            pending[0].subject_name if pending else subjects[0].name if subjects else "Estudos"
        )
        return (
            f"Preparei uma sessão de foco de 45 minutos para {subject}. "
            "Confirme ou cancele na prévia da ação.",
            {"type": "focus", "subject": subject, "duration": "45"},
        )

    if "atras" in normalized:
        if not overdue:
            return "Você não possui tarefas atrasadas neste momento.", None
        items = "; ".join(f"{task.title} ({task.subject_name})" for task in overdue[:4])
        return f"Encontrei {len(overdue)} tarefa(s) atrasada(s): {items}.", None

    if "semana" in normalized or "planej" in normalized:
        if not pending:
            return "Sua semana está livre. Cadastre uma tarefa para montar o próximo plano.", None
        items = " ".join(
            f"{index}. {task.title} — {task.subject_name}."
            for index, task in enumerate(pending[:3], start=1)
        )
        return f"Minha recomendação para a semana: {items}", None

    if "prior" in normalized:
        if not pending:
            return (
                "Nenhuma tarefa pendente. Aproveite para revisar ou planejar a próxima semana.",
                None,
            )
        items = " ".join(
            f"{index}. {task.title}." for index, task in enumerate(pending[:3], start=1)
        )
        return f"Priorize nesta ordem: {items}", None

    if "desempenho" in normalized or "progresso" in normalized:
        metrics = calculate_dashboard_metrics(tasks, subjects)
        return (
            f"Seu progresso geral é de {metrics['completion_rate']:g}%, com "
            f"{metrics['completed_tasks']} tarefa(s) concluída(s) e "
            f"{metrics['overdue_tasks']} atrasada(s).",
            None,
        )

    if "criar tarefa" in normalized or "adicionar tarefa" in normalized:
        return (
            "Use o botão “Criar tarefa” em Ações rápidas para abrir o cadastro completo.",
            None,
        )

    if "evento" in normalized or "agenda" in normalized:
        return (
            "Use “Adicionar evento à agenda” em Ações rápidas para abrir o cadastro completo.",
            None,
        )

    return (
        "Entendi sua mensagem, mas este protótipo ainda não usa uma IA generativa externa. "
        "Posso responder sobre tarefas, atrasos, progresso, planejamento semanal e sessões de foco.",
        None,
    )


def install_assistant_css(user: dict[str, str]) -> None:
    """Install assistant styles and render the approved desktop header."""
    css = (Path(__file__).parent / "figma_assistant.css").read_text(encoding="utf-8")
    theme_class = " orbit-assistant-dark" if st.session_state.get("edutrack_dark_mode") else ""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(dedent(f"<style>{css}</style>"), unsafe_allow_html=True)
    st.markdown(
        dedent(f"""
<div class="orbit-assistant{theme_class}" aria-label="Assistente Orbit">
  <header class="orbit-assistant-topbar">
    <div><h1>Boa noite, {first_name}</h1><p>Organize, acompanhe e evolua</p></div>
    <div class="orbit-assistant-header-icons">
      <span class="orbit-assistant-search">{icon("search", "")} Buscar...</span>
      <span class="orbit-assistant-bell">{icon("bell", "Notificações")}</span>
    </div>
  </header>
  <div class="orbit-assistant-heading">
    <h2>Assistente <em>Orbit</em></h2>
    <p>Seu apoio inteligente para planejar, estudar e evoluir.</p>
  </div>
</div>
"""),
        unsafe_allow_html=True,
    )


def render_assistant_welcome(user: dict[str, str]) -> None:
    """Render the assistant status and initial explanation."""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(
        dedent(f"""
<div class="orbit-assistant-status">✦ Orbit online</div>
<div class="orbit-assistant-welcome">
  <strong>Olá, {first_name}! Como posso ajudar nos seus estudos hoje?</strong>
  <span>Posso analisar tarefas, sugerir um plano de estudo ou organizar sua agenda.<br>
  Sempre pedirei confirmação antes de alterar qualquer informação.</span>
</div>
"""),
        unsafe_allow_html=True,
    )


def render_messages(messages: list[dict[str, str]]) -> None:
    """Render the conversation history using the approved bubble hierarchy."""
    rows = "".join(
        f'<article class="orbit-assistant-message {safe(message.get("role", "assistant"))}">'
        f"{safe(message.get('content', ''))}</article>"
        for message in messages
    )
    st.markdown(dedent(f'<div class="orbit-assistant-messages">{rows}</div>'), unsafe_allow_html=True)


def render_context(subjects: list[Subject]) -> None:
    """Render the current academic context."""
    subject_rows = "".join(f"<li>{safe(subject.name)}</li>" for subject in subjects[:3])
    if not subject_rows:
        subject_rows = "<li>Nenhuma disciplina cadastrada</li>"
    st.markdown(
        dedent(f"""
<aside class="orbit-assistant-context">
  <h3>CONTEXTO ATUAL</h3><ul>{subject_rows}</ul>
</aside>
"""),
        unsafe_allow_html=True,
    )


def render_pending_action(action: dict[str, str]) -> None:
    """Render the action preview before the confirmation controls."""
    st.markdown(
        dedent(f"""
<div class="orbit-assistant-preview">
  <strong>Prévia da ação</strong>
  <span>Sessão de foco · {safe(action.get("subject", "Estudos"))} ·
    {safe(action.get("duration", "45"))} minutos</span>
  <small>Nenhuma informação foi alterada ainda.</small>
</div>
"""),
        unsafe_allow_html=True,
    )


def render_safety_note() -> None:
    """Render the assistant safety promise below native quick actions."""
    st.markdown(
        dedent("""
<div class="orbit-assistant-safety">
  <h3>ANTES DE EXECUTAR</h3>
  <p>O Orbit sempre mostrará uma prévia e pedirá sua confirmação antes de criar, editar ou excluir informações.</p>
</div>
"""),
        unsafe_allow_html=True,
    )
