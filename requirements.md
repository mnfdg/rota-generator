# Version 0.1 Requirements

## Goal
The user manually supplies a rota.
The program checks the rota and reports all rule violations.

## Employees
The fictional workplace has six employees:
- Alice
- Ben
- Cara
- Dan
- Eve
- Frank

## Period
The rota covers Monday to Sunday.

## Shifts
Each day has two shifts:
- Early
- Late

Each shift requires two employees.

## Rules
1. Each shift must have exactly two employees.
2. An employee cannot work more than one shift per day.
3. An employee cannot work on a day when they are unavailable.


# Version 0.2 Requirements

## Goal
Automatically generate a rota that satisfies all Version 0.1 rules.

## Generator behaviour
The generator must:
1. assign exactly two employees to every shift;
2. assign each employee to at most one shift per day;
3. avoid assigning employees on unavailable days;
4. return assignments in the same tuple format used by the validator;
5. return `None` when no feasible rota exists.

## Verification
Every generated rota is checked using the independent Version 0.1
validator.

## Not included
Version 0.2 does not yet consider:
- weekly working hours
- different shift lengths
- rest between shifts
- preferences
- fairness
- night-shift patterns
- multiple locations or qualifications

# Version 0.3 Requirements

## Goal
Account for different shift durations and employee-specific contracted
working hours across the full rota period.

## Workload
Each shift has a duration in hours.

Each employee has a target average number of hours per week. Their required
hours for the rota are calculated across the whole planning period rather
than enforced separately for each calendar week.

Employees may work different numbers of hours in individual weeks, provided
their total workload remains within the permitted range for the full rota.

## Not included
Version 0.3 does not yet consider:
- employee preferences for clustered or spread-out shifts
- maximum consecutive working days
- minimum blocks of days off
- night-shift recovery
- fairness or optimisation