import re
from dataclasses import dataclass
from typing import Tuple
from mutator.base_sequence import BaseSequence
<<<<<<< HEAD
from typing import Optional
=======
from mutator.edit_window import EditWindow
>>>>>>> bd95b0e... TD-419 Build window in MutationBuilder

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

    def _calculate_actual_coordinate(self, relative_coordinate, region_start):
        return region_start + relative_coordinate

    def find_pam(self, bases) -> SequenceFragment:
        pattern = self._define_pam_pattern()
        pam_matches = re.finditer(pattern, bases)

        for match in pam_matches:
            if self._check_pam_position(match, bases):
                pam = match

        if pam_matches:
            return SequenceFragment(
                pam.group(0),
                self._calculate_actual_coordinate(pam.start(0), self.start),
                self._calculate_actual_coordinate(pam.end(0) - 1, self.start)
            )
        else:
            raise Exception('No PAM found in the sequence')

    def define_window(self) -> Tuple[int, int]:
        bases = self._get_sequence_by_coords().upper()
        pam = self.find_pam(bases)

        if self.is_positive_strand:
            window_start = pam.end  - self.window_length + 1
            window_end = pam.end
        else:
            window_start = pam.start
            window_end = pam.end + self.window_length

        return  window_start, window_end

