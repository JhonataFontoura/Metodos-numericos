from __future__ import annotations
from copy import deepcopy
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

Matrix = list[list[float]]
Vector = list[float]

def lu_decomposition(A: Matrix) -> MethodResult:
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    rows: list[IterationRow] = []
    for i in range(n):
        L[i][i] = 1.0
    for k in range(n):
        for j in range(k, n):
            U[k][j] = A[k][j] - sum(L[k][s] * U[s][j] for s in range(k))
        if abs(U[k][k]) < 1e-14:
            return MethodResult("Decomposição LU", None, False, "Pivô nulo. Tente pivotamento ou outra ordem de linhas.", rows)
        for i in range(k + 1, n):
            L[i][k] = (A[i][k] - sum(L[i][s] * U[s][k] for s in range(k))) / U[k][k]
        rows.append(IterationRow(k + 1, {"L": deepcopy(L), "U": deepcopy(U)}))
    return MethodResult("Decomposição LU", {"L": L, "U": U}, True, "A = L × U.", rows)
