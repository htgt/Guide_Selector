from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from config.config import prepare_config


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
