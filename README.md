# Rota Generator

A Python project exploring employee rota generation using constraint
programming with Google OR-Tools.

## Current functionality

Version 0.2 can:

- validate manually supplied rotas;
- generate a feasible rota;
- enforce shift coverage;
- prevent multiple shifts per employee per day;
- respect unavailable days;
- report when no feasible rota exists.

## Run the generator

```bash
py generator.py
```

## Run the tests

```bash
py -m pytest
```