import unittest

from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.mutation_builder import build_coding_region_objects

class CodingRegionObjectsTestCase(unittest.TestCase):

    def test_build_coding_region_objects(self):
        # Sample input data
        data = {
            'cds_start': '100',
            'cds_end': '200',
            'cds_strand': '+',
            'chromosome': 'chr1',
            'cds_frame': '0',
            'window_start': '150',
            'window_end': '250',
            'guide_strand': '-',
        }

        # Expected output
        expected_cds = BaseSequence(100, 200, True, '1', 0)
        expected_window = EditWindow(150, 250, False, '1')

        # Call the function
        cds, window = build_coding_region_objects(data)

        # Assert the results
        self.assertEqual(cds, expected_cds)
        self.assertEqual(window, expected_window)


if __name__ == '__main__':
    unittest.main()
