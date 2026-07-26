from generator import generate_rota
from rota import validate_rota


def test_generated_rota_passes_validation():
    employees = ["Alice", "Ben", "Cara", "Dan"]
    days = ["Monday"]
    shifts = ["early", "late"]
    shift_hours = {"early": 8,"late": 10,}
    workload_limits = {
        "Alice": {"minimum": 8, "maximum": 10},
        "Ben": {"minimum": 8, "maximum": 10},
        "Cara": {"minimum": 8, "maximum": 10},
        "Dan": {"minimum": 8, "maximum": 10},
    }

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
        required_staff=2, #required_staff
        shift_hours=shift_hours,
        workload_limits=workload_limits
        )

    assert generated_assignments is not None

    violations = validate_rota(
        generated_assignments,
        employees,
        days,
        shifts,
        unavailable,
        shift_hours,
        workload_limits
    )

    assert violations == {
        "coverage": [],
        "employee_days": [],
        "availability": [],
        "workload": [],
    }


def test_impossible_rota_returns_none():
    employees = ["Alice"]
    days = ["Monday"]
    shifts = ["early", "late"]
    shift_hours = {"early": 8,"late": 10,}
    workload_limits = {
        "Alice": {"minimum": 8, "maximum": 10},
    }

    unavailable = {
        "Alice": set(),
    }

    generated_assignments = generate_rota(
        employees,
        days,
        shifts,
        unavailable,
        required_staff=2,
        shift_hours=shift_hours,
        workload_limits=workload_limits
    )

    assert generated_assignments is None