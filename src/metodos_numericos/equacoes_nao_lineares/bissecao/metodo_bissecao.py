from __future__ import annotations
from typing import Callable
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def bisection(f: Callable[[float], float], a: float, b: float, tolerance: float = 1e-6, max_iterations: int = 100) -> MethodResult:
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return MethodResult("Bisseção", None, False, "O intervalo não garante troca de sinal.")
    rows: list[IterationRow] = []
    midpoint = a
    for i in range(1, max_iterations + 1):
        midpoint = (a + b) / 2
        fm = f(midpoint)
        error = abs(b - a) / 2
        rows.append(IterationRow(i, {"a": a, "b": b, "xm": midpoint, "f(xm)": fm, "erro": error}))
        if abs(fm) <= tolerance or error <= tolerance:
            return MethodResult("Bisseção", midpoint, True, "Critério de parada atingido.", rows)
        if fa * fm < 0:
            b, fb = midpoint, fm
        else:
            a, fa = midpoint, fm
    return MethodResult("Bisseção", midpoint, False, "Número máximo de iterações atingido.", rows)
