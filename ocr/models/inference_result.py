from dataclasses import dataclass
from typing import Any


@dataclass
class InferenceResult:
    value: Any = None
    prob: float = None
    pos: list[list] = None
