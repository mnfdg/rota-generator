# Rota Generator

A Python project exploring employee rota generation using constraint
programming with Google OR-Tools.

## Current functionality

This version can:

- validate manually supplied rotas;
- generate a feasible rota;
- enforce uniform shift coverage;
- assign to shifts with different lengths;
- prevent multiple shifts per employee per day;
- respect unavailable days;
- respect workers' different workload ranges;
- respect workers' individual preferences for working run lengths;
- report when no feasible rota exists.

## Run the generator

```bash
py generator.py
```

## Run the tests

```bash
py -m pytest
```