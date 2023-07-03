from dataclasses import dataclass
from enum import Enum

from utils.get_data.ensembl import get_seq_from_ensembl_by_coords

class PositionInCodon(Enum):
    FIRST = 0
    SECOND = 1
    THIRD = 2


@dataclass
class BaseSequence:
    start: int
    end: int
    isPositiveStrand: bool
    chromosome: str
    frame: PositionInCodon = 0

    def _get_sequence_by_coords(self, chromosome, start, end) -> str:
        return get_seq_from_ensembl_by_coords(chromosome, start, end)

    def _get_sequence_codons(self):
        pass

