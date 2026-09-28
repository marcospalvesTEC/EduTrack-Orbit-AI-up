"""Figma-aligned helpers for the desktop Orbit assistant screen."""

from __future__ import annotations

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
    """Generate a safe, deterministic answer using the current academic data."""
    normalized = prompt.strip().lower()
    pending = sorted(
        (task for task in tasks if task.status != TaskStatus.CONCLUIDA),
        key=lambda task: (task.due_date, task.priority.value, task.title),
    )
    overdue = [task for task in pending if task.status == TaskStatus.ATRASADA or task.is_overdue]

    if "foco" in normalized:
        subject = (
            pending[0].subject_name if pending else subjects[0].name if subjects else "Estudos"
        )
        return (
            f"Preparei uma sessão de foco de 45 minutos para {subject}. "
            "Confira a prévia e confirme antes de adicioná-la à Agenda.",
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
    if "prior" in normalized or "hoje" in normalized:
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
            "Posso preparar a tarefa, mas preciso do título, da disciplina e do prazo. "
            "Nada será criado sem sua confirmação.",
            None,
        )
    if "evento" in normalized or "agenda" in normalized:
        return (
            "Posso preparar um evento. Informe o título, a data e o horário; mostrarei uma "
            "prévia antes de adicionar à Agenda.",
            None,
        )
    return (
        "Posso ajudar a priorizar tarefas, planejar sua semana, resumir seu desempenho ou "
        "preparar uma sessão de foco.",
        None,
    )


def install_assistant_css(user: dict[str, str]) -> None:
    """Install assistant styles and render the approved desktop header."""
    css = (Path(__file__).parent / "figma_assistant.css").read_text(encoding="utf-8")
    theme_class = " orbit-assistant-dark" if st.session_state.get("edutrack_dark_mode") else ""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
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
""",
        unsafe_allow_html=True,
    )


def render_assistant_welcome(user: dict[str, str]) -> None:
    """Render the assistant status and initial explanation."""
    first_name = safe(user.get("name", "Estudante").split()[0])
    st.markdown(
        f"""
<div class="orbit-assistant-status">✦ Orbit online</div>
<div class="orbit-assistant-welcome">
  <strong>Olá, {first_name}! Como posso ajudar nos seus estudos hoje?</strong>
  <span>Posso analisar tarefas, sugerir um plano de estudo ou organizar sua agenda.<br>
  Sempre pedirei confirmação antes de alterar qualquer informação.</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_messages(messages: list[dict[str, str]]) -> None:
    """Render the conversation history using the approved bubble hierarchy."""
    rows = "".join(
        f'<article class="orbit-assistant-message {safe(message.get("role", "assistant"))}">'
        f"{safe(message.get('content', ''))}</article>"
        for message in messages
    )
    st.markdown(f'<div class="orbit-assistant-messages">{rows}</div>', unsafe_allow_html=True)


def render_context(subjects: list[Subject]) -> None:
    """Render current context, quick actions and the safety promise."""
    subject_rows = "".join(f"<li>{safe(subject.name)}</li>" for subject in subjects[:3])
    if not subject_rows:
        subject_rows = "<li>Nenhuma disciplina cadastrada</li>"
    st.markdown(
        f"""
<aside class="orbit-assistant-context">
  <h3>CONTEXTO ATUAL</h3><ul>{subject_rows}</ul>
  <h3>AÇÕES RÁPIDAS</h3>
  <ul><li>Criar tarefa</li><li>Planejar sessão de foco</li>
    <li>Adicionar evento à agenda</li><li>Resumir desempenho</li></ul>
  <h3>ANTES DE EXECUTAR</h3>
  <p>O Orbit sempre mostrará uma prévia e pedirá sua confirmação antes de criar, editar ou excluir informações.</p>
</aside>
""",
        unsafe_allow_html=True,
    )


def render_pending_action(action: dict[str, str]) -> None:
    """Render the action preview before the confirmation controls."""
    st.markdown(
        f"""
<div class="orbit-assistant-preview">
  <strong>Prévia da ação</strong>
  <span>Sessão de foco · {safe(action.get("subject", "Estudos"))} ·
    {safe(action.get("duration", "45"))} minutos</span>
  <small>Nenhuma informação foi alterada ainda.</small>
</div>
""",
        unsafe_allow_html=True,
    )
