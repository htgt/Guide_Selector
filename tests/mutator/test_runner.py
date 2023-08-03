import unittest
from mutator.runner import Runner
from mutator.mutation_builder import MutationBuilder
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.coding_region import CodingRegion
from mutator.edit_window import EditWindow
from mutator.codon import WindowCodon
import pandas as pd
from pathlib import Path
from tdutils.utils.vcf_utils import write_to_vcf, Variants, Variant
from copy import copy

class RunnerTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = Runner({
            'ignore_positions': [-1, 1],
            'allow_codon_loss': True,
        })
        self.chrom = 'chr1'
        self.pos = 23
        self.third_base = 'A'
        self.alt_third_base = 'G'
        self.test_dir = '/test_dir'
        self.cds = BaseSequence(100, 200, True, '1', 1)
        self.window = EditWindow(150, 180, True, '1')
        self.guide = GuideSequence(
            guide_id=123,
            start=160,
            end=170,
            is_positive_strand=True,
            chromosome=self.chrom
        )
        self.gene_name = 'ACT'
        # self.codons = [WindowCodon('TCA', self.pos, 1, True)]
        self.mutation_builder=MutationBuilder(self.guide, self.cds, self.gene_name)
        self.variants = Variants(variant_list=
            [
                Variant(
                chrom=self.chrom,
                pos=self.pos,
                ref=self.third_base,
                alt=self.alt_third_base,
                info={'SGRNA': "sGRNA_XXXXX"}
                )
            ], 
            chrom=self.chrom
        )

    def test_as_row(self):
        config = {
            "ignore_positions": [-1, 1],
            "allow_codon_loss": True
        }
        mb = MutationBuilder(
            cds=BaseSequence(100, 200, True, '1', 1),
            guide=GuideSequence(
                start=160,
                end=170,
                is_positive_strand=True,
                guide_id=123,
                chromosome='1'
            ),
            gene_name='ACT'
        )
        mb.window = EditWindow(150, 180, True, '1'),
        mb.codons = [WindowCodon('TCA', 23, 1, True)]

        self.runner.mutation_builders = [mb]

        rows = self.runner.as_rows(config)

        expected_rows = [{
            'guide_id': 123,
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
        }]

        self.assertEqual(rows, expected_rows)

    def test_fill_guide_sequence(self):
        row = pd.Series({
            'guide_start': 160,
            'guide_end': 170,
            'guide_strand': '+',
            'chromosome': 'chr1',
            'cds_strand': '+',
            'guide_frame': 2
        })

        guide_sequence = self.runner.fill_guide_sequence(row)

        self.assertIsInstance(guide_sequence, GuideSequence)
        self.assertEqual(guide_sequence.start, 160)
        self.assertEqual(guide_sequence.end, 170)
        self.assertEqual(guide_sequence.chromosome, 'chr1')
        self.assertEqual(guide_sequence.is_positive_strand, True)
        self.assertEqual(guide_sequence.guide_id, None)  # Ensure guide_id is not set in the test

    def test_fill_coding_region(self):
        row = pd.Series({
            'cds_start': 100,
            'cds_end': 200,
            'chromosome': 'chr1',
            'cds_strand': '+',
            'exon_number': 1,
            'cds_frame': 1
        })

        coding_region = self.runner.fill_coding_region(row)

        self.assertIsInstance(coding_region, CodingRegion)
        self.assertEqual(coding_region.start, 100)
        self.assertEqual(coding_region.end, 200)
        self.assertEqual(coding_region.chromosome, 'chr1')
        self.assertEqual(coding_region.is_positive_strand, True)
        self.assertEqual(coding_region.exon_number, 1)
        self.assertEqual(coding_region.frame, 1)
        
    def test_to_variants_obj(self):
        # arrange
        self.runner.mutation_builders=[(self.mutation_builder)]
        expected_result = self.variants
        # act
        test_result = self.runner.to_variants_obj()
        # assert
        self.assertCountEqual(test_result._variants, expected_result._variants)
        self.assertEqual(test_result.header, expected_result.header)

    @unittest.mock.patch('mutator.runner.write_to_vcf')
    @unittest.mock.patch('mutator.runner.Runner.to_variants_obj')
    def test_write_output_to_vcf(self, mocked_write_to_vcf, mocked_transform_mutator_to_variants):
        # arrange
        expected_file_name = 'test_file'
        expected_file = expected_file_name + '.vcf'
        expected_file_path = Path(self.test_dir) / expected_file
        mocked_write_to_vcf.return_value = expected_file_path
        mocked_transform_mutator_to_variants.return_value = self.variants

        # act
        test_result = self.runner.write_output_to_vcf(expected_file_path)

        # assert
        self.assertEqual(test_result, str(expected_file_path))
        assert mocked_write_to_vcf.called
        assert mocked_transform_mutator_to_variants.called


if __name__ == '__main__':
    unittest.main()
