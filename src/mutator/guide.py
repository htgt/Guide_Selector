import re
from dataclasses import dataclass

PAM_POSITIVE_PATTERN = r'TGG'
PAM_NEGATIVE_PATTERN = r'CCA'

@dataclass
class SequenceFragment:
    bases: str
    start: int
    end: int

class GuideSequence:
    def __init__(self,
            bases: str,
            strand: str,
            window_length: int = 12
        ) -> None:

        self.bases = bases.upper()
        self.strand = strand
        self.window_length = window_length


    def find_pam(self) -> SequenceFragment:
        if self.strand == "+":
            pattern = PAM_POSITIVE_PATTERN
        else:
            pattern = PAM_NEGATIVE_PATTERN

        pam = re.search(pattern, self.bases)

        return SequenceFragment(pam.group(0), pam.start(0), pam.end(0))


    def define_window_positive_strand(self, pam_position: dict) -> SequenceFragment:
        window_start = pam_position["end"] - self.window_length
        window_end = pam_position["end"]

        return {
            "start": window_start,
            "end": window_end,
        }



