from mutator.edit_window import EditWindow, WindowCodon, BaseWithPosition

import unittest
from parameterized import parameterized


class TestParametrizedEditWindow(unittest.TestCase):
    @parameterized.expand([
        # Positive strand test cases
        (10, 21, True, '16', 0, (10, 21)),
        (10, 21, True, '16', 1, (8, 21)),
        (10, 21, True, '16', 2, (9, 21)),
        # Negative strand test cases
        (10, 21, False, '16', 0, (10, 21)),
        (10, 21, False, '16', 1, (10, 23)),
        (10, 21, False, '16', 2, (10, 22)),
    ])
    def test_get_extended_window_coordinates(self, start, end, isPositiveStrand, chromosome, frame, expected_coordinates):
        window = EditWindow(start, end, isPositiveStrand, chromosome, frame)

        result_coordinates = window._get_extended_window_coordinates()

        self.assertEqual(result_coordinates, expected_coordinates, "Incorrect extended window coordinates")

class TestEditWindowCodons(unittest.TestCase):
        def test_split_window_into_codons(self):
            bases = 'TATATTGAGCAAGG'
            codons = [
                WindowCodon('TAT', BaseWithPosition('T', 2)),
                WindowCodon('ATT', BaseWithPosition('T', 5)),
                WindowCodon('GAG', BaseWithPosition('G', 8)),
                WindowCodon('CAA', BaseWithPosition('A', 11))
            ]

            window = EditWindow(0, 12, True, '16')

            self.assertEqual(window.split_window_into_codons(bases, 0), codons)

        def test_split_window_into_codons2(self):
            bases = 'TATTGAGCAAGG'
            codons = [
                WindowCodon('TAT', BaseWithPosition('T', 2)),
                WindowCodon('TGA', BaseWithPosition('A', 5)),
                WindowCodon('GCA', BaseWithPosition('A', 8)),
                WindowCodon('AGG', BaseWithPosition('G', 11))
            ]

            window = EditWindow(0, 12, True, '16')

            self.assertEqual(window.split_window_into_codons(bases, 0), codons)


if __name__ == '__main__':
    unittest.main()

