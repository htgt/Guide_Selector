from adaptors.parsers.parse_guide_tsv import read_guide_tsv_to_guide_sequences
from abstractions.reader import Reader
from utils.file_system import read_gtf_to_df


class MutatorReader(Reader):
    def __init__(self) -> None:
        self.gtf_data = None
        self.guide_sequences = None

    def read_inputs(self, args: dict, guide_sequences=None) -> Reader:
        self.gtf_data = read_gtf_to_df(args['gtf'])
        self.guide_sequences = guide_sequences
        if not self.guide_sequences:
            self.guide_sequences = read_guide_tsv_to_guide_sequences(args['tsv'])
        return self
