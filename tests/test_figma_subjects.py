"""Tests for the Figma-aligned subjects overview helpers."""

from datetime import date, timedelta

from src.models.subject import Subject
from src.ui.figma_subjects import filter_subjects, safe_color, weekly_workload


def test_filter_subjects_matches_name_code_and_professor():
    subjects = [
        Subject(name="Banco de Dados", code="BD", professor="Prof. Ana", workload_hours=40),
        Subject(name="Algoritmos", code="ALG", professor="Prof. Carlos", workload_hours=80),
    ]

    assert filter_subjects(subjects, "banco") == [subjects[0]]
    assert filter_subjects(subjects, "alg") == [subjects[1]]
    assert filter_subjects(subjects, "ana") == [subjects[0]]
    assert filter_subjects(subjects, "") == subjects


def test_weekly_workload_uses_subject_period():
    subject = Subject(
        name="Banco de Dados",
        code="BD",
        professor="Prof. Ana",
        workload_hours=40,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=70),
    )

    assert weekly_workload([subject]) == 4


def test_subject_color_only_accepts_safe_hex_values():
    assert safe_color("#7C3AED") == "#7C3AED"
    assert safe_color("#fff; background:url(bad)") == "#7c3aed"
