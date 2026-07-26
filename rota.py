employees = [
    "Alice",
    "Ben",
    "Cara",
    "Dan",
    "Eve",
    "Frank",
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

shifts = [
    "early",
    "late",
    #"long day",
]

shift_hours = {
    "early": 8,
    "late": 10,
    #"long day": 10,
}

# Record "unavailable" days, as these should be fewer than "available" days.
unavailable = {
    "Alice": {"Wednesday"},
    "Ben": {"Friday"},
    "Cara": set(), # an empty set
    "Dan": {"Monday"},
    "Eve": {"Saturday", "Sunday"},
    "Frank": set(),
}

workload_limits = {
    "Alice": {"minimum": 32, "maximum": 50},
    "Ben": {"minimum": 32, "maximum": 50},
    "Cara": {"minimum": 32, "maximum": 50},
    "Dan": {"minimum": 32, "maximum": 50},
    "Eve": {"minimum": 32, "maximum": 50},
    "Frank": {"minimum": 32, "maximum": 50},
}

assignments = [
    ("Alice", "Monday", "early"),
    ("Ben", "Monday", "early"),
    ("Cara", "Monday", "late"),
    ("Eve", "Monday", "late"),
    ("Alice", "Monday", "late"),
    ("Dan", "Monday", "late"),
    ("Eve", "Saturday", "late"),
]

REQUIRED_STAFF = 2

# Functions to check shift staff numbers
def count_assignments(assignments, target_day, target_shift) -> int:
    """Count staff assigned to a given shift on a given day."""

    count = 0
    for _, day, shift in assignments:
        if day == target_day and shift == target_shift:
            count += 1
    return count

def check_coverage(assignments, target_day, target_shift) -> str | None:
    """Return a warning if staff numbers for a given shift on a given day differ
    from the required number."""

    assigned_staff = count_assignments(assignments, target_day, target_shift)
    if assigned_staff != REQUIRED_STAFF:
        return (
            f"{target_day} {target_shift} requires "
            f"{REQUIRED_STAFF} employees but has {assigned_staff}."
        )
    return

def find_coverage_violations(assignments, days, shifts) -> list:
    """Return a list of shifts where staff numbers differ from required 
    numbers."""

    violations = []
    for day in days:
        for shift in shifts:
            violation = check_coverage(assignments, day, shift)
            if violation:
                violations.append(violation)
    return violations

# Functions to check staff are not assigned multiple shifts on one day
def count_employee_day_assignments(
        assignments, target_employee, target_day) -> int:
    """Return number of shifts assigned to a given employee on a given day."""
    count = 0
    for assignment in assignments:
        if assignment[0] == target_employee and assignment[1] == target_day:
            count += 1
    return count

def find_employee_day_violations(assignments, employees, days) -> list:
    """Return list of warnings where staff are assigned multiple shifts on
    the same day."""
    violations = []

    for employee in employees:
        for day in days:
            count = count_employee_day_assignments(
                assignments, employee, day
                )
            
            if count > 1:
                violation = (
                    f"{employee} is assigned to {count} shifts on {day}"
                )
                violations.append(violation)
                    
    return violations

# Functions to check staff unavailability is accounted for
def check_assignment_availability(assignment, unavailable) -> str | None:
    """Return a warning if a given assignment is on one of the staff member's 
    unavailable days."""
    employee, day, shift = assignment

    if day in unavailable[employee]:
        return (
            f"{employee} is unavailable on {day} but is assigned to the {shift}"
            f" shift."
        )
    return None

def find_availability_violations(assignments, unavailable) -> list:
    """Takes a list of assignments and a dictionary of staff members'
    unavailable days, returns a list of warnings for assignments where someone
    has been assigned to a day they are not available."""
    violations = []
    for assignment in assignments:
        violation = check_assignment_availability(assignment, unavailable)
        if violation:
            violations.append(violation)
    return violations


# Functions to check if employees are rota'd an appropriate number of hours
def calculate_employee_hours(
    assignments,
    target_employee,
    shift_hours,
):
    total_hours = 0

    for employee, _, shift in assignments:
        if employee == target_employee:
            total_hours += shift_hours[shift]

    return total_hours

def check_employee_workload(
    assignments,
    target_employee,
    shift_hours,
    workload_limits,
):
    assigned_hours = calculate_employee_hours(
        assignments,
        target_employee,
        shift_hours,
    )

    minimum_hours = workload_limits[target_employee]["minimum"]
    maximum_hours = workload_limits[target_employee]["maximum"]

    # Return a violation if assigned_hours is below the minimum.
    if assigned_hours < minimum_hours:
        violation = f"{target_employee} should work at least {minimum_hours}"\
            f" hours but is working only {assigned_hours} hours."
        return violation
    # Return a different violation if it is above the maximum.
    if assigned_hours > maximum_hours:
        violation = f"{target_employee} should work at most {maximum_hours}"\
            f" hours but is working {assigned_hours} hours."
        return violation
    # Otherwise return None
    return None

def find_workload_violations(
        assignments,
        employees,
        shift_hours,
        workload_limits
):
    violations = []

    for employee in employees:
        violation = check_employee_workload(
            assignments, employee, shift_hours, workload_limits
            )

        if violation:
            violations.append(violation)

    return violations


# Function to run all checks on a rota
def validate_rota(
        assignments, employees, days, shifts, unavailable, shift_hours, 
        workload_limits) -> dict:
    """Returns a dictionary of warnings from checks of coverage, staff only
    assigned to one shift per day, and staffs' unavailable days."""
    coverage_violations = find_coverage_violations(assignments, days, shifts)
    employee_day_violations = find_employee_day_violations(
        assignments, employees, days
        )
    availability_violations = find_availability_violations(
        assignments, unavailable
        )
    workload_violations = find_workload_violations(
        assignments, employees, shift_hours, workload_limits)
    
    return {
        "coverage": coverage_violations,
        "employee_days": employee_day_violations,
        "availability": availability_violations,
        "workload" : workload_violations
    }





if __name__ == "__main__":
    violations = validate_rota(assignments, employees, days, shifts, unavailable,
                               shift_hours, workload_limits)
    for violation_type, problems in violations.items():
        print(f"\n{violation_type}:")

        if problems:
            for problem in problems:
                print(f"- {problem}")
        else:
            print("- No violations")
