from ortools.sat.python import cp_model

from rota import (
    REQUIRED_STAFF,
    days,
    employees,
    shifts,
    unavailable,
    shift_hours,
    workload_limits,
    validate_rota,
)

Assignment = tuple[str, str, str]

def generate_rota(
    employees: list[str],
    days: list[str],
    shifts: list[str],
    unavailable: dict[str, set[str]],
    required_staff: int,
    shift_hours,
    workload_limits
) -> list[Assignment] | None:  
    """Generate a rota satisfying the Version 0.3 hard constraints.

    Return the generated assignments, or None if no feasible rota exists.
    """
    model = cp_model.CpModel()

    assign = {}

    # Creates a Boolean variable with a name {employee}_{day}_{shift} for every 
    # combination of employees, days and shifts.
    for employee in employees:
        for day in days:
            for shift in shifts:
                # Create a Boolean decision variable (no value yet)
                assign[employee, day, shift] = model.new_bool_var(
                    f"{employee}_{day}_{shift}"
                )


    # Add solver constraint: Number of staff assigned to a shift must equal 
    # required number of staff
    for day in days:
        for shift in shifts:
            model.add(
                sum(
                    assign[employee, day, shift]
                    for employee in employees
                )
                == required_staff
            )

    # Add solver constraint: Staff cannot be assigned to more than 1 shift 
    # per day
    for employee in employees:
        for day in days:
            model.add(
                sum(
                    assign[employee, day, shift]
                    for shift in shifts
                )
                <= 1
            )

    # Add solver constraint: Staff cannot be assigned to an unavailable day
    for employee in employees:
        for unavailable_day in unavailable[employee]:
            for shift in shifts:
                model.add(
                    assign[employee, unavailable_day, shift] == 0
                )

    # Add solver constraint: Staff must work within allowed range of hours
    for employee in employees:
        assigned_hours = sum(
            assign[employee, day, shift] * shift_hours[shift]
            for day in days
            for shift in shifts
        )

        minimum_hours = workload_limits[employee]["minimum"]
        maximum_hours = workload_limits[employee]["maximum"]

        model.add(assigned_hours >= minimum_hours)
        model.add(assigned_hours <= maximum_hours)

    solver = cp_model.CpSolver()    # Create solver
    status = solver.solve(model)    # Find values for the Boolean variables

    generated_assignments = []

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for employee in employees:
            for day in days:
                for shift in shifts:
                    if solver.value(assign[employee, day, shift]) == 1:
                        generated_assignments.append((employee, day, shift))
    else:
        return None

    return generated_assignments


if __name__ == "__main__":
    generated_assignments = generate_rota(
        employees,
        days,
        shifts,
        unavailable,
        REQUIRED_STAFF,
        shift_hours,
        workload_limits
    )

    if generated_assignments is None:
        print("No valid rota was found.")
    else:
        violations = validate_rota(
            generated_assignments,
            employees,
            days,
            shifts,
            unavailable,
            shift_hours,
            workload_limits
        )

        for assignment in generated_assignments:
            print(assignment)

        print("\nValidator results:")

        for violation_type, problems in violations.items():
            print(f"\n{violation_type}:")

            if problems:
                for problem in problems:
                    print(f"- {problem}")
            else:
                print("- No violations")

                