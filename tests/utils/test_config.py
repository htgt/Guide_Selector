from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from utils.config import prepare_config


class TestPrepareConfig(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @patch('utils.config.DEFAULT_CONFIG_FILE', 'default_config.json')
    def test_prepare_config_default(self):
        # arrange
        contents = '{"ignore_positions": [-1, 1], "allow_codon_loss": true}'
        self.fs.create_file('default_config.json', contents=contents)
        expected = {'ignore_positions': [-1, 1], 'allow_codon_loss': True}

        # act
        actual = prepare_config('')

        # assert
        self.assertEqual(expected, actual)

    @patch('utils.config.DEFAULT_CONFIG_FILE', 'default_config.json')
    def test_prepare_config_custom(self):
        # arrange
        default_contents = '{"ignore_positions": [-1, 1], "allow_codon_loss": true}'
        custom_contents = '{"ignore_positions": [1]}'
        self.fs.create_file('default_config.json', contents=default_contents)
        self.fs.create_file('custom_config.json', contents=custom_contents)
        expected = {'ignore_positions': [1], 'allow_codon_loss': True}

        # act
        actual = prepare_config('custom_config.json')

        # assert
        self.assertEqual(expected, actual)
