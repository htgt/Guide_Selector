from dataclasses import dataclass

from utils.get_data.ensembl import get_seq_from_ensembl_by_coords

@dataclass
class SequenceRegion:
    isPositiveStrand: bool
    start: int
    end: int
    frame: int


def get_frame(coding_region: SequenceRegion, region: SequenceRegion) -> int:
    if coding_region.isPositiveStrand:
        if region.start < coding_region.start:
            return coding_region.frame
        difference = region.start - coding_region.start
    else:
        if region.end > coding_region.end:
            return coding_region.frame
        difference = coding_region.end - region.end

    frames = (0, 1, 2)

    return frames[(difference + int(frames.index(coding_region.frame))) % 3]





