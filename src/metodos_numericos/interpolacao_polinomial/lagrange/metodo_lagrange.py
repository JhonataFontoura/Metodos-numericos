from __future__ import annotations
from metodos_numericos.core.resultado import IterationRow, MethodResult

def lagrange(xs: list[float], ys: list[float], x: float) -> MethodResult:
    if len(xs) != len(ys) or len(set(xs)) != len(xs):
        return MethodResult("Interpolação de Lagrange", None, False, "Pontos inválidos ou x repetido.")
    total = 0.0
    rows: list[IterationRow] = []
    for i, xi in enumerate(xs):
        Li = 1.0
        factors = []
        for j, xj in enumerate(xs):
            if i != j:
                factor = (x - xj) / (xi - xj)
                Li *= factor
                factors.append(factor)
        contribution = ys[i] * Li
        total += contribution
        rows.append(IterationRow(i, {"L_i": Li, "y_i*L_i": contribution, "fatores": factors}))
    return MethodResult("Interpolação de Lagrange", total, True, "Valor interpolado calculado.", rows)
