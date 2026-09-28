"""Tests for the Figma-aligned profile helpers."""

from datetime import date
from pathlib import Path

from src.models.subject import Subject
from src.models.task import Task, TaskStatus
from src.ui.figma_profile import (
    DEFAULT_PROFILE_PREFERENCES,
    load_profile_section,
    profile_metrics,
    profile_photo_data_url,
    profile_state_key,
    safe,
    save_profile_section,
)


def test_profile_state_is_scoped_by_normalized_email():
    user = {"name": "Marcos", "email": " MARCOS@Example.com "}

    assert profile_state_key(user, "preferences") == "profile:preferences:marcos@example.com"


def test_profile_preferences_round_trip_without_mutating_defaults():
    state = {}
    user = {"name": "Marcos", "email": "marcos@example.com"}
    values = load_profile_section(state, user, "preferences", DEFAULT_PROFILE_PREFERENCES)
    values["weekly_goal"] = 24
    save_profile_section(state, user, "preferences", values)

    loaded = load_profile_section(state, user, "preferences", DEFAULT_PROFILE_PREFERENCES)

    assert loaded["weekly_goal"] == 24
    assert DEFAULT_PROFILE_PREFERENCES["weekly_goal"] == 18


def test_profile_metrics_use_actual_tasks_and_safe_study_time():
    subjects = [
        Subject(
            id="s1",
            name="Algoritmos",
            code="CC1",
            professor="Prof. Carlos",
            workload_hours=80,
        )
    ]
    tasks = [
        Task(
            id="t1",
            title="Feita",
            subject_id="s1",
            subject_name="Algoritmos",
            due_date=date(2026, 9, 18),
            status=TaskStatus.CONCLUIDA,
        ),
        Task(
            id="t2",
            title="Pendente",
            subject_id="s1",
            subject_name="Algoritmos",
            due_date=date(2026, 9, 19),
        ),
    ]

    assert profile_metrics(tasks, subjects, -5) == {
        "completion_rate": 50,
        "completed_tasks": 1,
        "study_hours": 0,
    }


def test_profile_escapes_values_and_keeps_desktop_dark_fields_dark():
    css = (Path(__file__).parents[1] / "src/ui/figma_profile.css").read_text(encoding="utf-8")
    compact_css = " ".join(css.split())
    page = (Path(__file__).parents[1] / "pages/4_Perfil.py").read_text(encoding="utf-8")

    assert safe('<script>alert("x")</script>') == (
        "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;"
    )
    assert "background-color: #121525 !important" in css
    assert "border-color: #f5f3ff !important" in css
    assert ".st-key-profile_dialog_panel" in css
    assert '[data-testid="stWidgetLabel"] *' in css
    assert ".st-key-profile_dialog_close button" in css
    assert "background: #7c3aed !important" in css
    assert "flex-wrap: nowrap !important" in css
    assert "justify-content: space-between" in css
    assert "flex: 0 0 calc(50% - 6px) !important" in css
    assert (
        'grid-template-areas: "intro intro" "personal summary" '
        '"preferences preferences" "security security"' in compact_css
    )
    assert "@media (max-width: 768px)" not in css
    assert '"Alterar foto do perfil"' not in page
    assert '"Editar informações do perfil"' not in page


def test_profile_photo_is_validated_and_encoded_as_data_url():
    result = profile_photo_data_url("avatar.png", "image/png", b"profile-photo")

    assert result == "data:image/png;base64,cHJvZmlsZS1waG90bw=="


def test_profile_photo_rejects_unsupported_content_type():
    try:
        profile_photo_data_url("avatar.svg", "image/svg+xml", b"<svg></svg>")
    except ValueError as error:
        assert "PNG, JPG, JPEG ou WebP" in str(error)
    else:
        raise AssertionError("unsupported profile photo must be rejected")
