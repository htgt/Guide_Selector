from typing import List

from guide import GuideSequence
from utils.file_system import write_list_dict_in_tsv


def write_guide_sequences_to_tsv(path: str, guide_sequences: List[GuideSequence]) -> None:
    tsv_rows = []
    for guide in guide_sequences:
        serialised_guide = serialise_guide_sequence(guide)

        tsv_rows.append(serialised_guide)

    write_list_dict_in_tsv(path, tsv_rows)


def serialise_guide_sequence(guide: GuideSequence) -> dict:
    return {
        'target_region_id': guide.target_region.id,
        'chr': guide.chromosome,
        'target_region_start': guide.target_region.start,
        'target_region_end': guide.target_region.end,
        'guide_id': guide.guide_id,
        'guide_start': guide.start,
        'guide_end': guide.end,
        'guide_strand': guide.strand_symbol,
        'ot_summary': guide.ot_summary,
        'wge_percentile': guide.wge_percentile,
        'centrality_score': guide.centrality_score,
    }
