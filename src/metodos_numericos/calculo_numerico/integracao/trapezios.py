from __future__ import annotations
from typing import Callable
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def trapezoidal(f: Callable[[float], float], a: float, b: float, n: int) -> MethodResult:
    h = (b - a) / n
    total = f(a) + f(b)
    rows = []
    for i in range(1, n):
        x = a + i * h
        total += 2 * f(x)
        rows.append(IterationRow(i, {"x": x, "f(x)": f(x)}))
    return MethodResult("Regra dos Trapézios", h * total / 2, True, "Integral aproximada.", rows, {"h": h})
