from base_sequence import BaseSequence, FragmentFrameIndicator


def get_frame(coding_region: BaseSequence, region: BaseSequence) -> FragmentFrameIndicator:
    if coding_region.is_positive_strand:
        difference = region.start - coding_region.start
    else:
        difference = coding_region.end - region.end

    frames = (0, 2, 1)

    frame_value = frames[(difference + frames.index(int(coding_region.frame.value))) % 3]
    return FragmentFrameIndicator.get_frame_indicator(frame_value)
