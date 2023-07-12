from dataclasses import dataclass
from typing import List, Tuple

from mutator.frame import get_frame
from mutator.base_sequence import BaseSequence

@dataclass
class BaseWithPosition:
    base: str
    coordinate: int
    window_position: int = 0

@dataclass
class WindowCodon:
    bases: str
    third: BaseWithPosition


class EditWindow(BaseSequence):
    def _get_extended_window_coordinates(self) -> Tuple[int, int]:
        start = self.start
        end = self.end

        if self.frame == 0:
            return start, end

        if self.isPositiveStrand:
            start = self.start - 3 + self.frame
        else:
            end = self.end + 3 - self.frame

        return start, end

    def get_extended_window_bases(self, extended_window_start: int, extended_window_end: int) -> str:
        bases = self._get_sequence_by_coords(
            self.chromosome,
            extended_window_start,
            extended_window_end,
        )

        return bases

    def split_window_into_codons(self, bases: str, start: int) -> List[WindowCodon]:
        codons = []

        for i in range(0, len(bases) - 2, 3):
            coordinate = self._get_third_base_coordinate(start, i+2)
            window_position = self._get_base_window_position(coordinate)

            third = BaseWithPosition(
                bases[i+2],
                coordinate,
                window_position,
            )
            codon = WindowCodon(bases[i:i+3], third)

            codons.append(codon)

        return codons

    def _get_third_base_coordinate(self, start: int, base_position: int) -> int:
        return start + base_position

    def _get_base_window_position(self, coordinate: int) -> int:
        return calculate_position_in_window(self.start, coordinate, self.isPositiveStrand)

    def get_window_codons(self) -> List[WindowCodon]:
        extended_coords = self._get_extended_window_coordinates()

        bases = self.get_extended_window_bases(extended_coords[0], extended_coords[1])
        codons = self.split_window_into_codons(bases, extended_coords[0])

        return codons


    # Position in window - for 12 bases length window (12 is 9 + PAM)
    # Positive strand: NNNNNNNNN PAM - 9...1 -1 ... -3
    # Negative strand: PAM NNNNNNNNN - -3 ... -1 1 ... 9

def calculate_position_in_window(
        window_start: int,
        coordinate: int,
        strand: bool,
        window_length: int = 12
) -> int:
    PAM_PROTECTION_LENGTH = 3

    result = 0
    coords_diff = coordinate - window_start

    if strand == True:
        result = window_length - PAM_PROTECTION_LENGTH - coords_diff

        if result <= 0:
            result = result - 1
    else:
        result = coords_diff - PAM_PROTECTION_LENGTH
        if result >= 0:
            result = result + 1

    return result
