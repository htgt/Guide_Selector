from typing import Tuple, List

import pyranges as pr
import pandas as pd

from utils.file_system import read_csv_to_list_dict
from utils.exceptions import MutatorError


class Mutator:
    def mutate(gtf: str, guide_tsv: str) -> None:
        gtf_data, guide_data = Mutator.read_input_files(gtf, guide_tsv)
        coding_regions = Mutator.get_coding_regions_for_all_guides(gtf_data, guide_data)
        coding_regions['guide_frame'] = coding_regions.apply(
            Mutator.determine_frame_for_guide, axis=1
        )
        print(Mutator.adjust_columns_for_output(coding_regions))

    def read_input_files(gtf: str, guide_tsv: str) -> Tuple[List[dict], pd.DataFrame]:
        gtf_data = pr.read_gtf(gtf, as_df=True)
        gtf_data['Start'] += 1  # pyranges uses 0-based coords
        guide_data = read_csv_to_list_dict(guide_tsv, delimiter='\t')
        return (gtf_data, guide_data)

    def get_coding_regions_for_all_guides(
        gtf_data: pd.DataFrame, guide_data: List[dict]
    ) -> pd.DataFrame:
        coding_regions = pd.DataFrame()
        for guide in guide_data:
            coding_region = Mutator.get_coding_region_for_guide(gtf_data, guide)
            coding_region = Mutator.add_guide_data_to_dataframe(coding_region, guide)
            coding_regions = pd.concat([coding_regions, coding_region])
        return coding_regions

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
        return coding_region

    def add_guide_data_to_dataframe(dataframe: pd.DataFrame, guide: dict) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dataframe['guide_id'] = int(guide['guide_id'])
        dataframe.set_index('guide_id', inplace=True)
        dataframe['guide_start'] = int(guide['start'])
        dataframe['guide_end'] = int(guide['end'])
        return dataframe

    def determine_frame_for_guide(row: pd.Series) -> str:
        if row['Strand'] == '+':
            if row['guide_start'] < row['Start']:
                return row['Frame']
            difference = row['guide_start'] - row['Start']
        else:
            if row['guide_end'] > row['End']:
                return row['Frame']
            difference = row['End'] - row['guide_end']
        frames = ('0', '2', '1')
        return frames[(difference + int(frames.index(row['Frame']))) % 3]

    def adjust_columns_for_output(coding_regions: pd.DataFrame) -> pd.DataFrame:
        coding_regions.rename(
            columns={
                'Chromosome': 'chromosome',
                'Start': 'cds_start',
                'End': 'cds_end',
                'Strand': 'cds_strand',
                'Frame': 'cds_frame',
            },
            inplace=True
        )
        required_cols = [
            'chromosome',
            'cds_start',
            'cds_end',
            'cds_strand',
            'cds_frame',
            'gene_name',
            'exon_number',
            'guide_start',
            'guide_end',
            'guide_frame',
        ]
        return coding_regions[required_cols].copy()