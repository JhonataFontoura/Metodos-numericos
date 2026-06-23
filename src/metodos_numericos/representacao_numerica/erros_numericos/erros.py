from __future__ import annotations
import math
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from fractions import Fraction


def absolute_error(exact: float, approximate: float) -> float:
    return abs(exact - approximate)


def relative_error(exact: float, approximate: float) -> float:
    if exact == 0:
        raise ZeroDivisionError("Erro relativo não é definido para valor exato zero.")
    return abs(exact - approximate) / abs(exact)


def percentage_error(exact: float, approximate: float) -> float:
    return relative_error(exact, approximate) * 100


def cancellation_detector(a: float, b: float) -> dict[str, float | str]:
    result = a - b
    magnitude_ratio = abs(result) / max(abs(a), abs(b), 1e-300)
    return {
        "resultado": result,
        "razao_magnitude": magnitude_ratio,
        "alerta": "possível cancelamento" if magnitude_ratio < 1e-6 else "baixo risco",
    }
