from generator import generate_rota
from rota import validate_rota


def test_generated_rota_passes_validation():
    employees = ["Alice", "Ben", "Cara", "Dan"]
    days = ["Monday"]
    shifts = ["early", "late"]

    unavailable = {
        "Alice": set(),
        "Ben": set(),
        "Cara": set(),
        "Dan": set(),
    }

    generated_assignments = generate_rota(
        employees,
        days,
        shifts,
        unavailable,
        required_staff=2,
    )

    assert generated_assignments is not None

    violations = validate_rota(
        generated_assignments,
        employees,
        days,
        shifts,
        unavailable,
    )

    assert violations == {
        "coverage": [],
        "employee_days": [],
        "availability": [],
    }


def test_impossible_rota_returns_none():
    employees = ["Alice"]
    days = ["Monday"]
    shifts = ["early", "late"]

    unavailable = {
        "Alice": set(),
    }

    generated_assignments = generate_rota(
        employees,
        days,
        shifts,
        unavailable,
        required_staff=2,
    )

    assert generated_assignments is None