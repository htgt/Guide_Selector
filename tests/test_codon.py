from unittest import TestCase
from unittest.mock import Mock, patch

from codon import WindowCodon, get_third_base_on_positive_strand
from utils.exceptions import MutatorError


class TestWindowCodon(TestCase):
    def setUp(self):
        self.codon = Mock()
        self.codon.bases = 'ATT'
        self.codon.third_base_pos = 2
        self.codon.amino_acids_lost_from_edit = []
        self.codon.third_base_coord = 100
        self.config = {
            'ignore_positions': [-1, 1],
            'allow_codon_loss': False,
            'splice_mask_distance': 5,
        }

    def test_init_upper(self):
        # arrange
        mock_object = Mock()

        # act
        WindowCodon.__init__(mock_object, 'ATC', 3, 2, True)

        # assert
        self.assertEqual(mock_object._bases, 'ATC')

    def test_init_lower(self):
        # arrange
        mock_object = Mock()

        # act
        WindowCodon.__init__(mock_object, 'ctg', 3, 2, True)

        # assert
        self.assertEqual(mock_object._bases, 'CTG')

    def test_bases(self):
        # arrange
        mock_object = Mock()
        mock_object._bases = 'ATT'
        expected = 'ATT'

        # act
        actual = WindowCodon.bases.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_third_base_coord(self):
        # arrange
        mock_object = Mock()
        mock_object._third_base_coord = 3
        expected = 3

        # act
        actual = WindowCodon.third_base_coord.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_third_base_pos(self):
        # arrange
        mock_object = Mock()
        mock_object._third_base_pos = 2
        expected = 2

        # act
        actual = WindowCodon.third_base_pos.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_is_positive_strand(self):
        # arrange
        mock_object = Mock()
        mock_object._is_positive_strand = True

        # act
        actual = WindowCodon.is_positive_strand.fget(mock_object)

        # assert
        self.assertEqual(actual, True)

    def test_edited_bases_t(self):
        # arrange
        mock_object = Mock()
        mock_object.bases = 'ATT'
        expected = 'ATC'

        # act
        actual = WindowCodon.edited_bases.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_bases_c(self):
        # arrange
        mock_object = Mock()
        mock_object.bases = 'ATC'
        expected = 'ATT'

        # act
        actual = WindowCodon.edited_bases.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_bases_a(self):
        # arrange
        mock_object = Mock()
        mock_object.bases = 'ATA'
        expected = 'ATG'

        # act
        actual = WindowCodon.edited_bases.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_edited_bases_g(self):
        # arrange
        mock_object = Mock()
        mock_object.bases = 'ATG'
        expected = 'ATA'

        # act
        actual = WindowCodon.edited_bases.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_is_edit_permitted_true(self):
        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertTrue(actual)

    def test_is_edit_permitted_false_forbidden_codon(self):
        # arrange
        self.codon.bases = 'ATG'

        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertFalse(actual)

    def test_is_edit_permitted_false_window_position(self):
        # arrange
        self.codon.third_base_pos = 1

        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertFalse(actual)

    def test_is_edit_permitted_true_allow_codon_loss(self):
        # arrange
        self.codon.bases = 'AAG'
        self.codon.amino_acids_lost_from_edit = ['M']
        self.config['allow_codon_loss'] = True

        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertTrue(actual)

    def test_is_edit_permitted_false_not_allow_codon_loss(self):
        # arrange
        self.codon.bases = 'AAG'
        self.codon.amino_acids_lost_from_edit = ['M']

        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertFalse(actual)

    def test_is_edit_permitted_false_in_masked_region_start(self):
        # arrange
        self.codon.third_base_coord = 54

        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertFalse(actual)

    def test_is_edit_permitted_false_in_masked_region_end(self):
        # arrange
        self.codon.third_base_coord = 150

        # act
        actual = WindowCodon.is_edit_permitted(self.codon, self.config, 50, 150)

        # assert
        self.assertFalse(actual)

    def test_is_edit_permitted_raises_error_config_field_missing(self):
        # arrange
        config = {'ignore_positions': [-1, 1], 'allow_codon_loss': False}
        expected = 'Field missing from config'

        # act
        with self.assertRaises(MutatorError) as cm:
            WindowCodon.is_edit_permitted(self.codon, config, 50, 150)

        # assert
        self.assertEqual(str(cm.exception), expected)

    def test_amino_acids_lost_from_edit_edit_forbidden_codon(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'ATA'
        expected = []

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_missing_m(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'AAA'
        expected = ['M']

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_missing_i(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'CTG'
        expected = ['I']

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_missing_w(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'TAA'
        expected = ['W']

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_missing_stop(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'CGG'
        expected = ['*']

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_missing_m_and_w(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'AGA'
        expected = ['M', 'W']

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_missing_i_and_stop(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'AGG'
        expected = ['I', '*']

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    def test_amino_acids_lost_from_edit_none_missing(self):
        # arrange
        mock_object = Mock()
        mock_object.edited_bases = 'AGT'
        expected = []

        # act
        actual = WindowCodon.amino_acids_lost_from_edit.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)

    @patch('codon.get_third_base_on_positive_strand')
    def test_third_base_on_positive_strand_true(self, mock_func):
        # arrange
        mock_func.return_value = 'T'
        mock_object = Mock()
        mock_object.is_positive_strand = True
        mock_object.bases = 'ATT'
        expected = 'T'

        # act
        actual = WindowCodon.third_base_on_positive_strand.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)
        mock_func.assert_called_with('ATT', True)

    @patch('codon.get_third_base_on_positive_strand')
    def test_third_base_on_positive_strand_false(self, mock_func):
        # arrange
        mock_func.return_value = 'A'
        mock_object = Mock()
        mock_object.is_positive_strand = False
        mock_object.bases = 'ATT'
        expected = 'A'

        # act
        actual = WindowCodon.third_base_on_positive_strand.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)
        mock_func.assert_called_with('ATT', False)

    @patch('codon.get_third_base_on_positive_strand')
    def test_edited_third_base_on_positive_strand_true(self, mock_func):
        # arrange
        mock_func.return_value = 'C'
        mock_object = Mock()
        mock_object.is_positive_strand = True
        mock_object.edited_bases = 'ATC'
        expected = 'C'

        # act
        actual = WindowCodon.edited_third_base_on_positive_strand.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)
        mock_func.assert_called_with('ATC', True)

    @patch('codon.get_third_base_on_positive_strand')
    def test_edited_third_base_on_positive_strand_false(self, mock_func):
        # arrange
        mock_func.return_value = 'G'
        mock_object = Mock()
        mock_object.is_positive_strand = False
        mock_object.edited_bases = 'ATC'
        expected = 'G'

        # act
        actual = WindowCodon.edited_third_base_on_positive_strand.fget(mock_object)

        # assert
        self.assertEqual(actual, expected)
        mock_func.assert_called_with('ATC', False)


class TestGetThirdBaseOnPositiveStrand(TestCase):
    def test_get_third_base_on_positive_strand_true(self):
        # arrange
        expected = 'T'

        # act
        actual = get_third_base_on_positive_strand('ATT', True)

        # assert
        self.assertEqual(actual, expected)

    def test_get_third_base_on_positive_strand_false(self):
        # arrange
        expected = 'A'

        # act
        actual = get_third_base_on_positive_strand('ATT', False)

        # assert
        self.assertEqual(actual, expected)
