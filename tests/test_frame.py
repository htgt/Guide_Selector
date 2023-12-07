import unittest

from parameterized import parameterized

from base_sequence import BaseSequence, FragmentFrameIndicator
from frame import get_frame


class TestGetFrame(unittest.TestCase):
    frame_ZERO = FragmentFrameIndicator.ZERO
    frame_ONE = FragmentFrameIndicator.ONE

    # fmt: off
    @parameterized.expand([  # Positive strand cds, same strand
        (BaseSequence(10, 40, True, '16', frame_ZERO), BaseSequence(15, 27, True, '16', frame_ZERO), frame_ONE),
        # Negative strand cds, same strand
        (BaseSequence(10, 40, False, '16', frame_ZERO), BaseSequence(27, 38, False, '16', frame_ZERO), frame_ONE),
        # Positive strand cds, different strand
        (BaseSequence(10, 40, True, '16', frame_ZERO), BaseSequence(25, 40, False, '16', frame_ZERO), frame_ZERO),
        # Negative strand cds, different strand
        (BaseSequence(10, 40, False, '16', frame_ONE), BaseSequence(16, 28, True, '16', frame_ZERO), frame_ONE),
    ])  # fmt: on
    def test_get_frame(self, coding_region, region, expected_frame):
        result_frame = get_frame(coding_region, region)

        self.assertEqual(
            result_frame,
            expected_frame,
            f"Correct frame for test case {coding_region.is_positive_strand, region.is_positive_strand}",
        )

    def test_invalid_frame_definition(self):
        invalid_frame_value = 3

        with self.assertRaises(ValueError) as error:
            FragmentFrameIndicator.get_frame_indicator(invalid_frame_value)

        self.assertEqual(
            str(error.exception),
            f'Invalid: the frame value {invalid_frame_value} is not in number in (0, 1, 2)'
        )


if __name__ == '__main__':
    unittest.main()
