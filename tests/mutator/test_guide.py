from unittest import TestCase, mock
from unittest.mock import patch
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence, SequenceFragment, calculate_window_coordinates


class TestGuideSequence(TestCase):
    def setUp(self):
        positive_bases = "AGTTTCGGACTCCTCCACAAGGT"
        negative_bases = "GCCATTGTCCGGGAGTCAGAAACT"

        def mock_get_sequence_by_coords_positive(chromosome, start, end):
            return positive_bases

        def mock_get_sequence_by_coords_negative(chromosome, start, end):
            return negative_bases

        with patch.object(
            BaseSequence,
            '_get_sequence_by_coords',
            side_effect=mock_get_sequence_by_coords_positive
        ):

            self.test_positive_guide = GuideSequence(0, 22, is_positive_strand=True)
            self.pam_fragment_positive = SequenceFragment("AGG", 19, 22)

        with patch.object(
            BaseSequence,
            '_get_sequence_by_coords',
            side_effect=mock_get_sequence_by_coords_negative
        ):

            self.test_negative_guide = GuideSequence(0, 22, is_positive_strand=False)
            self.pam_fragment_negative = SequenceFragment("CCA", 1, 4)



    def test_guide_find_pam_real_coords_positive_strand(self):
        bases = "ATATTGAGCAAGG"

        def mock_get_sequence_by_coords(chromosome, start, end):
            return bases

        with patch.object(BaseSequence, '_get_sequence_by_coords',
                side_effect=mock_get_sequence_by_coords):

            guide = GuideSequence(67626582, 67626594, is_positive_strand=True)
            pam = SequenceFragment("AGG", 67626592, 67626594)

            test_pam = guide.find_pam()

            self.assertEqual(test_pam, pam)


class TestCalculateWindowCoordinates(TestCase):
    def test_calculate_window_coords(self):
        #bases = "CAGCATTCCTATATTGAGCAAGG"
        bases = "ATATTGAGCAAGG"
        #guide_start = 67626572
        guide_start = 67626582
        guide_end = 67626594

        def mock_get_sequence_by_coords(chromosome, start, end):
            return bases

        window_start = 67626583
        window_end = 67626594

        with patch.object(
                BaseSequence,
                '_get_sequence_by_coords',
                side_effect=mock_get_sequence_by_coords
        ):
            guide = GuideSequence(guide_start, guide_end, is_positive_strand=True)
            result_window = calculate_window_coordinates(guide)

        self.assertEqual(result_window, (window_start, window_end))
