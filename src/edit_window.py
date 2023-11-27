from typing import List, Optional, Tuple

from Bio.Seq import Seq

from base_sequence import BaseSequence
from codon import WindowCodon


class EditWindow(BaseSequence):
    def __init__(
        self,
        start: int,
        end: int,
        window_length: int,
        is_positive_strand: bool = True,
        chromosome: Optional[str] = None,
        frame: int = 0,
        guide_strand_is_positive: bool = True,
    ) -> None:
        self.id = id
        self.start = start
        self.end = end
        self._window_length = window_length
        self.is_positive_strand = is_positive_strand
        self.chromosome = chromosome
        self.frame = frame
        self.guide_strand = guide_strand_is_positive

    def _get_extended_window_coordinates(self) -> Tuple[int, int]:
        start = self.start
        end = self.end

        if self.frame == 0:
            return start, end

        if self.is_positive_strand:
            start = self.start - 3 + self.frame
        else:
            end = self.end + 3 - self.frame

        return start, end

    def split_window_into_codons(
        self,
        bases: str,
        start: int,
        end: int,
        is_positive_strand: bool,
        config: dict,
        cds_start: int,
        cds_end: int,
    ) -> List[WindowCodon]:
        length = len(bases)
        codons = []

        for i in range(0, length - 2, 3):
            coordinate = self._get_third_base_coordinate(start, end, i, is_positive_strand)
            window_position = self._get_base_window_position(coordinate)

            if is_positive_strand:
                codon_seq = bases[i : i + 3]
            else:
                codon_seq = str(Seq(bases[length - i - 3 : length - i]).reverse_complement())

            codon = WindowCodon(codon_seq, coordinate, window_position, is_positive_strand)

            if codon.is_edit_permitted(config, cds_start, cds_end):
                codons.append(codon)

        return codons

    def _get_third_base_coordinate(self, start: int, end: int, i: int, is_positive_strand: bool) -> int:
        if is_positive_strand:
            return start + i + 2
        else:
            return end - i - 2

    def _get_base_window_position(self, coordinate: int) -> int:
        return calculate_position_in_window(self.start, coordinate, self.guide_strand, self._window_length)

    def _get_extended_window_bases(self, coords: Tuple[int, int]) -> str:
        extended_window = BaseSequence(
            coords[0],
            coords[1],
            self.is_positive_strand,
            self.chromosome,
        )

        return extended_window.get_sequence_by_coords()

    def get_window_codons(self, config: dict, cds_start: int, cds_end: int) -> List[WindowCodon]:
        extended_coords = self._get_extended_window_coordinates()
        extended_bases = self._get_extended_window_bases(extended_coords)

        codons = self.split_window_into_codons(
            extended_bases,
            extended_coords[0],
            extended_coords[1],
            self.is_positive_strand,
            config,
            cds_start,
            cds_end
        )

        return codons

    # Position in window - for 12 bases length window (12 is 9 + PAM)
    # Positive strand: NNNNNNNNN PAM - 9...1 -1 ... -3
    # Negative strand: PAM NNNNNNNNN - -3 ... -1 1 ... 9


def calculate_position_in_window(window_start: int, coordinate: int, strand: bool, window_length: int) -> int:
    PAM_PROTECTION_LENGTH = 3

    result = 0
    coords_diff = coordinate - window_start

    if strand:
        result = window_length - PAM_PROTECTION_LENGTH - coords_diff

        if result <= 0:
            result = result - 1
    else:
        result = coords_diff - PAM_PROTECTION_LENGTH
        if result >= 0:
            result = result + 1

    return result
