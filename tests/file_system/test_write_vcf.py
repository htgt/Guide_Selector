import unittest
from pyfakefs.fake_filesystem_unittest import TestCase
from pathlib import Path
from src.utils.file_system import transform_tsv_to_variants
from td_utils.src.utils.file_system import read_csv

class TestWriteVCF(TestCase):
    test_dir = '/test_dir'
    def setUp(self):
        self.tsv_data = read_csv(r'tests/fixtures/ARTX_output_forbidden.tsv').to_list_dicts()
        self.setUpPyfakefs()
        self.fs.create_dir(self.test_dir)
        
    def test_transform_tsv_to_variants(self):
        # arrange   
        mock_tsv = Variant(
            CHROM='chr1',
            POS=1000, 
            REF='A', 
            ALT='G', 
            INFO={'SGRNA': "sGRNA_XXXXX"}
            )
        mock_chromosome = 'chr1'
        mock_data = Variants([mock_variant], mock_chromosome)
        expected_file_name = 'test_file'
        expected_file = expected_file_name + '.vcf'
        expected_file_path = Path(self.test_dir) / expected_file
        expected_result = {}
        

        # act
        test_file_path = OutputFilesData(self.test_dir).write_output(
            mock_data,
            expected_file,
            time_stamped=False,
        )
        test_data = read_vcf(test_file_path)._asdict()
        
        # assert
        self.assertEqual(test_file_path, expected_file_path)
        self.assertTrue(expected_file_path.exists())
        print(test_data)
        self.assertDictEqual(test_data, expected_result)
        
    @unittest.mock.patch('src.utils.vcf_utils.get_contig_length')
    def test_write_vcf(self, mocked_get_contig_length):
        # arrange   
        mocked_get_contig_length.return_value = 248956422
        mock_variant = Variant(
            CHROM='chr1',
            POS=1000, 
            REF='A', 
            ALT='G', 
            INFO={'SGRNA': "sGRNA_XXXXX"}
            )
        mock_chromosome = 'chr1'
        mock_data = Variants([mock_variant], mock_chromosome)
        expected_file_name = 'test_file'
        expected_file = expected_file_name + '.vcf'
        expected_file_path = Path(self.test_dir) / expected_file
        expected_result = {}
        

        # act
        test_file_path = OutputFilesData(self.test_dir).write_output(
            mock_data,
            expected_file,
            time_stamped=False,
        )
        test_data = read_vcf(test_file_path)._asdict()
        
        # assert
        self.assertEqual(test_file_path, expected_file_path)
        self.assertTrue(expected_file_path.exists())
        print(test_data)
        self.assertDictEqual(test_data, expected_result)


if __name__ == '__main__':
    unittest.main()
