from __future__ import annotations
from copy import deepcopy
from math import sqrt
from metodos_numericos.core.resultado import IterationRow, MethodResult

Matrix = list[list[float]]
Vector = list[float]

def cholesky(A: Matrix) -> MethodResult:
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    rows: list[IterationRow] = []
    for i in range(n):
        for j in range(i + 1):
            total = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                value = A[i][i] - total
                if value <= 0:
                    return MethodResult("Cholesky", None, False, "Matriz não é definida positiva.", rows)
                L[i][j] = sqrt(value)
            else:
                L[i][j] = (A[i][j] - total) / L[j][j]
        rows.append(IterationRow(i + 1, {"L": deepcopy(L)}))
    return MethodResult("Cholesky", {"L": L, "Lt": [list(row) for row in zip(*L)]}, True, "A = L × Lt.", rows)
