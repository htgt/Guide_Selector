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

        guide = GuideSequence(67626582, 67626594, is_positive_strand=True)
        pam = SequenceFragment("AGG", 67626592, 67626594)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam)
