import unittest
from pyfakefs.fake_filesystem_unittest import TestCase
from pathlib import Path
from src.utils.file_system import transform_mutator_to_variants, write_mutator_to_vcf
from src.mutator.runner import Runner, mutator_to_dict_list
from src.mutator.base_sequence import BaseSequence
from src.mutator.guide import GuideSequenceLoci
from src.mutator.edit_window import EditWindow, WindowCodon, BaseWithPosition
from td_utils.src.vcf_utils import read_vcf, Variants, Variant


class TestWriteVCF(TestCase):
    test_dir = '/test_dir'

    def setUp(self):
        self.runner = Runner()
        self.setUpPyfakefs()
        self.fs.create_dir(self.test_dir)
        self.runner.cds = BaseSequence(100, 200, True, '1', 1)
        self.runner.window = EditWindow(150, 180, True, '1')
        self.runner.guide = GuideSequenceLoci(
            guide_id=123,
            start=160,
            end=170,
            isPositiveStrand=True,
            chromosome='1'
        )
        self.runner.gene_name = 'ACT'
        self.runner.codons = [WindowCodon('TCA', BaseWithPosition('A', 23, 1))]
        self.variant = Variant(
            CHROM=self.runner.guide.chromosome,
            POS=self.runner.codons[0].third.coordinate,
            REF=self.runner.codons[0].third.base,
            ALT='G',
            INFO={'SGRNA': "sGRNA_XXXXX"}
        )
        self.variants = Variants([self.variant], self.runner.guide.chromosome)
        
    def test_transform_mutator_to_variants(self):
        # arrange
        test_runner = self.runner
        expected_result = self.variants
        # act
        test_result = test_runner.to_variants()
        # assert
        self.assertEqual(test_result, expected_result)

    @unittest.mock.patch('src.utils.file_system.write_to_vcf')
    @unittest.mock.patch('src.utils.file_system.transform_mutator_to_variants')
    def test_write_mutator_to_vcf(self, mocked_write_to_vcf, mocked_transform_mutator_to_variants):
        # arrange
        test_data = [self.runner]
        expected_file_name = 'test_file'
        expected_file = expected_file_name + '.vcf'
        expected_file_path = Path(self.test_dir) / expected_file
        mocked_write_to_vcf.return_value = expected_file_path
        mocked_transform_mutator_to_variants.return_value = self.variants

        # act
        test_result = write_mutator_to_vcf(expected_file_path, test_data)

        # assert
        self.assertEqual(test_result, expected_file_path)
        assert mocked_write_to_vcf.called()
        assert mocked_transform_mutator_to_variants.called()


if __name__ == '__main__':
    unittest.main()
