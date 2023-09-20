import unittest

from parameterized import parameterized

from edit_window import EditWindow, calculate_position_in_window
from codon import WindowCodon


class TestEditWindow(unittest.TestCase):
    def setUp(self) -> None:
        self.window_length = 12
    
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
        window = EditWindow(start, end, self.window_length, is_positive_strand, chromosome, frame, is_positive_strand)

        result_coordinates = window._get_extended_window_coordinates()

        self.assertEqual(result_coordinates, expected_coordinates, "Incorrect extended window coordinates")


class TestEditWindowCodons(unittest.TestCase):
    def setUp(self) -> None:
        self.window_length = 12
    
    @parameterized.expand([
        ('TATATTGAGCAAGG', (2, 13), [
            WindowCodon('TAT', 2, 9, True),
            WindowCodon('ATT', 5, 6, True),
            WindowCodon('GAG', 8, 3, True),
            WindowCodon('CAA', 11, -1, True)
        ]),
        ('TATTGAGCAAGG',  (0, 11), [
            WindowCodon('TAT', 2, 7, True),
            WindowCodon('TGA', 5, 4, True),
            WindowCodon('GCA', 8, 1, True),
            WindowCodon('AGG', 11, -3, True)
        ]),
    ])

    def test_split_window_into_codons(self, bases, window_coords, expected_codons):
        window = EditWindow(window_coords[0], window_coords[1], self.window_length, True, '16')

        result_codons = window.split_window_into_codons(bases, 0, len(bases), True)

        self.assertEqual(list(map(vars, result_codons)),  list(map(vars, expected_codons)))
        #self.assertEqual(result_codons, expected_codons, "Incorrect split into codons")


class TestEditWindowCodonsNegative(unittest.TestCase):
    def setUp(self) -> None:
        self.window_length = 12
    
    @parameterized.expand([('ATCATCCAAAGG',
        [WindowCodon('CCT', 77696656, -1, False),
        WindowCodon('TTG', 77696653, 3, False),
        WindowCodon('GAT', 77696650, 6, False),
        WindowCodon('GAT', 77696647, 9, False)]),
    ])

    def test_split_window_into_codons_negative(self, bases, expected_codons):
        window = EditWindow(77696647, 77696658, self.window_length, False, 'X')

        result_codons = window.split_window_into_codons(bases, 77696647, 77696658, False)

        self.assertEqual(list(map(vars, result_codons)),  list(map(vars, expected_codons)))


class TestCalculatePosition(unittest.TestCase):
    def setUp(self) -> None:
        self.window_length = 12
    
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
        result_position = calculate_position_in_window(start, coordinate, strand, self.window_length)

        self.assertEqual(result_position, expected_position, "Correct window position")


if __name__ == '__main__':
    unittest.main()

