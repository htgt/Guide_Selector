import re
from dataclasses import dataclass
from typing import Tuple
from mutator.base_sequence import BaseSequence

PAM_POSITIVE_PATTERN = r'.GG'
PAM_NEGATIVE_PATTERN = r'CC.'


@dataclass
class SequenceFragment:
    bases: str
    start: int
    end: int

@dataclass
class GuideSequenceLoci(BaseSequence):
    guide_id: int = 0

class GuideSequence(BaseSequence):
    def __init__(self,
            start: int,
            end: int,
            is_positive_strand: bool = True,
            guide_id: int = 0,
            window_length: int = 12
        ) -> None:

        self.id = id
        self.start = start
        self.end  = end
        self.guide_id = guide_id
        self.is_positive_strand = is_positive_strand
        self.window_length = window_length

        self.bases = self._get_sequence_by_coords(self.chromosome, start, end).upper()

        self.pam = self.find_pam()
        self.window = self.define_window()

    def _define_pam_pattern(self) -> str:
        return PAM_POSITIVE_PATTERN if self.is_positive_strand else PAM_NEGATIVE_PATTERN

    def _check_pam_position(self, match: re.Match) -> bool:
        MAX_PAM_POSITION_FROM_SEQ_EDGE = 2
        is_pam = False

        if not self.is_positive_strand:
            is_pam = ( match.start() <= MAX_PAM_POSITION_FROM_SEQ_EDGE )
        else:
            is_pam = ( match.end() >= len(self.bases) - MAX_PAM_POSITION_FROM_SEQ_EDGE )

        return is_pam


    def find_pam(self) -> SequenceFragment:
        pattern = self._define_pam_pattern()
        pam_matches = re.finditer(pattern, self.bases)

        print(self.bases)

        for match in pam_matches:
            print(match)
            if self._check_pam_position(match):
                pam = match

        if pam_matches:
            return SequenceFragment(
                pam.group(0),
                self._calculate_actual_coordinate(pam.start(0), self.start),
                self._calculate_actual_coordinate(pam.end(0) - 1, self.start)
            )
        else:
            raise Exception('No PAM found in the sequence')

    def _calculate_actual_coordinate(self, relative_coordinate, region_start):
        return region_start + relative_coordinate

    def define_window(self) -> SequenceFragment:
        if self.is_positive_strand:
            window_start = self.pam.end  - self.window_length + 1
            window_end = self.pam.end
        else:
            window_start = self.pam.start
            window_end = self.pam.end + self.window_length

        window_bases = self.bases[window_start:window_end]

        return SequenceFragment(window_bases, window_start, window_end)


def calculate_window_coordinates(guide: GuideSequence) -> Tuple[int, int]:
    window = guide.define_window()

    return window.start, window.end


