from __future__ import annotations
from copy import deepcopy
from metodos_numericos.core.resultado import IterationRow, MethodResult

Matrix = list[list[float]]
Vector = list[float]

def gaussian_elimination(A: Matrix, b: Vector) -> MethodResult:
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(deepcopy(A))]
    rows: list[IterationRow] = []
    for k in range(n - 1):
        pivot_row = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[pivot_row][k]) < 1e-14:
            return MethodResult("Eliminação de Gauss", None, False, "Sistema singular ou pivô nulo.", rows)
        if pivot_row != k:
            M[k], M[pivot_row] = M[pivot_row], M[k]
        for i in range(k + 1, n):
            multiplier = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= multiplier * M[k][j]
            rows.append(IterationRow(len(rows) + 1, {"pivô": k + 1, "linha": i + 1, "multiplicador": multiplier, "matriz": [r[:] for r in M]}))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(M[i][i]) < 1e-14:
            return MethodResult("Eliminação de Gauss", None, False, "Sistema sem solução única.", rows)
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return MethodResult("Eliminação de Gauss", x, True, "Solução obtida por retro-substituição.", rows, {"matriz_triangular": M})
