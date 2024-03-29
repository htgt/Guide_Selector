import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional, Tuple

from base_sequence import BaseSequence, FragmentFrameIndicator
from target_region import TargetRegion
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


class GuideSequence(BaseSequence):
    def __init__(
        self,
        chromosome: str,
        start: int,
        end: int,
        is_positive_strand: bool = True,
        guide_id: str = '',
        target_region: TargetRegion = TargetRegion(None, None, None),
        frame: int = 0,
        ot_summary: dict = None,
        on_target_score: float = None,
    ) -> None:
        frame_indicator = FragmentFrameIndicator.get_frame_indicator(frame)
        super().__init__(start, end, is_positive_strand, add_chr_prefix(chromosome), frame_indicator)

        self.guide_id = guide_id
        self.target_region = target_region
        self.ot_summary = ot_summary
        self.on_target_score = on_target_score

    @property
    def wge_percentile(self) -> Optional[int]:
        return calculate_wge_percentile(self.ot_summary)

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

    @staticmethod
    def _calculate_coordinate(difference: int, start: int):
        return start + difference

    def find_pam(self, bases: str) -> SequenceFragment:
        pattern = self._define_pam_pattern(self.is_positive_strand)

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

    @property
    def centrality_score(self) -> Optional[float]:
        if self.target_region.start and self.target_region.end:
            pam = self.find_pam(self.bases)
            if type(pam) == PamNotFoundError:
                return None
            pam_midpoint = pam.start + 1
            tr_midpoint = (self.target_region.start + self.target_region.end) / 2
            tr_length = self.target_region.end - self.target_region.start
            standardised_distance = abs(pam_midpoint - tr_midpoint) / tr_length
            score = 1 - standardised_distance
            return float(Decimal(score).quantize(Decimal('0.0001'), ROUND_HALF_UP))
        else:
            return None
