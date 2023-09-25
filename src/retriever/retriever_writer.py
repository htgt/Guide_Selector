import os
from typing import List

from abstractions.writer import Writer
from adaptors.serialisers.serialise_guide_sequences import write_guide_sequences_to_tsv  # NOQA
from guide import GuideSequence

GUIDES_TSV_FILENAME = 'guides.tsv'


class RetrieverWriter(Writer):
    def __init__(self, guide_sequences: List[GuideSequence]):
        self._guide_sequences = guide_sequences

    def write_outputs(self, output_dir: str):
        output_path = os.path.join(output_dir, GUIDES_TSV_FILENAME)
        write_guide_sequences_to_tsv(output_path, self._guide_sequences)

        print('====================================')
        print('Guides retrieved: ', len(self._guide_sequences))
        print('Output saved to: ', output_path)
