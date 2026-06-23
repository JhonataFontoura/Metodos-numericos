from __future__ import annotations
import math
import re
from typing import Callable

_ALLOWED = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
    "exp": math.exp, "abs": abs, "pow": pow,
    "pi": math.pi, "e": math.e, "math": math,
}

_SUPERSCRIPT = {"²": "**2", "³": "**3", "⁴": "**4", "⁵": "**5", "⁶": "**6", "⁷": "**7", "⁸": "**8", "⁹": "**9", "¹": "**1", "⁰": "**0"}


def normalize_expression(expression: str) -> str:
    """Converte entradas didáticas como sen(x), √x, x³, 2x e e^x para sintaxe Python segura."""
    expr = expression.strip().replace(",", ".")
    for old, new in _SUPERSCRIPT.items():
        expr = expr.replace(old, new)
    expr = re.sub(r"√\(([^\)]+)\)", r"sqrt(\1)", expr)
    expr = re.sub(r"√([a-zA-Z0-9\.]+)", r"sqrt(\1)", expr)
    expr = expr.replace("^", "**")
    expr = re.sub(r"\be\*\*\(([^\)]+)\)", r"exp(\1)", expr)
    expr = re.sub(r"\be\*\*([a-zA-Z0-9\.]+)", r"exp(\1)", expr)
    for old, new in {"sen": "sin", "tg": "tan", "raiz": "sqrt", "ln": "log"}.items():
        expr = re.sub(rf"\b{old}\b", new, expr, flags=re.IGNORECASE)
    expr = re.sub(r"(\d)(x)", r"\1*\2", expr)
    expr = re.sub(r"(x)(\d)", r"\1*\2", expr)
    expr = re.sub(r"(\d)\(", r"\1*(", expr)
    expr = re.sub(r"\)(\d)", r")*\1", expr)
    expr = re.sub(r"(x)\(", r"\1*(", expr)
    expr = re.sub(r"\)(x)", r")*\1", expr)
    for name in ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "log", "log10", "exp", "abs"]:
        expr = expr.replace(f"{name}*(", f"{name}(")
    return expr


def build_function(expression: str) -> Callable[[float], float]:
    normalized = normalize_expression(expression)

    def f(x: float) -> float:
        return float(eval(normalized, {"__builtins__": {}}, {**_ALLOWED, "x": x}))

    f.original_expression = expression  # type: ignore[attr-defined]
    f.normalized_expression = normalized  # type: ignore[attr-defined]
    return f


def numerical_derivative(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)
