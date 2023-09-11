from ast import literal_eval
from typing import List

from utils.file_system import read_csv_to_list_dict
from mutator.guide import GuideSequence


def read_guide_tsv_to_guide_sequences(tsv: str) -> List[GuideSequence]:
    guide_data = read_csv_to_list_dict(tsv, delimiter='\t')

    guide_sequences = []
    for guide in guide_data:
        guide_sequence = GuideSequence(
            chromosome=guide['chr'],
            start=int(guide['start']),
            end=int(guide['end']),
            is_positive_strand=(guide['grna_strand'] == '+'),
            guide_id=guide['guide_id'],
            ot_summary=literal_eval(guide['ot_summary']) if 'ot_summary' in guide else None,
            target_region_id=guide['target_region_id'],
        )
        guide_sequences.append(guide_sequence)

    return guide_sequences
