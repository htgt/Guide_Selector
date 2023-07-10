from mutator.edit_window import \
    EditWindow, \
    WindowCodon, \
    BaseWithPosition, \
    calculate_position_in_window

import unittest
from parameterized import parameterized


class TestEditWindow(unittest.TestCase):
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


class TestCalculatePosition(unittest.TestCase):
    @parameterized.expand([
        (67626583, 67626592, True, -1),
        (67626583, 67626589, True, 3),
        (67626583, 67626586, True, 6),
        (77696647, 77696656, True, -1),
        (77696647, 77696653, True, 3),
        (67610855, 67610856, False, -2),
        (67610855, 67610859, False, 2),
        (67610855, 67610862, False, 5),
        (67610855, 67610865, False, 8),
    ])
    def test_calculate_position_in_window(self, start, coordinate, strand, expected_position):
        result_position = calculate_position_in_window(start, coordinate, strand)

        self.assertEqual(result_position, expected_position, "Correct window position")


if __name__ == '__main__':
    unittest.main()

