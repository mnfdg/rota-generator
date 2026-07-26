# Rota Generator

A Python project exploring employee rota generation using constraint
programming with Google OR-Tools.

## Current functionality

Version 0.3 can:

- validate manually supplied rotas;
- generate a feasible rota;
- enforce shift coverage;
- assign to shifts with different lengths;
- prevent multiple shifts per employee per day;
- respect unavailable days;
- respect workers' different workload ranges;
- report when no feasible rota exists.

## Run the generator

```bash
py generator.py
```

## Run the tests

```bash
py -m pytest
```