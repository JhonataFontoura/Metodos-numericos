from __future__ import annotations
from typing import Callable
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def simpson_one_third(f: Callable[[float], float], a: float, b: float, n: int) -> MethodResult:
    if n % 2 != 0:
        return MethodResult("Simpson 1/3", None, False, "n deve ser par.")
    h = (b - a) / n
    total = f(a) + f(b)
    rows = []
    for i in range(1, n):
        x = a + i * h
        weight = 4 if i % 2 else 2
        total += weight * f(x)
        rows.append(IterationRow(i, {"x": x, "peso": weight, "f(x)": f(x)}))
    return MethodResult("Simpson 1/3", h * total / 3, True, "Integral aproximada.", rows, {"h": h})
