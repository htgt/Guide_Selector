import unittest

import pandas as pd
from tdutils.utils.vcf_utils import Variant, Variants

from base_sequence import BaseSequence
from coding_region import CodingRegion
from codon import WindowCodon
from edit_window import EditWindow
from guide import GuideSequence
from mutation_builder import MutationBuilder
from mutator.mutator import Mutator


class MutatorTestCase(unittest.TestCase):
    def setUp(self):
        self.mutator = Mutator({
            'ignore_positions': [-1, 1],
            'allow_codon_loss': True,
        })
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
            target_region_id='101',
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

    def test_guides_and_codons_without_ot_summary(self):
        mb = MutationBuilder(
            cds=BaseSequence(100, 200, True, '1', 1),
            guide=GuideSequence(
                start=160,
                end=170,
                is_positive_strand=True,
                guide_id='123',
                chromosome='1',
                target_region_id='101',
            ),
            gene_name='ACT',
            window_length=self.window_length,
        )
        mb.window = (EditWindow(150, 180, self.window_length, True, '1'),)
        mb.codons = [WindowCodon('TCA', 23, 1, True)]

        self.mutator.mutation_builders = [mb]

        rows = self.mutator.guides_and_codons

        expected_rows = [{
            'guide_id': '123',
            'alt': 'G',
            'chromosome': '1',
            'cds_strand': "+",
            'gene_name': 'ACT',
            'target_region_id': '101',
            'guide_strand': "+",
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 1,
            'pos': 23,
            'ref_codon': 'TCA',
            'ref_pos_three': 'A',
            'lost_amino_acids': 'N/A',
            'permitted': False,
            'ot_summary': None,
        }]

        self.assertEqual(rows, expected_rows)

    def test_guides_and_codons_with_ot_summary(self):
        mb = MutationBuilder(
            cds=BaseSequence(100, 200, True, '1', 1),
            guide=GuideSequence(
                start=160,
                end=170,
                is_positive_strand=True,
                guide_id='123',
                chromosome='1',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
                target_region_id='123456',
            ),
            gene_name='ACT',
            window_length=self.window_length,
        )
        mb.window = (EditWindow(150, 180, True, '1'),)
        mb.codons = [WindowCodon('TCA', 23, 1, True)]

        self.mutator.mutation_builders = [mb]

        rows = self.mutator.guides_and_codons

        expected_rows = [{
            'guide_id': '123',
            'alt': 'G',
            'chromosome': '1',
            'cds_strand': "+",
            'gene_name': 'ACT',
            'guide_strand': "+",
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 1,
            'pos': 23,
            'ref_codon': 'TCA',
            'ref_pos_three': 'A',
            'lost_amino_acids': 'N/A',
            'permitted': False,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'wge_percentile': 25,
        }]

        self.assertEqual(rows, expected_rows)

    def test_fill_guide_sequence_without_ot_summary(self):
        row = pd.Series({
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': '+',
            'chromosome': 'chr1',
            'cds_strand': '+',
            'guide_frame': 2
        })

        guide_sequence = self.mutator._fill_guide_sequence(row)

        self.assertIsInstance(guide_sequence, GuideSequence)
        self.assertEqual(guide_sequence.start, 160)
        self.assertEqual(guide_sequence.end, 170)
        self.assertEqual(guide_sequence.chromosome, 'chr1')
        self.assertEqual(guide_sequence.is_positive_strand, True)
        self.assertEqual(guide_sequence.guide_id, None)  # Ensure guide_id is not set in the test
        self.assertEqual(guide_sequence.ot_summary, None)

    def test_fill_guide_sequence_with_ot_summary(self):
        row = pd.Series({
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': '+',
            'chromosome': 'chr1',
            'cds_strand': '+',
            'guide_frame': 2,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76}
        })

        guide_sequence = self.mutator._fill_guide_sequence(row)

        self.assertIsInstance(guide_sequence, GuideSequence)
        self.assertEqual(guide_sequence.start, 160)
        self.assertEqual(guide_sequence.end, 170)
        self.assertEqual(guide_sequence.chromosome, 'chr1')
        self.assertEqual(guide_sequence.is_positive_strand, True)
        self.assertEqual(guide_sequence.guide_id, None)  # Ensure guide_id is not set in the test
        self.assertEqual(guide_sequence.ot_summary, {0: 1, 1: 0, 2: 0, 3: 4, 4: 76})

    def test_fill_coding_region(self):
        row = pd.Series({
            'cds_start': 100,
            'cds_end': 200,
            'chromosome': 'chr1',
            'cds_strand': '+',
            'exon_number': 1,
            'cds_frame': 1
        })

        coding_region = self.mutator._fill_coding_region(row)

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
            WindowCodon('GAT', 23, 9, False),
        ]
        self.mutator.mutation_builders = [mb_test]
        expected_result = self.variants

        # act
        test_result = self.mutator.variants

        # assert
        self.assertEqual(test_result.__len__(), expected_result.__len__())
        self.assertEqual(test_result.header, expected_result.header)


if __name__ == '__main__':
    unittest.main()
