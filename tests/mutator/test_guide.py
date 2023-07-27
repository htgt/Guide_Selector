from unittest import TestCase, mock
from unittest.mock import patch
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence, SequenceFragment


class TestGuideSequence(TestCase):
    def test_guide_find_pam_real_coords_positive_strand(self):
        bases = "ATATTGAGCAAGG"

        guide = GuideSequence(67626582, 67626594, is_positive_strand=True)
        pam = SequenceFragment("AGG", 67626592, 67626594)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam)

    def test_guide_find_pam_negative_strand(self):
        bases = "GCCATTGTCCGGGAGTCAGAAACT"
        guide = GuideSequence(0, 22, is_positive_strand=False)

        pam_fragment_negative = SequenceFragment("CCA", 1, 3)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam_fragment_negative)
