from dataclasses import dataclass

@dataclass
class TargetRegion:
    chromosome: str
    id: str
    start: int
    end: int