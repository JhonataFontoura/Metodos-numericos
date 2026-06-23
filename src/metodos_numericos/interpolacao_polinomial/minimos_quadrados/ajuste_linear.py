from __future__ import annotations
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def least_squares_line(xs: list[float], ys: list[float]) -> MethodResult:
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x, y in zip(xs, ys))
    denominator = n * sxx - sx * sx
    if abs(denominator) < 1e-14:
        return MethodResult("Mínimos Quadrados Linear", None, False, "Denominador nulo.")
    a = (n * sxy - sx * sy) / denominator
    b = (sy - a * sx) / n
    return MethodResult("Mínimos Quadrados Linear", {"a": a, "b": b, "equação": f"y = {a}x + {b}"}, True, "Ajuste linear calculado.")
