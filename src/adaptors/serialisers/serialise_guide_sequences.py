from typing import List

from guide import GuideSequence
from utils.file_system import write_list_dict_in_tsv


def write_guide_sequences_to_tsv(path: str, guide_sequences: List[GuideSequence]) -> None:
    tsv_rows = []
    for guide in guide_sequences:
        tsv_rows.append(serialise_guide_sequence(guide))

    write_list_dict_in_tsv(path, tsv_rows)


def serialise_guide_sequence(guide: GuideSequence) -> dict:
    return {
        'target_region_id': guide.target_region_id,
        'guide_id': guide.guide_id,
        'chr': guide.chromosome,
        'start': guide.start,
        'end': guide.end,
        'grna_strand': guide.strand_symbol,
        'ot_summary': guide.ot_summary,
    }
