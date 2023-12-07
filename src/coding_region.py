from base_sequence import BaseSequence, FragmentFrameIndicator


class CodingRegion(BaseSequence):
    def __init__(
        self,
        start: int,
        end: int,
        is_positive_strand: bool = True,
        chromosome: str = '',
        frame: int = 0,
        exon_number: int = 0,
    ) -> None:
        frame_indicator = FragmentFrameIndicator.get_frame_indicator(frame)
        super().__init__(start, end, is_positive_strand, chromosome, frame_indicator)

        self.exon_number = exon_number
