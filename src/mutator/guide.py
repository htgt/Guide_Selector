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

        self.pam = self.find_pam()
        self.window = self.define_window()


    def _define_pam_pattern(self) -> re.Match:
        return PAM_POSITIVE_PATTERN if self.strand == "+" else PAM_NEGATIVE_PATTERN


    def find_pam(self) -> SequenceFragment:
        pattern = self._define_pam_pattern()
        pam = re.search(pattern, self.bases)

        return SequenceFragment(pam.group(0), pam.start(0), pam.end(0))


    def define_window(self) -> SequenceFragment:
        if self.strand == "+":
            window_start = self.pam.end - self.window_length
            window_end = self.pam.end
        else:
            window_start = self.pam.start
            window_end = self.pam.end + self.window_length

        window_bases = self.bases[window_start:window_end]

        return SequenceFragment(window_bases, window_start, window_end)



