from unittest import TestCase
from unittest.mock import Mock

from mutator.codon import CodonEdit
from utils.exceptions import MutatorError


class TestCodonEdit(TestCase):
    def test_init_upper(self):
        # arrange
        mock_object = Mock()

        # act
        CodonEdit.__init__(mock_object, 'ATC', 2)

        # assert
        self.assertEqual(mock_object._original_codon, 'ATC')
        self.assertEqual(mock_object._window_pos, 2)

    def test_init_lower(self):
        # arrange
        mock_object = Mock()

        # act
        CodonEdit.__init__(mock_object, 'ctg', 2)

        # assert
        self.assertEqual(mock_object._original_codon, 'CTG')
        self.assertEqual(mock_object._window_pos, 2)

    def test_original_codon(self):
        # arrange
        mock_object = Mock()
        mock_object._original_codon = 'ATT'
        expected = 'ATT'

        # act
        actual = CodonEdit.original_codon.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_window_pos(self):
        # arrange
        mock_object = Mock()
        mock_object._window_pos = 2
        expected = 2

        # act
        actual = CodonEdit.window_pos.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_codon_t(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATT'
        expected = 'ATC'

        # act
        actual = CodonEdit.edited_codon.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_codon_c(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATC'
        expected = 'ATT'

        # act
        actual = CodonEdit.edited_codon.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_codon_a(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATA'
        expected = 'ATG'

        # act
        actual = CodonEdit.edited_codon.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_codon_g(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATG'
        expected = 'ATA'

        # act
        actual = CodonEdit.edited_codon.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_is_permitted_true(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATT'
        mock_object.window_pos = 2
        mock_object.lost_amino_acids = []
        config = {'ignore_positions': [-1, 1], 'allow_codon_loss': False}

        # act
        actual = CodonEdit.is_permitted(mock_object, config)

        # assert
        self.assertTrue(actual)

    def test_is_permitted_false_forbidden_codon(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATG'
        mock_object.window_pos = 2
        mock_object.lost_amino_acids = []
        config = {'ignore_positions': [-1, 1], 'allow_codon_loss': False}

        # act
        actual = CodonEdit.is_permitted(mock_object, config)

        # assert
        self.assertFalse(actual)

    def test_is_permitted_false_window_position(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATT'
        mock_object.window_pos = 1
        mock_object.lost_amino_acids = []
        config = {'ignore_positions': [-1, 1], 'allow_codon_loss': False}

        # act
        actual = CodonEdit.is_permitted(mock_object, config)

        # assert
        self.assertFalse(actual)

    def test_is_permitted_true_allow_codon_loss(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'AAG'
        mock_object.window_pos = 2
        mock_object.lost_amino_acids = ['M']
        config = {'ignore_positions': [-1, 1], 'allow_codon_loss': True}

        # act
        actual = CodonEdit.is_permitted(mock_object, config)

        # assert
        self.assertTrue(actual)

    def test_is_permitted_false_not_allow_codon_loss(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'AAG'
        mock_object.window_pos = 2
        mock_object.lost_amino_acids = ['M']
        config = {'ignore_positions': [-1, 1], 'allow_codon_loss': False}

        # act
        actual = CodonEdit.is_permitted(mock_object, config)

        # assert
        self.assertFalse(actual)

    def test_is_permitted_raises_error_config_field_missing(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATT'
        mock_object.window_pos = 2
        mock_object.lost_amino_acids = []
        config = {'ignore_positions': [-1, 1]}
        expected = 'Field missing from config'

        # act
        with self.assertRaises(MutatorError) as cm:
            CodonEdit.is_permitted(mock_object, config)

        # assert
        self.assertEqual(str(cm.exception), expected)

    def test_lost_amino_acids_edit_forbidden_codon(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'ATA'
        expected = []

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_missing_m(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'AAA'
        expected = ['M']

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_missing_i(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'CTG'
        expected = ['I']

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_missing_w(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'TAA'
        expected = ['W']

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_missing_stop(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'CGG'
        expected = ['*']

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_missing_m_and_w(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'AGA'
        expected = ['M', 'W']

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_missing_i_and_stop(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'AGG'
        expected = ['I', '*']

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_lost_amino_acids_none_missing(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_codon = 'AGT'
        expected = []

        # act
        actual = CodonEdit.lost_amino_acids.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)
