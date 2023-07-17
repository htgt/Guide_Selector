import re
from dataclasses import dataclass
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

class GuideSequence:
    def __init__(self,
            start: int,
            end: int,
            isPositiveStrand: bool = True,
            guide_id: int = 0,
            window_length: int = 12
        ) -> None:

        self.id = id
        self.start = start
        self.end  = end
        self.guide_id = guide_id
        self.isPositiveStrand = isPositiveStrand
        self.window_length = window_length

        self.bases = self._get_sequence_by_coord(self.chromosome, start, end).upper()

        self.pam = self.find_pam()
        self.window = self.define_window()


    def _define_pam_pattern(self) -> str:
        return PAM_POSITIVE_PATTERN if self.isPositiveStrand else PAM_NEGATIVE_PATTERN

    def _check_pam_position(self, match: re.Match) -> bool:
        MAX_PAM_POSITION_FROM_SEQ_EDGE = 2
        is_pam = False

        if not self.isPositiveStrand:
            is_pam = ( match.start() <= MAX_PAM_POSITION_FROM_SEQ_EDGE )
        else:
            is_pam = ( match.end() >= len(self.bases) - MAX_PAM_POSITION_FROM_SEQ_EDGE )

        return is_pam


    def find_pam(self) -> SequenceFragment:
        pattern = self._define_pam_pattern()
        pam_matches = re.finditer(pattern, self.bases)

        for match in pam_matches:
            if self._check_pam_position(match):
                pam = match

        if pam_matches:
            return SequenceFragment(pam.group(0), pam.start(0), pam.end(0))
        else:
            raise Exception('No PAM found in the sequence')


    def define_window(self) -> SequenceFragment:
        if self.isPositiveStrand:
            window_start = self.pam.end - self.window_length
            window_end = self.pam.end
        else:
            window_start = self.pam.start
            window_end = self.pam.end + self.window_length

        window_bases = self.bases[window_start:window_end]

        return SequenceFragment(window_bases, window_start, window_end)



