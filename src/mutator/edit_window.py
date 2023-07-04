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

        if self.isPositiveStrand:
            start = self.start - self.frame
        else:
            end = self.end + self.frame

        return start, end

    def get_extended_window_bases(self):
        extended_window = self._get_extended_window_coordinates()
        bases = self._get_sequence_by_coords(
            self.chromosome,
            extended_window[0],
            extended_window[1]
        )

        return bases


    def split_window_into_codons(self, bases) -> List[WindowCodon]:
        codons = []

        for i in range(0, len(bases) - 2, 3):
            codon = WindowCodon(bases[i:i+3], bases[i+2])
            codons.append(codon)

        return codons
