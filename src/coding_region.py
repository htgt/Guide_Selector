from base_sequence import BaseSequence


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
        self.exon_number = exon_number
        self.start = start
        self.end = end
        self.chromosome = chromosome
        self.is_positive_strand = is_positive_strand
        self.frame = frame
