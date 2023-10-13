import unittest

from adaptors.serialisers.mutation_builder_serialiser import serialise_mutation_builder
from coding_region import CodingRegion
from codon import WindowCodon
from guide import GuideSequence
from mutation_builder import MutationBuilder


class MutatorBuilderSerialiserTestCase(unittest.TestCase):
    def test_serialise_mutation_builder(self):
        mutation_builder = MutationBuilder(
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
        mutation_builder.codons = [
            WindowCodon(bases='TCA', third_base_coord=123, third_base_pos=1, is_positive_strand=True),
            WindowCodon(bases='TCC', third_base_coord=122, third_base_pos=2, is_positive_strand=False),
        ]

        config = {
            'ignore_positions': [-1, 1],
            'allow_codon_loss': True,
            'splice_mask_distance': 5,
        }

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
        },
        {
            'guide_id': '123',
            'alt': 'T',
            'chromosome': '1',
            'cds_strand': "+",
            'gene_name': 'ACT',
            'guide_strand': "+",
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
        }]  # fmt: on

        serialised_mb = serialise_mutation_builder(mutation_builder, config)

        self.assertEqual(serialised_mb, expected_serialisation)


if __name__ == '__main__':
    unittest.main()
