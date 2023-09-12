from typing import List

import pandas as pd

from utils.exceptions import GuideDeterminerError
from mutator.guide import GuideSequence


class GuideDeterminer:
    def parse_loci(self, gtf_data: pd.DataFrame, guide_sequences: List[GuideSequence]) -> pd.DataFrame:
        coding_regions = self.get_coding_regions_for_all_guides(gtf_data, guide_sequences)
        coding_regions['guide_frame'] = coding_regions.apply(
            self.determine_frame_for_guide, axis=1
        )
        guide_frame_df = self.adjust_columns_for_output(coding_regions)

        return guide_frame_df

    def get_coding_regions_for_all_guides(
        self, gtf_data: pd.DataFrame, guide_sequences: List[GuideSequence]
    ) -> pd.DataFrame:
        coding_regions = pd.DataFrame()
        for guide in guide_sequences:
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

    def get_coding_region_for_guide(
        self, gtf_data: pd.DataFrame, guide: GuideSequence
    ) -> pd.DataFrame:
        feature_cond = gtf_data['Feature'] == 'CDS'
        chrom_cond = gtf_data['Chromosome'] == guide.chromosome
        start_cond = gtf_data['Start'] <= guide.end
        end_cond = gtf_data['End'] >= guide.start
        coding_region = gtf_data[feature_cond & chrom_cond & start_cond & end_cond].copy()

        if coding_region.empty:
            raise GuideDeterminerError(
                f'Guide {guide.guide_id} does not overlap with any coding regions'
            )
        if len(coding_region) > 1:
            raise GuideDeterminerError(
                f'Guide {guide.guide_id} overlaps with multiple coding regions'
            )
        return coding_region

    def add_guide_data_to_dataframe(
        self, dataframe: pd.DataFrame, guide: GuideSequence
    ) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dataframe['guide_id'] = guide.guide_id
        dataframe.set_index('guide_id', inplace=True)
        dataframe['guide_start'] = guide.start
        dataframe['guide_end'] = guide.end
        dataframe['guide_strand'] = guide.strand_symbol
        dataframe['target_region_id'] = guide.target_region_id
        dataframe['ot_summary'] = str(guide.ot_summary)
        return dataframe

    def determine_frame_for_guide(self, row: pd.Series) -> int:
        if row['Strand'] == '+':
            difference = row['guide_start'] - row['Start']
        else:
            difference = row['End'] - row['guide_end']

        frames = (0, 2, 1)

        return frames[(difference + int(frames.index(int(row['Frame'])))) % 3]

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
            'ot_summary',
            'target_region_id',
        ]

        return coding_regions[required_cols].copy()
