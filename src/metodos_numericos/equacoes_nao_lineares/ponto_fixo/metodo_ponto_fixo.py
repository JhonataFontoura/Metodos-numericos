from __future__ import annotations
from typing import Callable
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def fixed_point(g: Callable[[float], float], x0: float, tolerance: float = 1e-6, max_iterations: int = 100) -> MethodResult:
    rows: list[IterationRow] = []
    x = x0
    last_error = None
    for i in range(1, max_iterations + 1):
        next_x = g(x)
        error = abs(next_x - x)
        tendency = "indefinida" if last_error is None else ("melhorando" if error <= last_error else "piorando")
        rows.append(IterationRow(i, {"xk": x, "g(xk)": next_x, "erro": error, "tendência": tendency}))
        if error <= tolerance:
            return MethodResult("Ponto Fixo", next_x, True, "Convergência atingida pelo erro.", rows)
        if abs(next_x) > 1e12:
            return MethodResult("Ponto Fixo", next_x, False, "Possível divergência: valores cresceram demais.", rows)
        x, last_error = next_x, error
    return MethodResult("Ponto Fixo", x, False, "Número máximo de iterações atingido; verifique convergência.", rows)
