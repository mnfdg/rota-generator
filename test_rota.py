from rota import (
    check_assignment_availability,
    check_coverage,
    count_assignments,
    count_employee_day_assignments,
    find_employee_day_violations,
    calculate_employee_hours,
    check_employee_workload,
    find_workload_violations,
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

    shift_hours = {
        "early": 8,
        "late": 10,
        #"long day": 10,
    }   

    workload_limits = {
        "Alice": {"minimum": 8, "maximum": 10},
        "Ben": {"minimum": 8, "maximum": 10},
        "Cara": {"minimum": 8, "maximum": 10},
        "Dan": {"minimum": 8, "maximum": 10},
    }


    result = validate_rota(
        assignments,
        employees,
        days,
        shifts,
        unavailable,
        shift_hours,
        workload_limits
    )

    assert result == {
        "coverage": [],
        "employee_days": [],
        "availability": [],
        "workload": [],
    }


def test_calculate_employee_hours():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Alice", "Tuesday", "late"),
        ("Ben", "Monday", "early"),
    ]

    shift_hours = {
        "early": 8,
        "late": 10,
    }

    result = calculate_employee_hours(
        assignments,
        "Alice",
        shift_hours,
    )

    assert result == 18

def test_workload_in_permitted_range_returns_None():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Alice", "Tuesday", "late"),
        ("Ben", "Monday", "early"),
    ]

    shift_hours = {
        "early": 8,
        "late": 10,
    }

    workload_limits = {
        "Alice": {"minimum": 16, "maximum": 20},
    }

    result = check_employee_workload(
        assignments,
        "Alice",
        shift_hours,
        workload_limits
    )

    assert result == None



def test_workload_below_permitted_range_returns_violation():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Ben", "Monday", "early"),
    ]

    shift_hours = {
        "early": 8,
        "late": 10,
    }

    workload_limits = {
        "Alice": {"minimum": 16, "maximum": 20},
    }

    result = check_employee_workload(
        assignments,
        "Alice",
        shift_hours,
        workload_limits
    )

    assert result == "Alice should work at least 16 hours but is working only 8 hours."



def test_workload_above_permitted_range_returns_violation():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Alice", "Tuesday", "early"),
        ("Alice", "Wednesday", "late"),
        ("Ben", "Monday", "early"),
    ]

    shift_hours = {
        "early": 8,
        "late": 10,
    }

    workload_limits = {
        "Alice": {"minimum": 16, "maximum": 20},
    }

    result = check_employee_workload(
        assignments,
        "Alice",
        shift_hours,
        workload_limits
    )

    assert result == "Alice should work at most 20 hours but is working 26 hours."


def test_find_workload_violations():
    assignments = [
        ("Alice", "Monday", "early"),
        ("Ben", "Monday", "early"),
        ("Ben", "Tuesday", "late"),
        ("Cara", "Monday", "late"),
        ("Cara", "Tuesday", "late"),
        ("Cara", "Wednesday", "late"),
    ]

    employees = ["Alice", "Ben", "Cara"]

    shift_hours = {
        "early": 8,
        "late": 10,
    }

    workload_limits = {
        "Alice": {"minimum": 16, "maximum": 20},
        "Ben": {"minimum": 16, "maximum": 20},
        "Cara": {"minimum": 16, "maximum": 20},
    }

    result = find_workload_violations(
        assignments,
        employees,
        shift_hours,
        workload_limits,
    )

    assert result == [
        "Alice should work at least 16 hours but is working only 8 hours.",
        "Cara should work at most 20 hours but is working 30 hours."
    ]