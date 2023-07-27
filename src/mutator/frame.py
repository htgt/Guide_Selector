from mutator.base_sequence import BaseSequence

def get_frame(coding_region: BaseSequence, region: BaseSequence) -> int:
    if coding_region.is_positive_strand:
        if region.start < coding_region.start:
            return coding_region.frame
        difference = region.start - coding_region.start
    else:
        if region.end > coding_region.end:
            return coding_region.frame
        difference = coding_region.end - region.end

    frames = (0, 2, 1)

    return frames[(difference + int(frames.index(int(coding_region.frame)))) % 3]





