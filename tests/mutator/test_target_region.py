import unittest
from mutator.target_region import parse_str_to_target_region, TargetRegion
from utils.exceptions import ParseStringToTargetRegionError

class TestParseTargetRegion(unittest.TestCase):
    def test_parse_str_to_target_region(self):
        input_str = "chr1:300-350"

        expected_region = TargetRegion(
            chromosome="chr1",
            start=300,
            end=350,
        )

        result = parse_str_to_target_region(input_str)

        self.assertEqual(result, expected_region)

    def test_fail_to_read_chr_for_target_region(self):
        input_str = "chr1300350"

        with self.assertRaises(ParseStringToTargetRegionError):
            parse_str_to_target_region(input_str)

    def test_fail_to_read_corrdinates_for_target_region(self):
        input_str = "chr1:300350"

        with self.assertRaises(ParseStringToTargetRegionError):
            parse_str_to_target_region(input_str)
