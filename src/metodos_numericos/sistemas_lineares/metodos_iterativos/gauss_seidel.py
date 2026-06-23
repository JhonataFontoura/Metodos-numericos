from __future__ import annotations
from copy import deepcopy
from metodos_numericos.core.resultado import IterationRow, MethodResult

Matrix = list[list[float]]
Vector = list[float]

def gauss_seidel(A: Matrix, b: Vector, x0: Vector | None = None, tolerance: float = 1e-6, max_iterations: int = 100) -> MethodResult:
    n = len(A)
    x = x0[:] if x0 else [0.0] * n
    rows: list[IterationRow] = []
    for iteration in range(1, max_iterations + 1):
        old = x[:]
        for i in range(n):
            if abs(A[i][i]) < 1e-14:
                return MethodResult("Gauss-Seidel", x, False, "Elemento diagonal nulo.", rows)
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(n) if j != i)) / A[i][i]
        error = max(abs(x[i] - old[i]) for i in range(n))
        rows.append(IterationRow(iteration, {"x": x[:], "erro": error}))
        if error <= tolerance:
            return MethodResult("Gauss-Seidel", x, True, "Critério de parada atingido.", rows)
    return MethodResult("Gauss-Seidel", x, False, "Número máximo de iterações atingido.", rows)
