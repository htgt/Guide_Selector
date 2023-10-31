import unittest

from mutation_builder import MutationBuilder
from coding_region import CodingRegion
from codon import WindowCodon
from guide import GuideSequence
from adaptors.serialisers.mutation_builder_serialiser import (
    convert_mutation_builders_to_df,
    extract_codon_details,
    _get_mutator_row,
    _get_codon_row,
)

class MutatorBuilderSerialiserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mutation_builder = MutationBuilder(
            guide=GuideSequence(
                chromosome='1',
                start=160,
                end=170,
                is_positive_strand=True,
                guide_id='123',
                target_region_id='101',
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
            'target_region_id', 'guide_id', 'chromosome', 'cds_strand',
            'gene_name', 'guide_strand', 'guide_start', 'guide_end',
            'ot_summary', 'wge_percentile', 'codon_details'
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

    def test_get_mutator_row(self):
        expected_row = {
            'target_region_id': '101',
            'guide_id': '123',
            'wge_percentile': 25,
            'valid_edits': 2,
            'chromosome': '1',
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': "+",
        }

        mutator_row = _get_mutator_row(self.mutation_builder)

        self.assertEqual(mutator_row, expected_row)

    def test_get_codon_row(self):
        expected_row = {
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

        codon_row = _get_codon_row(cds_start, cds_end, codon, self.config)

        self.assertEqual(codon_row, expected_row)

    def test_serialise_mutation_builder_when_no_filter_applied(self):
        expected_serialisation = {
            'target_region_id': '101',
            'guide_id': '123',
            'wge_percentile': 25,
            'valid_edits': 2,
            'chromosome': '1',
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': "+",
        }

        serialised_mb = serialise_mutation_builder(self.mutation_builder, self.config, filter_applied=None)
        print(serialised_mb)
        print(expected_serialisation)

        self.assertEqual(serialised_mb, expected_serialisation)

    def test_serialise_mutation_builder_when_filter_applied(self):
        # fmt: off
        expected_serialisation = {
            'target_region_id': '101',
            'guide_id': '123',
            'wge_percentile': 25,
            'valid_edits': 2,
            'chromosome': '1',
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': "+",
        }

        serialised_mb = serialise_mutation_builder(
            self.mutation_builder, self.config, filter_applied='filter_name'
        )

        self.assertEqual(serialised_mb, expected_serialisation)


if __name__ == '__main__':
    unittest.main()

    