from ast import literal_eval
from typing import List

from guide import GuideSequence
from utils.file_system import read_tsv_to_list_dict


def read_guide_tsv_to_guide_sequences(tsv_file: str) -> List[GuideSequence]:
    guide_data = read_tsv_to_list_dict(tsv_file)
    guide_sequences = []
    for guide in guide_data:
        guide_sequences.append(deserialise_guide_sequence(guide))
    return guide_sequences


def deserialise_guide_sequence(guide: dict) -> GuideSequence:
    return GuideSequence(
        chromosome=guide['chr'],
        start=int(guide['start']),
        end=int(guide['end']),
        is_positive_strand=(guide['grna_strand'] == '+'),
        guide_id=guide['guide_id'],
        ot_summary=literal_eval(guide['ot_summary']) if 'ot_summary' in guide else None,
        target_region_id=guide.get('target_region_id'),
        on_target_score=guide['on_target_score'] if 'on_target_score' in guide else None,
    )
