import unittest

from wge_percentile import calculate_wge_percentile


class TestWgePercentile(unittest.TestCase):
    def test_calculate_wge_percentile(self):
        percentile_10 = {0: 1, 1: 0, 2: 0, 3: 3, 4: 70}
        percentile_25 = {0: 1, 1: 0, 2: 0, 3: 8, 4: 70}
        percentile_50 = {0: 1, 1: 0, 2: 1, 3: 8, 4: 70}
        percentile_100 = {0: 1, 1: 0, 2: 3, 3: 63, 4: 590}

        expected_percentiles = [10, 25, 50, 100]

        off_targets_list = [percentile_10, percentile_25, percentile_50, percentile_100]
        percentiles = []
        for off_target in off_targets_list:
            percentiles.append(calculate_wge_percentile(off_target))

        self.assertEqual(percentiles, expected_percentiles)
