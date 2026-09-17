"""Tests for the Figma-aligned tasks board helpers."""

from datetime import date

from src.models.task import Task, TaskPriority, TaskStatus
from src.ui.figma_tasks import board_status, filter_tasks


def make_task(
    title: str,
    *,
    status: TaskStatus = TaskStatus.PENDENTE,
    priority: TaskPriority = TaskPriority.MEDIA,
) -> Task:
    return Task(
        title=title,
        subject_id="subject-1",
        subject_name="Banco de Dados",
        due_date=date(2026, 9, 20),
        status=status,
        priority=priority,
        description="Projeto acadêmico",
    )


def test_board_status_groups_pending_and_overdue_as_todo():
    assert board_status(make_task("Pendente")) == "A fazer"
    assert board_status(make_task("Atrasada", status=TaskStatus.ATRASADA)) == "A fazer"
    assert (
        board_status(make_task("Andamento", status=TaskStatus.EM_ANDAMENTO))
        == "Em andamento"
    )
    assert board_status(make_task("Feita", status=TaskStatus.CONCLUIDA)) == "Concluídas"


def test_filter_tasks_matches_text_status_and_priority():
    pending = make_task("Normalização", priority=TaskPriority.ALTA)
    doing = make_task("Diagrama", status=TaskStatus.EM_ANDAMENTO)
    tasks = [pending, doing]

    assert filter_tasks(tasks, query="banco") == tasks
    assert filter_tasks(tasks, query="normal") == [pending]
    assert filter_tasks(tasks, status="Em andamento") == [doing]
    assert filter_tasks(tasks, priority="Alta") == [pending]
