import unittest

from parameterized import parameterized

from base_sequence import BaseSequence
from frame import get_frame


class TestGetFrame(unittest.TestCase):
    @parameterized.expand([  # Positive strand cds, same strand
        (BaseSequence(10, 40, True, '16', 0), BaseSequence(15, 27, True, '16', 0), 1),
        # Negative strand cds, same strand
        (BaseSequence(10, 40, False, '16', 0), BaseSequence(27, 38, False, '16', 0), 1),
        # Positive strand cds, different strand
        (BaseSequence(10, 40, True, '16', 0), BaseSequence(25, 40, False, '16', 0), 0),
        # Negative strand cds, different strand
        (BaseSequence(10, 40, False, '16', 1), BaseSequence(16, 28, True, '16', 0), 1),
    ])
    def test_get_frame(self, coding_region, region, expected_frame):
        result_frame = get_frame(coding_region, region)

        self.assertEqual(
            result_frame,
            expected_frame,
            f"Correct frame for test case {coding_region.is_positive_strand, region.is_positive_strand}"
        )


if __name__ == '__main__':
    unittest.main()
