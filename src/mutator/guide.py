import re
from dataclasses import dataclass
from typing import Tuple
from mutator.base_sequence import BaseSequence
from typing import Optional

PAM_POSITIVE_PATTERN = r'.GG'
PAM_NEGATIVE_PATTERN = r'CC.'


@dataclass
class SequenceFragment:
    bases: str
    start: int
    end: int


class GuideSequence(BaseSequence):
    def __init__(self,
            start: int,
            end: int,
            is_positive_strand: bool = True,
            guide_id: int = 0,
            window_length: int = 12,
            chromosome: Optional[str] = None,
            frame: int = 0,
        ) -> None:

        self.id = id
        self.start = start
        self.end  = end
        self.guide_id = guide_id
        self.is_positive_strand = is_positive_strand
        self.window_length = window_length
        self.chromosome = chromosome
        self.frame = frame

    def _define_pam_pattern(self) -> str:
        return PAM_POSITIVE_PATTERN if self.is_positive_strand else PAM_NEGATIVE_PATTERN

    def _check_pam_position(self, match: re.Match, bases) -> bool:
        MAX_PAM_POSITION_FROM_SEQ_EDGE = 2
        is_pam = False

        if not self.is_positive_strand:
            is_pam = ( match.start() <= MAX_PAM_POSITION_FROM_SEQ_EDGE )
        else:
            is_pam = ( match.end() >= len(bases) - MAX_PAM_POSITION_FROM_SEQ_EDGE )

        return is_pam

    def _calculate_coordinate(self, difference, start):
        return start + difference

    def find_pam(self, bases) -> SequenceFragment:
        pattern = self._define_pam_pattern()
        pam_matches = re.finditer(pattern, bases)
        pam = None
        print(pam_matches)
        for match in pam_matches:
            if self._check_pam_position(match, bases):
                pam = match

        if pam_matches and pam is not None:
            return SequenceFragment(
                pam.group(0),
                self._calculate_coordinate(pam.start(0), self.start),
                self._calculate_coordinate(pam.end(0) - 1, self.start)
            )
        else:
            #raise Exception('No PAM found in the sequence')
            print('No PAM found in the sequence: ' + bases)

    def define_window(self) -> Tuple[int, int]:
        bases = self.get_sequence_by_coords().upper()
        pam = self.find_pam(bases)

        if self.is_positive_strand:
            window_start = pam.end  - self.window_length + 1
            window_end = pam.end
        else:
            window_start = pam.start
            window_end = pam.end + self.window_length - 1

        return  window_start, window_end

