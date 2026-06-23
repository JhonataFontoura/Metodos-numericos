from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class IterationRow:
    iteration: int
    values: dict[str, Any]

@dataclass(frozen=True)
class MethodResult:
    method: str
    result: Any
    converged: bool = True
    message: str = ""
    iterations: list[IterationRow] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def as_text(self) -> str:
        lines = [f"Método: {self.method}", f"Resultado: {self.result}", f"Status: {'convergiu' if self.converged else 'não convergiu'}"]
        if self.message:
            lines.append(f"Mensagem: {self.message}")
        if self.iterations:
            lines.append("\nIterações:")
            for row in self.iterations:
                vals = " | ".join(f"{k}={v}" for k, v in row.values.items())
                lines.append(f"{row.iteration}: {vals}")
        return "\n".join(lines)
