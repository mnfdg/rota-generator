# Code map

```mermaid
flowchart LR
    Inputs["Rota inputs<br/>employees, days, shifts,<br/>unavailability, shift hours,<br/>workload limits"]

    Inputs --> Generate["generator.py<br/>generate_rota()"]

    Generate -->|Feasible| Assignments["Generated assignments<br/>(employee, day, shift)"]
    Generate -->|Infeasible| NoRota["None"]

    Assignments --> Validate["rota.py<br/>validate_rota()"]

    Validate --> Coverage["find_coverage_violations()"]
    Coverage --> CountCoverage["count_assignments()"]

    Validate --> EmployeeDays["find_employee_day_violations()"]
    EmployeeDays --> CountEmployeeDays["count_employee_day_assignments()"]

    Validate --> Availability["find_availability_violations()"]
    Availability --> CheckAvailability["check_assignment_availability()"]

    Validate --> Workload["find_workload_violations()"]
    Workload --> CheckWorkload["check_employee_workload()"]
    CheckWorkload --> CalculateHours["calculate_employee_hours()"]

    Coverage --> Results["Dictionary of violations"]
    EmployeeDays --> Results
    Availability --> Results
    Workload --> Results

    TestGenerator["test_generator.py"] -. tests .-> Generate
    TestGenerator -. tests .-> Validate
    TestRota["test_rota.py"] -. tests .-> Validate
```


## Main functions

| Function | Takes | Returns |
|---|---|---|
| `generate_rota()` | Employees, days, shifts, availability, staffing requirements, shift hours and workload limits | Assignment list, or `None` |
| `validate_rota()` | Assignment list and rota information | Dictionary containing each category of violation |
| `count_assignments()` | Assignments, one day and one shift | Number of assigned employees |
| `calculate_employee_hours()` | Assignments, one employee and shift durations | Total assigned hours |
| `check_employee_workload()` | Assignments and one employee's workload limits | Warning string, or `None` |