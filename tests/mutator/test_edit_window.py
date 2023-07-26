import unittest

from parameterized import parameterized

from mutator.edit_window import EditWindow, calculate_position_in_window
from mutator.codon import WindowCodon, BaseWithPosition


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
    def test_get_extended_window_coordinates(self, start, end, is_positive_strand, chromosome, frame, expected_coordinates):
        window = EditWindow(start, end, is_positive_strand, chromosome, frame, is_positive_strand)

        result_coordinates = window._get_extended_window_coordinates()

        self.assertEqual(result_coordinates, expected_coordinates, "Incorrect extended window coordinates")


class TestEditWindowCodons(unittest.TestCase):
    @parameterized.expand([
        ('TATATTGAGCAAGG', (2, 13), [
            WindowCodon('TAT', third=BaseWithPosition('T', 2, 9)),
            WindowCodon('ATT', third=BaseWithPosition('T', 5, 6)),
            WindowCodon('GAG', third=BaseWithPosition('G', 8, 3)),
            WindowCodon('CAA', third=BaseWithPosition('A', 11, -1))
        ]),
        ('TATTGAGCAAGG',  (0, 11), [
            WindowCodon('TAT', BaseWithPosition('T', 2, 7)),
            WindowCodon('TGA', BaseWithPosition('A', 5, 4)),
            WindowCodon('GCA', BaseWithPosition('A', 8, 1)),
            WindowCodon('AGG', BaseWithPosition('G', 11, -3))
        ]),
    ])

    def test_split_window_into_codons(self, bases, window_coords, expected_codons):
        window = EditWindow(window_coords[0], window_coords[1], True, '16')

        result_codons = window.split_window_into_codons(bases, 0, len(bases), True)

        self.assertEqual(result_codons, expected_codons, "Incorrect split into codons")


class TestEditWindowCodonsNegative(unittest.TestCase):
    @parameterized.expand([('ACCTTTGGATGAT',
        [WindowCodon('GAT', BaseWithPosition('T', 77696659, 10)),
        WindowCodon('GAT', BaseWithPosition('T', 77696656, 7)),
        WindowCodon('TTG', BaseWithPosition('G', 77696653, 4)),
        WindowCodon('CCT', BaseWithPosition('T', 77696650, 1))]),
    ])

    def test_split_window_into_codons_negative(self, bases, expected_codons):
        window = EditWindow(77696647, 77696659, False, 'X')

        result_codons = window.split_window_into_codons(bases, 77696647, 77696659, False)

      #  self.assertEqual(result_codons, expected_codons, "Incorrect split into codons")


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

