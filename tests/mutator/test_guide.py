from unittest import TestCase
from unittest.mock import Mock
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence, SequenceFragment


class TestGuideSequence(TestCase):
    def test_strand_symbol_positive(self):
        # arrange
        mock_obj = Mock(is_positive_strand=True)
        expected = '+'

        # act
        actual = GuideSequence.strand_symbol.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_strand_symbol_negative(self):
        # arrange
        mock_obj = Mock(is_positive_strand=False)
        expected = '-'

        # act
        actual = GuideSequence.strand_symbol.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_guide_find_pam_real_coords_positive_strand(self):
        bases = "ATATTGAGCAAGG"

        guide = GuideSequence('chr16', 67626582, 67626594, is_positive_strand=True)
        pam = SequenceFragment("AGG", 67626592, 67626594)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam)

    def test_guide_find_pam_negative_strand(self):
        bases = "GCCATTGTCCGGGAGTCAGAAACT"
        guide = GuideSequence('chr1', 0, 22, is_positive_strand=False)

        pam_fragment_negative = SequenceFragment("CCA", 1, 3)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam_fragment_negative)
