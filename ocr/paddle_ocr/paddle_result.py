from dataclasses import dataclass

@dataclass
class PaddleResult:
    value: dict[str, str] = None
    prob: float = None
    pos: list[list] = None