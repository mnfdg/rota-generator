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
    max_consecutive_days = {
        "Alice": 5,
        "Ben": 5,
        "Cara": 5,
        "Dan": 5,
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
        workload_limits=workload_limits,
        max_consecutive_days=max_consecutive_days,
        )

    assert generated_assignments is not None

    violations = validate_rota(
        generated_assignments,
        employees,
        days,
        shifts,
        unavailable,
        shift_hours,
        workload_limits,
        max_consecutive_days,
    )

    assert violations == {
        "coverage": [],
        "employee_days": [],
        "availability": [],
        "workload": [],
        "working_runs": [],
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
    max_consecutive_days = {"Alice":3,}

    generated_assignments = generate_rota(
        employees,
        days,
        shifts,
        unavailable,
        required_staff=2,
        shift_hours=shift_hours,
        workload_limits=workload_limits,
        max_consecutive_days=max_consecutive_days,
    )

    assert generated_assignments is None

def test_impossible_consecutive_days_returns_none():
    employees = ["Alice"]
    days = ["Monday", "Tuesday", "Wednesday"]
    shifts = ["early"]

    unavailable = {
        "Alice": set(),
    }

    shift_hours = {
        "early": 8,
    }

    workload_limits = {
        "Alice": {"minimum": 0, "maximum": 24},
    }

    max_consecutive_days = {
        "Alice": 2,
    }

    generated_assignments = generate_rota(
        employees,
        days,
        shifts,
        unavailable,
        required_staff=1,
        shift_hours=shift_hours,
        workload_limits=workload_limits,
        max_consecutive_days=max_consecutive_days,
    )

    assert generated_assignments is None