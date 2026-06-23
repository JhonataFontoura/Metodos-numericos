from __future__ import annotations
from typing import Callable
from metodos_numericos.core.resultado import IterationRow, MethodResult
from metodos_numericos.core.funcoes import numerical_derivative

def newton(f: Callable[[float], float], x0: float, tolerance: float = 1e-6, max_iterations: int = 100) -> MethodResult:
    rows: list[IterationRow] = []
    x = x0
    for i in range(1, max_iterations + 1):
        fx = f(x)
        dfx = numerical_derivative(f, x)
        if abs(dfx) < 1e-14:
            return MethodResult("Newton-Raphson", x, False, "Derivada próxima de zero.", rows)
        next_x = x - fx / dfx
        error = abs(next_x - x)
        rows.append(IterationRow(i, {"xk": x, "f(xk)": fx, "f'(xk)": dfx, "xk+1": next_x, "erro": error}))
        if error <= tolerance or abs(f(next_x)) <= tolerance:
            return MethodResult("Newton-Raphson", next_x, True, "Critério de parada atingido.", rows)
        x = next_x
    return MethodResult("Newton-Raphson", x, False, "Número máximo de iterações atingido.", rows)
