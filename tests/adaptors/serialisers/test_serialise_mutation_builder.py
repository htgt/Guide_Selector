import unittest
from unittest.mock import patch, PropertyMock

from adaptors.serialisers.mutation_builder_serialiser import (
    convert_mutation_builders_to_df,
    extract_codon_details,
    _get_mutation_builder_dict,
    _get_codon_dict,
)
from coding_region import CodingRegion
from codon import WindowCodon
from guide import GuideSequence
from mutation_builder import MutationBuilder
from target_region import TargetRegion


class MutatorBuilderSerialiserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mutation_builder = MutationBuilder(
            guide=GuideSequence(
                chromosome='1',
                start=160,
                end=170,
                is_positive_strand=True,
                guide_id='123',
                target_region=TargetRegion('1', 100, 200, '101'),
                frame=0,  # to be replaced by FragmentFrameIndicator.ZERO
                ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            ),
            cds=CodingRegion(start=100, end=200, is_positive_strand=True, chromosome='1', frame=0, exon_number=0),
            gene_name='ACT',
            window_length=12,
        )
        self.mutation_builder.codons = [
            WindowCodon(bases='TCA', third_base_coord=123, third_base_pos=1, is_positive_strand=True),
            WindowCodon(bases='TCC', third_base_coord=122, third_base_pos=2, is_positive_strand=False),
        ]

        self.config = {
            'ignore_positions': [-1, 1],
            'allow_codon_loss': True,
            'splice_mask_distance': 5,
        }

    def test_convert_mutation_builders_to_df(self):
        expected_columns = [
            'target_region_id',
            'guide_id',
            'chromosome',
            'cds_strand',
            'gene_name',
            'guide_strand',
            'guide_start',
            'guide_end',
            'ot_summary',
            'wge_percentile',
            'on_target_score',
            'centrality_score',
            'codon_details',
        ]

        df = convert_mutation_builders_to_df([self.mutation_builder], self.config)

        self.assertEqual(list(df.columns), expected_columns)

    def test_extract_codon_details(self):
        expected_codon_details = [
            {
                'window_pos': 1,
                'pos': 123,
                'ref_codon': 'TCA',
                'ref_pos_three': 'A',
                'alt': 'G',
                'lost_amino_acids': 'N/A',
                'permitted': False,
            },
            {
                'window_pos': 2,
                'pos': 122,
                'ref_codon': 'TCC',
                'ref_pos_three': 'C',
                'alt': 'T',
                'lost_amino_acids': 'N/A',
                'permitted': True,
            }
        ]

        codon_details = extract_codon_details(self.mutation_builder, self.config)

        self.assertEqual(codon_details, expected_codon_details)

    @patch('guide.GuideSequence.centrality_score', new_callable=PropertyMock, return_value=0.5)
    def test_get_mutation_builder_dict(self, mock):
        expected_mb_dict = {
            'guide_id': '123',
            'wge_percentile': 25,
            'valid_edits': 2,
            'chromosome': '1',
            'guide_start': 160,
            'guide_end': 170,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'target_region_id': '101',
            'wge_percentile': 25,
            'centrality_score': 0.5,
            'on_target_score': 'N/A',
        }

        result = _get_mutation_builder_dict(self.mutation_builder)

        self.assertEqual(result, expected_mb_dict)

    def test_get_codon_dict(self):
        expected_codon_dict = {
            'window_pos': 1,
            'pos': 123,
            'ref_codon': 'TCA',
            'ref_pos_three': 'A',
            'alt': 'G',
            'lost_amino_acids': 'N/A',
            'permitted': False,
        }

        cds_start = 100
        cds_end = 200
        codon = WindowCodon(bases='TCA', third_base_coord=123, third_base_pos=1, is_positive_strand=True)

        result = _get_codon_dict(cds_start, cds_end, codon, self.config)

        self.assertEqual(result, expected_codon_dict)

    @patch('guide.GuideSequence.centrality_score', new_callable=PropertyMock, return_value=0.5)
    def test_serialise_mutation_builder_no_on_target_score_or_filter_applied(self, mock):
        # fmt: off
        expected_serialisation = [{
            'guide_id': '123',
            'alt': 'G',
            'chromosome': '1',
            'cds_strand': "+",
            'gene_name': 'ACT',
            'guide_strand': "+",
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 1,
            'pos': 123,
            'ref_codon': 'TCA',
            'ref_pos_three': 'A',
            'lost_amino_acids': 'N/A',
            'permitted': False,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'target_region_id': '101',
            'wge_percentile': 25,
            'centrality_score': 0.5,
            'on_target_score': 'N/A',
        },
        {
            'guide_id': '123',
            'wge_percentile': 25,
            'valid_edits': 2,
            'chromosome': '1',
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 2,
            'pos': 122,
            'ref_codon': 'TCC',
            'ref_pos_three': 'C',
            'lost_amino_acids': 'N/A',
            'permitted': True,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'target_region_id': '101',
            'wge_percentile': 25,
            'centrality_score': 0.5,
            'on_target_score': 'N/A',
        }]  # fmt: on

        serialised_mb = serialise_mutation_builder(self.mutation_builder, self.config, filter_applied=None)
        print(serialised_mb)
        print(expected_serialisation)

        self.assertEqual(serialised_mb, expected_serialisation)

    @patch('guide.GuideSequence.centrality_score', new_callable=PropertyMock, return_value=0.5)
    def test_serialise_mutation_builder_all_fields(self, mock):
        # fmt: off
        expected_serialisation = [{
            'guide_id': '123',
            'alt': 'G',
            'chromosome': '1',
            'cds_strand': "+",
            'gene_name': 'ACT',
            'guide_strand': "+",
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 1,
            'pos': 123,
            'ref_codon': 'TCA',
            'ref_pos_three': 'A',
            'lost_amino_acids': 'N/A',
            'permitted': False,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'target_region_id': '101',
            'wge_percentile': 25,
            'centrality_score': 0.5,
            'filter_applied': 'filter_name',
            'on_target_score': 0.86,
        },
        {
            'guide_id': '123',
            'wge_percentile': 25,
            'valid_edits': 2,
            'chromosome': '1',
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 2,
            'pos': 122,
            'ref_codon': 'TCC',
            'ref_pos_three': 'C',
            'lost_amino_acids': 'N/A',
            'permitted': True,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'target_region_id': '101',
            'wge_percentile': 25,
            'centrality_score': 0.5,
            'filter_applied': 'filter_name',
            'on_target_score': 0.86,
        }]  # fmt: on

        self.mutation_builder.guide.on_target_score = 0.86
        serialised_mb = serialise_mutation_builder(self.mutation_builder, self.config, filter_applied='filter_name')

        self.assertEqual(serialised_mb, expected_serialisation)


if __name__ == '__main__':
    unittest.main()

    