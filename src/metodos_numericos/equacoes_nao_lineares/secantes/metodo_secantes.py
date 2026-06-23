from __future__ import annotations
from typing import Callable
from metodos_numericos.core.resultado import IterationRow, MethodResult

def secant(f: Callable[[float], float], x0: float, x1: float, tolerance: float = 1e-6, max_iterations: int = 100) -> MethodResult:
    rows: list[IterationRow] = []
    for i in range(1, max_iterations + 1):
        fx0, fx1 = f(x0), f(x1)
        denominator = fx1 - fx0
        if abs(denominator) < 1e-14:
            return MethodResult("Secantes", x1, False, "Divisão por zero: f(x1)-f(x0) muito pequeno.", rows)
        x2 = (x0 * fx1 - x1 * fx0) / denominator
        error = abs(x2 - x1)
        rows.append(IterationRow(i, {"x0": x0, "x1": x1, "x2": x2, "f(x2)": f(x2), "erro": error}))
        if error <= tolerance or abs(f(x2)) <= tolerance:
            return MethodResult("Secantes", x2, True, "Critério de parada atingido.", rows)
        x0, x1 = x1, x2
    return MethodResult("Secantes", x1, False, "Número máximo de iterações atingido.", rows)
