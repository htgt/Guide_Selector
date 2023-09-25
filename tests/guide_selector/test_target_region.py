import unittest

from parameterized import parameterized

from target_region import TargetRegion, parse_string_to_target_region
from utils.exceptions import ParseStringToTargetRegionError


class TestParseTargetRegion(unittest.TestCase):
    @parameterized.expand([
        ("chr1:300-350", TargetRegion(chromosome="1", start=300, end=350)),
        ("ch2:100-150", TargetRegion(chromosome="2", start=100, end=150)),
        ("3:222-333", TargetRegion(chromosome="3", start=222, end=333)),
    ])
    def test_parse_valid_target_region(self, input_str, expected_region):
        result = parse_string_to_target_region(input_str)
        self.assertEqual(result, expected_region)

    @parameterized.expand([
        ("chr1300350", ParseStringToTargetRegionError),
        ("ch2100-150", ParseStringToTargetRegionError),
        ("222-333", ParseStringToTargetRegionError),
    ])
    def test_invalid_target_region(self, input_str, exception):
        with self.assertRaises(exception):
            parse_string_to_target_region(input_str)
