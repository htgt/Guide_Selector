import os
from typing import List

from abstractions.writer import Writer
from adaptors.serialisers.guide_sequences_serialiser import write_guide_sequences_to_tsv
from guide import GuideSequence


class RetrieverWriter(Writer):
    guides_tsv_filename = 'guides.tsv'

    def __init__(self, guide_sequences: List[GuideSequence]):
        self._guide_sequences = guide_sequences

    def write_outputs(self, output_dir: str):
        output_path = os.path.join(output_dir, RetrieverWriter.guides_tsv_filename)
        write_guide_sequences_to_tsv(output_path, self._guide_sequences)

        print('====================================')
        print('Guides retrieved: ', len(self._guide_sequences))
        print('Output saved to: ', output_path)
