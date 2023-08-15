from mutator.base_sequence import BaseSequence


def get_frame(coding_region: BaseSequence, region: BaseSequence) -> int:
    if coding_region.is_positive_strand:
        difference = region.start - coding_region.start
    else:
        difference = coding_region.end - region.end

    frames = (0, 2, 1)

    return frames[(difference + int(frames.index(int(coding_region.frame)))) % 3]
