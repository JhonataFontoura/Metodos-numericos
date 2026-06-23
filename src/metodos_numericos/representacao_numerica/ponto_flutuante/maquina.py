from __future__ import annotations
import math
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from fractions import Fraction


def max_rounding_relative_error(base: int, precision: int) -> float:
    return 0.5 * (base ** (1 - precision))


def truncate_decimal(value: str | float, digits: int) -> Decimal:
    quant = Decimal("1").scaleb(-digits)
    return Decimal(str(value)).quantize(quant, rounding=ROUND_DOWN)


def round_decimal(value: str | float, digits: int) -> Decimal:
    quant = Decimal("1").scaleb(-digits)
    return Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP)


def machine_range(base: int, precision: int, min_exponent: int, max_exponent: int) -> dict[str, float]:
    lower = base ** (min_exponent - 1)
    upper = (1 - base ** (-precision)) * (base ** max_exponent)
    return {"menor_normalizado": lower, "maior_normalizado": upper}


def classify_float_event(value: float, base: int, precision: int, min_exponent: int, max_exponent: int) -> str:
    limits = machine_range(base, precision, min_exponent, max_exponent)
    if value != 0 and abs(value) < limits["menor_normalizado"]:
        return "underflow"
    if abs(value) > limits["maior_normalizado"]:
        return "overflow"
    return "representável"
