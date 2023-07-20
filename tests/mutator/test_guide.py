from unittest import TestCase, mock
from unittest.mock import patch
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence, SequenceFragment




class TestGuideSequence(TestCase):
    def setUp(self):
        positive_bases = "AGTTTCGGACTCCTCCACAAGGT"
        negative_bases = "GCCATTGTCCGGGAGTCAGAAACT"

        def mock_get_sequence_by_coords_positive(chromosome, start, end):
            return positive_bases

        def mock_get_sequence_by_coords_negative(chromosome, start, end):
            return negative_bases

        with patch.object(BaseSequence, '_get_sequence_by_coords',
            side_effect=mock_get_sequence_by_coords_positive):

            self.test_positive_guide = GuideSequence(0, 1, is_positive_strand=True)
            self.pam_fragment_positive = SequenceFragment("AGG", 19, 22)

        with patch.object(BaseSequence, '_get_sequence_by_coords',
            side_effect=mock_get_sequence_by_coords_negative):

            self.test_negative_guide = GuideSequence(0, 1, is_positive_strand=False)
            self.pam_fragment_negative = SequenceFragment("CCA", 1, 4)


    def testguide_find_pam_positive_strand(self):
        guide = self.test_positive_guide

        test_pam = guide.find_pam()

        self.assertEqual(test_pam, self.pam_fragment_positive)


    def test_guide_find_pam_negative_strand(self):
        guide = self.test_negative_guide

        test_pam = guide.find_pam()

        self.assertEqual(test_pam, self.pam_fragment_negative)


    def test_define_window_positive_strand(self):
        window = SequenceFragment("TCCTCCACAAGG", 10, 22)

        guide = self.test_positive_guide

        test_window = guide.define_window()

        self.assertEqual(test_window, window)


    def test_define_window_negative_strand(self):
        window = SequenceFragment("CCATTGTCCGGGAGT", 1, 16)

        guide = self.test_negative_guide

        test_window = guide.define_window()

        self.assertEqual(test_window, window)

