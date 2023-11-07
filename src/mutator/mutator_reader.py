from abstractions.reader import Reader
from adaptors.parsers.parse_on_target_score_tsv import get_guides_on_target_scores
from adaptors.parsers.parse_guide_tsv import read_guide_tsv_to_guide_sequences
from utils.file_system import read_gtf_to_df


class MutatorReader(Reader):
    def __init__(self) -> None:
        self.gtf_data = None
        self.guide_sequences = []

    def read_inputs(self, args: dict, guide_sequences=None) -> Reader:
        self.gtf_data = read_gtf_to_df(args['gtf'])
        self.guide_sequences = guide_sequences or read_guide_tsv_to_guide_sequences(args['tsv'])

        if on_target_scores := get_guides_on_target_scores(args['on_target']):
            for guide in self.guide_sequences:
                guide.on_target_score = on_target_scores[int(guide.guide_id)]

        return self
