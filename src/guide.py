import re
from dataclasses import dataclass
from typing import Optional, Tuple

from base_sequence import BaseSequence
from utils.bio_utils import add_chr_prefix
from utils.exceptions import PamNotFoundError
from wge_percentile import calculate_wge_percentile

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
    def __init__(
        self,
        chromosome: str,
        start: int,
        end: int,
        is_positive_strand: bool = True,
        guide_id: str = '',
        frame: int = 0,
        ot_summary: dict = None,
        on_target_score: float = None,
    ) -> None:
        self.start = start
        self.end = end
        self.guide_id = guide_id
        self.is_positive_strand = is_positive_strand
        self._chromosome = chromosome
        self.frame = frame
        self.ot_summary = ot_summary
        self.on_target_score = on_target_score

    @property
    def wge_percentile(self) -> Optional[int]:
        return calculate_wge_percentile(self.ot_summary)

    @property
    def chromosome(self) -> str:
        return add_chr_prefix(self._chromosome)

    @property
    def strand_symbol(self) -> str:
        return '+' if self.is_positive_strand else '-'

    @staticmethod
    def _define_pam_pattern(is_positive_strand: bool) -> str:
        return PAM_POSITIVE_PATTERN if is_positive_strand else PAM_NEGATIVE_PATTERN

    @staticmethod
    def _check_pam_position(match: re.Match, bases: str, is_positive_strand: bool) -> bool:
        MAX_PAM_POSITION_FROM_SEQ_EDGE = 2
        is_pam = False

        if not is_positive_strand:
            is_pam = match.start() <= MAX_PAM_POSITION_FROM_SEQ_EDGE
        else:
            is_pam = match.end() >= len(bases) - MAX_PAM_POSITION_FROM_SEQ_EDGE

        return is_pam

    def _calculate_coordinate(self, difference: int, start: int):
        return start + difference

    def find_pam(self, bases: str) -> SequenceFragment:
        pattern = self._define_pam_pattern()
        pam_matches = re.finditer(pattern, bases)
        pam = None

        for match in pam_matches:
            if self._check_pam_position(match, bases, self.is_positive_strand):
                pam = match

        if pam_matches and pam is not None:
            return SequenceFragment(
                pam.group(0),
                self._calculate_coordinate(pam.start(0), self.start),
                self._calculate_coordinate(pam.end(0) - 1, self.start),
            )
        else:
            return PamNotFoundError('No PAM found in the sequence: ' + bases)

    def define_window(self, window_length: int) -> Tuple[int, int]:
        pam = self.find_pam(self.bases)

        if type(pam) == PamNotFoundError:
            return pam

        if self.is_positive_strand:
            window_start = pam.end - window_length + 1
            window_end = pam.end
        else:
            window_start = pam.start
            window_end = pam.end + window_length - 1

        return window_start, window_end
