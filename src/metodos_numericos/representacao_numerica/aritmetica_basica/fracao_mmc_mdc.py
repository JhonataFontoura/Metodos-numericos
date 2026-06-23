from __future__ import annotations
import math
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from fractions import Fraction


def prime_factorization(n: int) -> dict[int, int]:
    n = abs(n)
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def lcm(*values: int) -> int:
    result = 1
    for value in values:
        result = abs(result * value) // math.gcd(result, value)
    return result


def fraction_operation(a: str, operator: str, b: str) -> Fraction:
    left = Fraction(a.replace(",", "."))
    right = Fraction(b.replace(",", "."))
    operations = {
        "+": left + right,
        "-": left - right,
        "*": left * right,
        "/": left / right,
    }
    if operator not in operations:
        raise ValueError("Operador inválido. Use +, -, * ou /.")
    return operations[operator]
