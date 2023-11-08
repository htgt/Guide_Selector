import unittest

import pandas as pd
from tdutils.utils.vcf_utils import Variant, Variants

from base_sequence import BaseSequence
from coding_region import CodingRegion
from codon import WindowCodon
from edit_window import EditWindow
from guide import GuideSequence
from mutation_builder import MutationBuilder
from mutator.mutator import Mutator, _fill_coding_region, _fill_guide_sequence
from target_region import TargetRegion

from utils.warnings import NoGuidesRemainingWarning


class MutatorTestCase(unittest.TestCase):
    def setUp(self):
        # fmt: off
        self.mutator = Mutator({
            'ignore_positions': [-1, 1],
            'allow_codon_loss': True,
            'splice_mask_distance': 5,
        })  # fmt: on
        self.chrom = 'chr1'
        self.pos = 23
        self.third_base = 'A'
        self.alt_third_base = 'G'
        self.window_length = 12
        self.test_dir = '/test_dir'
        self.cds = BaseSequence(100, 200, True, 'chr1', 1)
        self.window = EditWindow(150, 180, self.window_length, True, '1')
        self.guide = GuideSequence(
            guide_id='123',
            start=160,
            end=170,
            is_positive_strand=True,
            chromosome=self.chrom,
            target_region=TargetRegion('chr1', None, None, '101'),
        )
        self.gene_name = 'ACT'
        self.target_region_id = '101'
        # self.codons = [WindowCodon('TCA', self.pos, 1, True)]

        self.mutation_builder = MutationBuilder(
            guide=self.guide, cds=self.cds, gene_name=self.gene_name, window_length=self.window_length
        )

        self.variants = Variants(
            variant_list=[
                Variant(
                    id='123',
                    chrom=self.chrom,
                    pos=self.pos,
                    ref=self.third_base,
                    alt=self.alt_third_base,
                    info={'SGRNA': "sgRNA_123"},
                )
            ],
            chroms=[self.chrom],
        )

    def test_fill_guide_sequence_only_required_fields(self):
        # fmt: off
        row = pd.Series({
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': '+',
            'chromosome': 'chr1',
            'cds_strand': '+',
            'guide_frame': 2
        })  # fmt: on

        guide_sequence = _fill_guide_sequence(row)

        self.assertIsInstance(guide_sequence, GuideSequence)
        self.assertEqual(guide_sequence.start, 160)
        self.assertEqual(guide_sequence.end, 170)
        self.assertEqual(guide_sequence.chromosome, 'chr1')
        self.assertEqual(guide_sequence.is_positive_strand, True)
        self.assertEqual(guide_sequence.guide_id, None)  # Ensure guide_id is not set in the test
        self.assertEqual(guide_sequence.ot_summary, None)
        self.assertEqual(guide_sequence.target_region, TargetRegion('chr1', None, None, ''))

    def test_fill_guide_sequence_with_all_fields(self):
        # fmt: off
        row = pd.Series({
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': '+',
            'chromosome': 'chr1',
            'cds_strand': '+',
            'guide_frame': 2,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'on_target_score': 0.86,
            'target_region_id': '101',
            'target_region_start': 100,
            'target_region_end': 200,
        })  # fmt: on

        guide_sequence = _fill_guide_sequence(row)

        self.assertIsInstance(guide_sequence, GuideSequence)
        self.assertEqual(guide_sequence.start, 160)
        self.assertEqual(guide_sequence.end, 170)
        self.assertEqual(guide_sequence.chromosome, 'chr1')
        self.assertEqual(guide_sequence.is_positive_strand, True)
        self.assertEqual(guide_sequence.guide_id, None)  # Ensure guide_id is not set in the test
        self.assertEqual(guide_sequence.ot_summary, {0: 1, 1: 0, 2: 0, 3: 4, 4: 76})
        self.assertEqual(guide_sequence.on_target_score, 0.86)
        self.assertEqual(guide_sequence.target_region, TargetRegion('chr1', 100, 200, '101'))

    def test_fill_coding_region(self):
        # fmt: off
        row = pd.Series({
            'cds_start': 100,
            'cds_end': 200,
            'chromosome': 'chr1',
            'cds_strand': '+',
            'exon_number': 1,
            'cds_frame': 1
        })  # fmt: on

        coding_region = _fill_coding_region(row)

        self.assertIsInstance(coding_region, CodingRegion)
        self.assertEqual(coding_region.start, 100)
        self.assertEqual(coding_region.end, 200)
        self.assertEqual(coding_region.chromosome, 'chr1')
        self.assertEqual(coding_region.is_positive_strand, True)
        self.assertEqual(coding_region.exon_number, 1)
        self.assertEqual(coding_region.frame, 1)

    def test_variants(self):
        # arrange
        mb_test = self.mutation_builder
        mb_test.window = self.window
        mb_test.codons = [
            WindowCodon('GAT', 123, 9, False),
        ]
        self.mutator.mutation_builders = [mb_test]
        expected_result = self.variants

        # act
        test_result = self.mutator.variants

        # assert
        self.assertEqual(test_result.__len__(), expected_result.__len__())
        self.assertEqual(test_result.header, expected_result.header)

    def test_filter_mutation_builders_all_guides_filtered(self):
        mb_test = self.mutation_builder
        self.mutator.mutation_builders = [mb_test]
        self.mutator._config = {
            "filters": {
                "min_edits_allowed": 123,
            }
        }

        with self.assertWarns(NoGuidesRemainingWarning):
            self.mutator._filter_mutation_builders()



if __name__ == '__main__':
    unittest.main()
