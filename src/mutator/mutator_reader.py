from abstractions.reader import Reader
from adaptors.parsers.parse_guide_tsv import read_guide_tsv_to_guide_sequences
from adaptors.parsers.parse_on_target_score_tsv import get_guides_on_target_scores
from config.config import Config
from utils.file_system import read_gtf_to_df


class MutatorReader(Reader):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.gtf_data = None
        self.guide_sequences = []

    def read_inputs(self, guide_sequences=None) -> Reader:
        self.gtf_data = read_gtf_to_df(self._config.gtf)
        self.guide_sequences = guide_sequences or read_guide_tsv_to_guide_sequences(self._config.tsv)

        if on_target_scores := get_guides_on_target_scores(self._config.on_target):
            for guide in self.guide_sequences:
                guide.on_target_score = on_target_scores[int(guide.guide_id)]

        return self
