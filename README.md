# Rota Generator

Beginning of a Python project exploring employee rota generation using constraint programming with Google OR-Tools.

The aim is ultimately to generate rotas that satisfy the complex shift patterns of a 24/7 hospital department with multiple locations, shift lengths and qualification requirements, while respecting individual employee shift preferences and qualifications.

## Current functionality

This version can:

- validate manually supplied rotas;
- generate a feasible rota;
- enforce shift coverage for a uniform number of required staff;
- assign to shifts with different lengths;
- prevent multiple shifts per employee per day;
- respect employee's unavailable days;
- respect employee' different workload ranges;
- report when no feasible rota exists.

Limitations:
This is a prototype using fixed, simple example data. There is currently no support for qualifications, employee preferences, fairness, time between shifts or varying requirements.  

## How it works

Data is specified in the variables at the top of `rota.py`.

The `generate_rota` function in `generator.py` creates a Boolean variable for every possible assignment `(employee, day, shift)` combination. Constraints are set for OR-Tools to satisfy as it then searches for a suitable combination of these Boolean variables.

If such a combination is found, it is converted into a list of assignment tuples and returned. A separate `validate_rota` function checks this list and returns a list of any violations.


## Installation, use and testing

```bash
pip install -r requirements.txt
python generator.py
py -m pytest
