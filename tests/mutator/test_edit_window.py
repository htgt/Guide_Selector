from mutator.edit_window import EditWindow

import unittest
from parameterized import parameterized


class TestParametrizedEditWindow(unittest.TestCase):
    @parameterized.expand([
        # Positive strand test cases
        (10, 21, True, '16', 0, (10, 21)),
        (10, 21, True, '16', 1, (9, 21)),
        (10, 21, True, '16', 2, (8, 21)),
        # Negative strand test cases
        (10, 21, False, '16', 0, (10, 21)),
        (10, 21, False, '16', 1, (10, 22)),
        (10, 21, False, '16', 2, (10, 23)),
    ])
    def test_get_extended_window_coordinates(self, start, end, isPositiveStrand, chromosome, frame, expected_coordinates):
        window = EditWindow(start, end, isPositiveStrand, chromosome, frame)

        result_coordinates = window._get_extended_window_coordinates()

        self.assertEqual(result_coordinates, expected_coordinates, "Incorrect extended window coordinates")

class TestEditWindowCodons(unittest.TestCase):
        def test_split_window_into_codons(self):
            bases = 'TATTGAGCAAGG'
            codons = ['TAT', 'TGA', 'GCA', 'AGG']

            window = EditWindow(1, 2, True, '16')
            self.assertEqual(window.split_window_into_codons(bases), codons)


if __name__ == '__main__':
    unittest.main()

