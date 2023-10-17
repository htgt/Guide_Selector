from dataclasses import dataclass
from enum import Enum

from utils.get_data.ensembl import get_seq_from_ensembl_by_coords


class FragmentFrameIndicator(Enum):
    ZERO = 0
    TWO = 2
    ONE = 1


@dataclass
class BaseSequence:
    start: int
    end: int
    is_positive_strand: bool = True
    chromosome: str = ""
    frame: FragmentFrameIndicator = FragmentFrameIndicator.ZERO

    @property
    def bases(self) -> str:
        return self.get_sequence_by_coords().upper()

    def get_sequence_by_coords(self) -> str:
        bases = get_seq_from_ensembl_by_coords(self.chromosome, self.start, self.end)

        return bases
