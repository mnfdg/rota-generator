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
working hours across a multi-week rota period.

## Planning period

The example rota covers two weeks.

Working hours are assessed across the entire two-week period, not separately
for each calendar week.

## Shift durations

Each shift type has a duration in hours.

For example:

- Early: 8 hours
- Late: 8 hours
- Long day: 12 hours

## Employee workload

Each employee has a contracted average number of hours per week.

For a two-week rota, an employee contracted for 40 hours per week has a
target of 80 hours across the full rota period.

Employees do not need to work exactly 40 hours in each individual week.

The generator may use a permitted range around the target rather than
requiring an exact total.

## Existing rules

The Version 0.2 rules still apply:

1. Every shift must receive the required number of employees.
2. An employee may work at most one shift per day.
3. Employees may not work when unavailable.
4. The generator returns `None` if no feasible rota exists.

## Not included

Version 0.3 does not yet model:

- maximum consecutive working days;
- preferences for clustered or spread-out shifts;
- minimum blocks of days off;
- detailed rest periods;
- night-shift blocks and recovery;
- fairness or optimisation.