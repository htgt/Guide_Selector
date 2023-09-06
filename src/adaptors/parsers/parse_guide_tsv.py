from typing import List

from utils.file_system import read_csv_to_list_dict
from mutator.guide import GuideSequence


def read_guide_tsv_to_guide_sequences(tsv: str) -> List[GuideSequence]:
    guide_data = read_csv_to_list_dict(tsv, delimiter='\t')
    guide_sequences = []
    for guide in guide_data:
        guide_sequence = GuideSequence(
            guide['chr'],
            int(guide['start']),
            int(guide['end']),
            is_positive_strand=(guide['grna_strand'] == '+'),
            guide_id=guide['guide_id'],
            ot_summary=eval(guide['ot_summary'])
        )
        guide_sequences.append(guide_sequence)
    return guide_sequences
