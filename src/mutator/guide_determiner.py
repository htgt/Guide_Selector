from typing import Tuple, List

import pyranges as pr
import pandas as pd

from utils.file_system import read_csv_to_list_dict
from utils.exceptions import GuideDeterminerError


class GuideDeterminer:
    def parse_loci(self, gtf: str, guide_tsv: str) -> None:
        gtf_data, guide_data = self.read_input_files(gtf, guide_tsv)
        coding_regions = self.get_coding_regions_for_all_guides(gtf_data, guide_data)
        coding_regions['guide_frame'] = coding_regions.apply(
            self.determine_frame_for_guide, axis=1
        )
        guide_frame_df = self.adjust_columns_for_output(coding_regions)
        print(guide_frame_df)
        return guide_frame_df

    def read_input_files(self, gtf: str, guide_tsv: str) -> Tuple[List[dict], pd.DataFrame]:
        gtf_data = pr.read_gtf(gtf, as_df=True)
        gtf_data['Start'] += 1  # pyranges uses 0-based coords
        guide_data = read_csv_to_list_dict(guide_tsv, delimiter="\t")
       
        for guide in guide_data:
            guide['chr'] = add_chr_prefix(guide['chr'])

        return (gtf_data, guide_data)

    def get_coding_regions_for_all_guides(
        self, gtf_data: pd.DataFrame, guide_data: List[dict]
    ) -> pd.DataFrame:
        coding_regions = pd.DataFrame()
        for guide in guide_data:
            try:
                coding_region = self.get_coding_region_for_guide(gtf_data, guide)
            except GuideDeterminerError as e:
                print(e)
                continue
            coding_region = self.add_guide_data_to_dataframe(coding_region, guide)
            coding_regions = pd.concat([coding_regions, coding_region])
        if coding_regions.empty:
            raise GuideDeterminerError(
                f'No coding regions found for any guides given.'
            )
        return coding_regions

    def get_coding_region_for_guide(self, gtf_data: pd.DataFrame, guide: dict) -> pd.DataFrame:
        feature_cond = gtf_data['Feature'] == 'CDS'
        chrom_cond = gtf_data['Chromosome'] == guide['chr']
        start_cond = gtf_data['Start'] <= int(guide['end'])
        end_cond = gtf_data['End'] >= int(guide['start'])
        coding_region = gtf_data[feature_cond & chrom_cond & start_cond & end_cond].copy()

        if coding_region.empty:
            raise GuideDeterminerError(
                f'Guide {guide["guide_id"]} does not overlap with any coding regions'
            )
        if len(coding_region) > 1:
            raise GuideDeterminerError(
                f'Guide {guide["guide_id"]} overlaps with multiple coding regions'
            )
        return coding_region

    def add_guide_data_to_dataframe(self, dataframe: pd.DataFrame, guide: dict) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dataframe['guide_id'] = int(guide['guide_id'])
        dataframe.set_index('guide_id', inplace=True)
        dataframe['guide_start'] = int(guide['start'])
        dataframe['guide_end'] = int(guide['end'])
        dataframe['guide_strand'] = str(guide['grna_strand'])
        return dataframe

    def determine_frame_for_guide(self, row: pd.Series) -> str:
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

    def adjust_columns_for_output(self, coding_regions: pd.DataFrame) -> pd.DataFrame:
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
            'guide_strand',
            'guide_start',
            'guide_end',
            'guide_frame',
        ]
        return coding_regions[required_cols].copy()
    
def add_chr_prefix(chromosome):
    if not chromosome.startswith('chr'):
        return 'chr' + chromosome
    return chromosome