from unittest.mock import patch, Mock

from pyfakefs.fake_filesystem_unittest import TestCase

from config.config import prepare_config, Config


class TestPrepareConfig(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        default_contents = '''
        {
            "ignore_positions": [-1, 1],
            "allow_codon_loss": true,
            "splice_mask_distance": 5
        }
        '''
        self.fs.create_file('default_config.json', contents=default_contents)

    def test_config_prioritising_CLI_arguments(self):
        input_args = Mock()
        input_args.arguments = {
            'out_dir': 'CLI_out_dir',
            'on_target': 'CLI_on_target',
            'region_file': 'CLI_region_file',
            'region': 'CLI_region',
            'gtf': 'CLI_gtf',
            'tsv': 'CLI_tsv'
        }
        input_args.conf = 'conf'
        input_args.command = 'Command'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                "input_args": {
                    'out_dir': 'CONF_out_dir',
                    'on_target': 'CONF_on_target',
                    'region_file': 'CONF_region_file',
                    'region': 'CONF_region',
                    'gtf': 'CONF_gtf',
                    'tsv': 'CONF_tsv'
                },
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            result = Config(input_args)

            self.assertEqual(result.output_dir, 'CLI_out_dir')
            self.assertEqual(result.on_target, 'CLI_on_target')
            self.assertEqual(result.region_file, 'CLI_region_file')
            self.assertEqual(result.region, 'CLI_region')
            self.assertEqual(result.gtf, 'CLI_gtf')
            self.assertEqual(result.tsv, 'CLI_tsv')

            self.assertEqual(result.edit_rules, 'CONF_edit_rules')
            self.assertEqual(result.wge_species_id, 'CONF_wge_species_id')
            self.assertEqual(result.assembly, 'CONF_assembly')
            self.assertEqual(result.window_length, 'CONF_window_length')
            self.assertEqual(result.filters, {})
            self.assertEqual(result.ranking_priority_order, [])

    def test_config_when_no_CLI_arguments(self):
        input_args = Mock()
        input_args.arguments = {}
        input_args.conf = 'conf'
        input_args.command = 'command'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                "input_args": {
                    'out_dir': 'CONF_out_dir',
                    'on_target': 'CONF_on_target',
                    'region_file': 'CONF_region_file',
                    'region': 'CONF_region',
                    'gtf': 'CONF_gtf',
                    'tsv': 'CONF_tsv'
                },
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            result = Config(input_args)

            self.assertEqual(result.output_dir, 'CONF_out_dir')
            self.assertEqual(result.on_target, 'CONF_on_target')
            self.assertEqual(result.region_file, 'CONF_region_file')
            self.assertEqual(result.region, 'CONF_region')
            self.assertEqual(result.gtf, 'CONF_gtf')
            self.assertEqual(result.tsv, 'CONF_tsv')

            self.assertEqual(result.edit_rules, 'CONF_edit_rules')
            self.assertEqual(result.wge_species_id, 'CONF_wge_species_id')
            self.assertEqual(result.assembly, 'CONF_assembly')
            self.assertEqual(result.window_length, 'CONF_window_length')
            self.assertEqual(result.filters, {})
            self.assertEqual(result.ranking_priority_order, [])

    def test_config_when_no_CLI_nor_config_arguments(self):
        input_args = Mock()
        input_args.arguments = {}
        input_args.conf = 'conf'
        input_args.command = 'command'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            result = Config(input_args)

            self.assertEqual(result.output_dir, './')
            self.assertEqual(result.on_target, '')
            self.assertEqual(result.region_file, '')
            self.assertEqual(result.region, '')
            self.assertEqual(result.gtf, '')
            self.assertEqual(result.tsv, '')

            self.assertEqual(result.edit_rules, 'CONF_edit_rules')
            self.assertEqual(result.wge_species_id, 'CONF_wge_species_id')
            self.assertEqual(result.assembly, 'CONF_assembly')
            self.assertEqual(result.window_length, 'CONF_window_length')
            self.assertEqual(result.filters, {})
            self.assertEqual(result.ranking_priority_order, [])

    def test_config_when_no_region_nor_region_file_in_retriever_command(self):
        input_args = Mock()
        input_args.arguments = {
            'gtf': 'CLI_gtf'
        }
        input_args.conf = 'conf'
        input_args.command = 'retrieve'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            with self.assertRaises(ValueError) as error:
                Config(input_args)

            self.assertEqual(str(error.exception), '"region" or "region_file" is required to run retrieve')

    def test_config_when_no_tsv_in_mutator_command(self):
        input_args = Mock()
        input_args.arguments = {'gtf': 'CLI_gtf'}
        input_args.conf = 'conf'
        input_args.command = 'mutator'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            with self.assertRaises(ValueError) as error:
                Config(input_args)
            self.assertEqual(str(error.exception), '"tsv" is required to run mutator')

    def test_config_when_no_gtf_in_mutator_command(self):
        input_args = Mock()
        input_args.arguments = {}
        input_args.conf = 'conf'
        input_args.command = 'mutator'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            with self.assertRaises(ValueError) as error:
                Config(input_args)

            self.assertEqual(str(error.exception), '"gtf" is required to run mutator')

    def test_config_when_no_region_nor_region_file_in_guide_selector_command(self):
        input_args = Mock()
        input_args.arguments = {
            'gtf': 'CLI_gtf'
        }
        input_args.conf = 'conf'
        input_args.command = 'guide_selector'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            with self.assertRaises(ValueError) as error:
                Config(input_args)

            self.assertEqual(str(error.exception), '"region" or "region_file" is required to run guide_selector')

    def test_config_when_no_gtf_in_guide_selector_command(self):
        input_args = Mock()
        input_args.arguments = {'region': 'CLI_region'}
        input_args.conf = 'conf'
        input_args.command = 'guide_selector'

        with patch('config.config.prepare_config') as config_dict:
            config_dict.return_value = {
                'edit_rules': 'CONF_edit_rules',
                'wge_species_id': 'CONF_wge_species_id',
                'assembly': 'CONF_assembly',
                'window_length': 'CONF_window_length'
            }

            with self.assertRaises(ValueError) as error:
                Config(input_args)

            self.assertEqual(str(error.exception), '"gtf" is required to run guide_selector')

    @patch('config.config.DEFAULT_CONFIG_FILE', 'default_config.json')
    def test_prepare_config_default(self):
        # arrange
        expected = {
            'ignore_positions': [-1, 1],
            'allow_codon_loss': True,
            'splice_mask_distance': 5,
        }

        # act
        actual = prepare_config('')

        # assert
        self.assertEqual(expected, actual)

    @patch('config.config.DEFAULT_CONFIG_FILE', 'default_config.json')
    def test_prepare_config_custom(self):
        # arrange
        custom_contents = '''
        {
            "ignore_positions": [1],
            "splice_mask_distance": 4
        }
        '''
        self.fs.create_file('custom_config.json', contents=custom_contents)
        expected = {
            'ignore_positions': [1],
            'allow_codon_loss': True,
            'splice_mask_distance': 4,
        }

        # act
        actual = prepare_config('custom_config.json')

        # assert
        self.assertEqual(expected, actual)
