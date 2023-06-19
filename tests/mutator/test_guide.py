from unittest import TestCase

from mutator.guide import GuideSequence, SequenceFragment


class TestGuideSequence(TestCase):
    def setUp(self):
        positive_bases = "AGTTTCGGACTCCTCCACAAGGT"
        self.test_positive_guide = GuideSequence(positive_bases, "+")
        self.pam_fragment_positive = SequenceFragment("AGG", 19, 22)

        negative_bases = "GCCATTGTCCGGGAGTCAGAAACT"
        self.test_negative_guide = GuideSequence(negative_bases, "-")
        self.pam_fragment_negative = SequenceFragment("CCA", 1, 4)


    def test_guide_find_pam_positive_strand(self):
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

