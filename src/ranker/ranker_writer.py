import pandas as pd
from os import path

from abstractions.writer import Writer

RANKED_FILENAME = 'ranked_guides_and_codons.tsv'


class RankerWriter(Writer):

    def __init__(self, df: pd.DataFrame) -> None:
        self._data = df
        self._output_file_path = RANKED_FILENAME

    def write_outputs(self, dir):
        file_path = path.join(dir, self._output_file_path)

        self._data.to_csv(file_path, index_label='ranking')

        print('Output saved to ', file_path)
