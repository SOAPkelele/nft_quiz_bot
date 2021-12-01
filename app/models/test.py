from dataclasses import dataclass


@dataclass
class Test:
    id: int
    name: str
    description: str
    lang: str
