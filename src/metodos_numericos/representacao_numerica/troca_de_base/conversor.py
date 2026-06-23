from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

@dataclass(frozen=True)
class BaseConversionStep:
    description: str
    value: str

@dataclass(frozen=True)
class BaseConversionResult:
    original: str
    source_base: int
    target_base: int
    converted: str
    decimal_value: str
    steps: list[BaseConversionStep]


def _validate_base(base: int) -> None:
    if not 2 <= base <= 36:
        raise ValueError("A base deve estar entre 2 e 36.")


def _digit_value(char: str) -> int:
    char = char.upper()
    if char not in _DIGITS:
        raise ValueError(f"Dígito inválido: {char}")
    return _DIGITS.index(char)


def to_decimal(number: str, source_base: int) -> tuple[Fraction, list[BaseConversionStep]]:
    _validate_base(source_base)
    raw = number.strip().upper().replace(",", ".")
    sign = -1 if raw.startswith("-") else 1
    raw = raw.lstrip("+-")
    integer_part, _, fractional_part = raw.partition(".")
    total = Fraction(0, 1)
    steps: list[BaseConversionStep] = []

    for power, char in enumerate(reversed(integer_part or "0")):
        value = _digit_value(char)
        if value >= source_base:
            raise ValueError(f"Dígito {char} não existe na base {source_base}.")
        contribution = value * (source_base ** power)
        total += contribution
        steps.append(BaseConversionStep(f"{char} × {source_base}^{power}", str(contribution)))

    for index, char in enumerate(fractional_part, start=1):
        value = _digit_value(char)
        if value >= source_base:
            raise ValueError(f"Dígito {char} não existe na base {source_base}.")
        contribution = Fraction(value, source_base ** index)
        total += contribution
        steps.append(BaseConversionStep(f"{char} × {source_base}^-{index}", f"{float(contribution):.12g}"))

    return sign * total, steps


def from_decimal(value: Fraction, target_base: int, max_fraction_digits: int = 12) -> tuple[str, list[BaseConversionStep]]:
    _validate_base(target_base)
    steps: list[BaseConversionStep] = []
    sign = "-" if value < 0 else ""
    value = abs(value)
    integer = value.numerator // value.denominator
    fraction = value - integer

    if integer == 0:
        integer_digits = ["0"]
    else:
        integer_digits = []
        n = integer
        while n > 0:
            n, remainder = divmod(n, target_base)
            integer_digits.append(_DIGITS[remainder])
            steps.append(BaseConversionStep(f"divisão por {target_base}", f"quociente={n}, resto={remainder}"))
        integer_digits.reverse()

    fractional_digits: list[str] = []
    for _ in range(max_fraction_digits):
        if fraction == 0:
            break
        fraction *= target_base
        digit = fraction.numerator // fraction.denominator
        fractional_digits.append(_DIGITS[digit])
        steps.append(BaseConversionStep(f"multiplicação fracionária por {target_base}", f"dígito={digit}, resto={float(fraction - digit):.12g}"))
        fraction -= digit

    converted = sign + "".join(integer_digits)
    if fractional_digits:
        converted += "." + "".join(fractional_digits)
    return converted, steps


def convert_base(number: str, source_base: int, target_base: int, max_fraction_digits: int = 12) -> BaseConversionResult:
    decimal, to_steps = to_decimal(number, source_base)
    converted, from_steps = from_decimal(decimal, target_base, max_fraction_digits)
    return BaseConversionResult(number, source_base, target_base, converted, str(decimal), to_steps + from_steps)
