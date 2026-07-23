from rota import (
    check_assignment_availability,
    check_coverage,
    count_assignments,
    count_employee_day_assignments,
    find_employee_day_violations,
    validate_rota,
)

def test_count_assignments():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Ben", "Monday", "early"),
        ("Cara", "Monday", "late"),
    ]

    assert count_assignments(
        assignments,
        "Monday",
        "early",
    ) == 2

    assert count_assignments(
        assignments,
        "Monday",
        "late",
    ) == 1

def test_correct_coverage_has_no_violation():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Ben", "Monday", "early"),
    ]

    result = check_coverage(
        assignments,
        "Monday",
        "early",
    )

    assert result is None

def test_incorrect_coverage_returns_violation():
    assignments = [
        ("Alice", "Monday", "early"),
    ]

    result = check_coverage(
        assignments,
        "Monday",
        "early",
    )

    assert result == (
        "Monday early requires 2 employees but has 1."
    )

def test_count_employee_day_assignments():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Alice", "Monday", "late"),
        ("Alice", "Tuesday", "early"),
    ]

    assert count_employee_day_assignments(
        assignments,
        "Alice",
        "Monday",
    ) == 2

def test_multiple_shifts_on_one_day_returns_violation():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Alice", "Monday", "late"),
    ]

    result = find_employee_day_violations(
        assignments,
        ["Alice"],
        ["Monday"],
    )

    assert result == [
        "Alice is assigned to 2 shifts on Monday"
    ]

def test_unavailable_assignment_returns_violation():
    assignment = ("Dan", "Monday", "late")
    unavailable = {
        "Dan": {"Monday"},
    }

    result = check_assignment_availability(
        assignment,
        unavailable,
    )

    assert result == (
        "Dan is unavailable on Monday "
        "but is assigned to the late shift."
    )

def test_valid_rota_has_no_violations():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Ben", "Monday", "early"),
        ("Cara", "Monday", "late"),
        ("Dan", "Monday", "late"),
    ]

    employees = ["Alice", "Ben", "Cara", "Dan"]
    days = ["Monday"]
    shifts = ["early", "late"]

    unavailable = {
        "Alice": set(),
        "Ben": set(),
        "Cara": set(),
        "Dan": set(),
    }

    result = validate_rota(
        assignments,
        employees,
        days,
        shifts,
        unavailable,
    )

    assert result == {
        "coverage": [],
        "employee_days": [],
        "availability": [],
    }
