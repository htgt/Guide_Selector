from typing import List

from mutator.guide import GuideSequence
from utils.file_system import write_dict_list_to_csv


def write_guide_sequences_to_tsv(path: str, guide_sequences: List[GuideSequence]) -> None:
    tsv_rows = []
    for guide in guide_sequences:
        tsv_rows.append({
            'target_region_id': guide.target_region_id,
            'guide_id': guide.guide_id,
            'chr': guide.chromosome,
            'start': guide.start,
            'end': guide.end,
            'grna_strand': guide.strand_symbol,
            'ot_summary': guide.ot_summary,
        })

    write_dict_list_to_csv(path, tsv_rows, delimiter='\t')
