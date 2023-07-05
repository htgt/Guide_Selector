from unittest import TestCase
from unittest.mock import Mock

from mutator.codon import CodonEdit


class TestCodonEdit(TestCase):
    def test_init_upper(self):
        # arrange
        mock_object = Mock()
        expected = 'ATC'

        # act
        CodonEdit.__init__(mock_object, 'ATC')
        actual = mock_object._original_codon

        # assert
        self.assertEqual(actual, expected)

    def test_init_lower(self):
        # arrange
        mock_object = Mock()
        expected = 'CTG'

        # act
        CodonEdit.__init__(mock_object, 'ctg')
        actual = mock_object._original_codon

        # assert
        self.assertEqual(actual, expected)

    def test_original_codon(self):
        # arrange
        mock_object = Mock()
        mock_object._original_codon = 'ATT'
        expected = 'ATT'

        # act
        actual = CodonEdit.original_codon.fget(mock_object)

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

        # act
        actual = CodonEdit.is_permitted.fget(mock_object)

        # assert
        self.assertTrue(actual)

    def test_is_permitted_false(self):
        # arrange
        mock_object = Mock()
        mock_object.original_codon = 'ATG'

        # act
        actual = CodonEdit.is_permitted.fget(mock_object)

        # assert
        self.assertFalse(actual)

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
