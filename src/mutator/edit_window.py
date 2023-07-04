from dataclasses import dataclass
from typing import List

from mutator.frame import get_frame
from mutator.base_sequence import BaseSequence

@dataclass
class BaseWithPosition:
    base: str
    coordinate: int
    window_position: int

@dataclass
class WindowCodon:
    bases: str
    third: BaseWithPosition


class EditWindow(BaseSequence):
    extended_coords_start: int = 0
    extended_coords_end: int = 0

    def __post_init__(self):
        extended_coords = self._get_extended_window_coordinates()
        self.extended_coords_start = extended_coords[0]
        self.extended_coords_end = extended_coords[1]


    def _get_extended_window_coordinates(self):
        start = self.start
        end = self.end

        if self.frame == 0:
            return start, end

        if self.isPositiveStrand:
            start = self.start - 3 + self.frame
        else:
            end = self.end + 3 - self.frame

        return start, end

    def get_extended_window_bases(self) -> str:
        bases = self._get_sequence_by_coords(
            self.chromosome,
            self.extended_coords_start,
            self.extended_coords_end,
        )

        return bases

    def split_window_into_codons(self, bases: str) -> List[WindowCodon]:
        codons = []

        for i in range(0, len(bases) - 2, 3):
            codon = WindowCodon(bases[i:i+3], bases[i+2])
            codons.append(codon)

        return codons

    def get_window_codons(self) -> List[WindowCodon]:
        bases = self.get_extended_window_bases

        codons = split_window_into_codons(bases)

        return codons
