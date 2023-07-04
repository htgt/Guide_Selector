from mutator.base_sequence import BaseSequence

def get_frame(coding_region: BaseSequence, region: BaseSequence) -> int:
    if coding_region.isPositiveStrand:
        if region.start < coding_region.start:
            return coding_region.frame
        difference = region.start - coding_region.start
    else:
        if region.end > coding_region.end:
            return coding_region.frame
        difference = coding_region.end - region.end

    frames = (0, 2, 1)

    print((difference + int(frames.index(coding_region.frame))) % 3)
    print(frames[(difference + int(frames.index(coding_region.frame))) % 3])

    return frames[(difference + int(frames.index(coding_region.frame))) % 3]





