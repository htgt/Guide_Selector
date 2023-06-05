from typing import Tuple, List

import pyranges as pr
import pandas as pd

from utils.file_system import read_csv_to_list_dict
from utils.exceptions import MutatorError


class Mutator:
    def mutate(gtf: str, guide_tsv: str) -> None:
        gtf_data, guide_data = Mutator.read_input_files(gtf, guide_tsv)
        print(Mutator.get_coding_regions_for_all_guides(gtf_data, guide_data))

    def read_input_files(gtf: str, guide_tsv: str) -> Tuple[List[dict], pd.DataFrame]:
        gtf_data = pr.read_gtf(gtf, as_df=True)
        gtf_data['Start'] += 1  # pyranges uses 0-based coords
        guide_data = read_csv_to_list_dict(guide_tsv, delimiter='\t')
        return (gtf_data, guide_data)

    def get_coding_regions_for_all_guides(
        gtf_data: pd.DataFrame, guide_data: Tuple[List[dict]]
    ) -> pd.DataFrame:
        coding_regions = pd.DataFrame()
        for guide in guide_data:
            coding_region = Mutator.get_coding_region_for_guide(gtf_data, guide)
            coding_regions = pd.concat([coding_regions, coding_region])
        required_cols = [
            'Chromosome',
            'Start',
            'End',
            'gene_name',
            'exon_number',
            'Frame',
            'Strand'
        ]
        return coding_regions[required_cols].copy()

    def get_coding_region_for_guide(gtf_data: pd.DataFrame, guide: dict) -> pd.DataFrame:
        feature_cond = gtf_data['Feature'] == 'CDS'
        chrom_cond = gtf_data['Chromosome'] == guide['chr']
        start_cond = gtf_data['Start'] <= int(guide['end'])
        end_cond = gtf_data['End'] >= int(guide['start'])
        coding_region = gtf_data[feature_cond & chrom_cond & start_cond & end_cond].copy()
        if coding_region.empty:
            raise MutatorError(
                f'Guide {guide["guide_id"]} does not overlap with any coding regions'
            )
        if len(coding_region) > 1:
            raise MutatorError(
                f'Guide {guide["guide_id"]} overlaps with multiple coding regions'
            )
        coding_region['guide_id'] = int(guide['guide_id'])
        coding_region.set_index('guide_id', inplace=True)
        return coding_region
