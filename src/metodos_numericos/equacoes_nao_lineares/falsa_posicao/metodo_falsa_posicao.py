from __future__ import annotations
from typing import Callable
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def false_position(f: Callable[[float], float], a: float, b: float, tolerance: float = 1e-6, max_iterations: int = 100) -> MethodResult:
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return MethodResult("Falsa Posição", None, False, "O intervalo não garante troca de sinal.")
    rows: list[IterationRow] = []
    x = a
    for i in range(1, max_iterations + 1):
        x = (a * fb - b * fa) / (fb - fa)
        fx = f(x)
        rows.append(IterationRow(i, {"a": a, "b": b, "x": x, "f(x)": fx}))
        if abs(fx) <= tolerance:
            return MethodResult("Falsa Posição", x, True, "Critério |f(x)| atingido.", rows)
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
    return MethodResult("Falsa Posição", x, False, "Número máximo de iterações atingido.", rows)
