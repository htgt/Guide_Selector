import unittest
from mutator.base_sequence import BaseSequence
from mutator.frame import get_frame


class TestGetFrame(unittest.TestCase):
    def test_positive_strand_cds_same_strand(self):
        coding_region = BaseSequence(10, 40, True, '16', 0)
        region = BaseSequence(15, 27, True, '16', 0)
        expected_frame = 2

        result_frame = get_frame(coding_region, region)

        self.assertEqual(result_frame, expected_frame, "Correct frame for positive strand (same strand)")


    def test_negative_strand_cds_same_strand(self):
        coding_region = BaseSequence(10, 40, False, '16', 0)
        region = BaseSequence(27, 38, False, '16', 0)
        expected_frame = 2

        result_frame = get_frame(coding_region, region)

        self.assertEqual(result_frame, expected_frame, "Correct frame for negative strand (same strand)")


    def test_positive_strand_cds_different_strand(self):
        coding_region = BaseSequence(10, 40, True, '16', 0)
        region = BaseSequence(25, 40, False, '16', 0)
        expected_frame = 0

        result_frame = get_frame(coding_region, region)

        self.assertEqual(result_frame, expected_frame, "Correct frame for positive strand (different strand)")


    def test_negative_strand_cds_different_strand(self):
        coding_region = BaseSequence(10, 40, False, '16', 1)
        region = BaseSequence(16, 28, True, '16', 0)
        expected_frame = 1

        result_frame = get_frame(coding_region, region)

        self.assertEqual(result_frame, expected_frame, "Correct frame for negative strand (different strand)")

if __name__ == '__main__':
    unittest.main()
