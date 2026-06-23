from __future__ import annotations
from metodos_numericos.compartilhado.resultado import IterationRow, MethodResult

def divided_differences(xs: list[float], ys: list[float]) -> list[list[float]]:
    n = len(xs)
    table = [[0.0] * n for _ in range(n)]
    for i, y in enumerate(ys):
        table[i][0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (xs[i + j] - xs[i])
    return table

def newton_interpolation(xs: list[float], ys: list[float], x: float) -> MethodResult:
    if len(xs) != len(ys) or len(set(xs)) != len(xs):
        return MethodResult("Interpolação de Newton", None, False, "Pontos inválidos ou x repetido.")
    table = divided_differences(xs, ys)
    result = table[0][0]
    product = 1.0
    rows = [IterationRow(0, {"coeficiente": table[0][0], "produto": 1, "parcial": result})]
    for order in range(1, len(xs)):
        product *= x - xs[order - 1]
        result += table[0][order] * product
        rows.append(IterationRow(order, {"coeficiente": table[0][order], "produto": product, "parcial": result}))
    return MethodResult("Interpolação de Newton", result, True, "Valor obtido por diferenças divididas.", rows, {"tabela_diferencas_divididas": table})
