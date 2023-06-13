from unittest import TestCase

from mutator.guide import GuideSequence, SequenceFragment

class TestGuideSequence(TestCase):
    def setUp(self):
        positive_bases = "AGTTTCGGACTCCTCCACAATGGCT"
        self.test_positive_guide = GuideSequence(positive_bases, "+")

        pam = "TGG"
        pam_start = 20
        pam_end = 23
        self.pam_fragment_positive = SequenceFragment(pam, pam_start, pam_end)

        self.pam_position = {
            "start": pam_start,
            "end": pam_end
        }

        negative_bases = "GCCATTGTGGAGGAGTCCGAAACT"
        self.test_negative_guide = GuideSequence(negative_bases, "-")


    def test_guide_find_pam_positive_strand(self):
        guide = self.test_positive_guide

        test_pam = guide.find_pam()

        self.assertEqual(test_pam, self.pam_fragment_positive)

    def test_guide_find_pam_negative_strand(self):
        pam = "CCA"
        pam_start =1
        pam_end = 4
        pam_fragment = SequenceFragment(pam, pam_start, pam_end)

        guide = self.test_negative_guide

        test_pam = guide.find_pam()

        self.assertEqual(test_pam, pam_fragment)


    def test_define_window_positive_strand(self):
        window_start = 11
        window_end = 23
        window = {
            "start": window_start,
            "end": window_end
        }

        guide = self.test_positive_guide

        test_window = guide.define_window_positive_strand(self.pam_position)

        self.assertEqual(test_window, window)



