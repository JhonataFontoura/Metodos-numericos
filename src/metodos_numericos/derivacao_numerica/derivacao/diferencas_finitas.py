from __future__ import annotations
from typing import Callable
from metodos_numericos.core.resultado import IterationRow, MethodResult

def finite_difference(f: Callable[[float], float], x: float, h: float, mode: str = "central") -> MethodResult:
    if mode == "progressiva":
        value = (f(x + h) - f(x)) / h
    elif mode == "regressiva":
        value = (f(x) - f(x - h)) / h
    else:
        value = (f(x + h) - f(x - h)) / (2 * h)
        mode = "central"
    return MethodResult("Derivação Numérica", value, True, f"Diferença {mode} calculada.", extra={"h": h})
