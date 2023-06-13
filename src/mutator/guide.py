import re

PAM_POSITIVE_PATTERN = r'TGG'
PAM_NEGATIVE_PATTERN = r'CCA'

class GuideSequence:
    def __init__(self, bases: str, strand: str, window_length: int = 12):
        self.bases = bases.upper()
        self.strand = strand
        self.window_length = window_length


    def find_pam(self) -> dict:
        if self.strand == "+":
            pattern = PAM_POSITIVE_PATTERN
        else:
            pattern = PAM_NEGATIVE_PATTERN

        pam = re.search(pattern, self.bases)

        return {
            "start": pam.start(0),
            "end": pam.end(0),
        }


    def define_window_positive_strand(self, pam_position: dict) -> dict:
        window_start = pam_position["end"] - self.window_length
        window_end = pam_position["end"]

        return {
            "start": window_start,
            "end": window_end,
        }



