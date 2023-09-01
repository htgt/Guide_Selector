from src.cli import run_mutator_cmd, run_retrieve_cmd
import unittest


class TestRunCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {
            'ignore_positions': [1], 
            'allow_codon_loss': True,
            'species_id': '5',
            'assembly': 'TCGTCGTCGAAC',
        }
        self.args = {
            'gtf': './tests/fixtures/example_gtf.gtf',
            'tsv': './tests/fixtures/example_tsv.tsv',
            'region_file': './tests/fixtures/example_region_file.txt',
            'region': 'chr1:1-10001',
            'out_dir': './tests/fixtures',
        }
    
    # @unittest.mock.patch('cli.write_dict_list_to_csv')
    # @unittest.mock.patch('mutator.runner.write_to_vcf')
    # def test_run_mutator_cmd(self, mock_vcf_writer, mock_csv_writer):
    
    def test_run_mutator_cmd(self):
        # Arrange
        # mock_csv_writer.return_value = 'done'
        # mock_vcf_writer.return_value = 'done'
        # Act
        run_mutator_cmd(self.args, self.config)
        # Assert
        # assert mock_csv_writer.called
        # assert mock_vcf_writer.called