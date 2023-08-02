from unittest import TestCase
from unittest.mock import patch

from mutator.mutation_builder import get_window, MutationBuilder
from mutator.base_sequence import BaseSequence
from mutator.coding_region import CodingRegion
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow
from mutator.codon import WindowCodon


class TestGuideSequence(TestCase):
    def test_get_window_frame_plus_plus(self):
        guide = GuideSequence(67626572, 67626594, is_positive_strand=True, chromosome='16', frame=0)
        cds = CodingRegion(67626555, 67626715, is_positive_strand=True, chromosome='16', frame=2)

        control_codons = [
            WindowCodon('TAT', 67626583, 9, True),
            WindowCodon('ATT', 67626586, 6, True),
            WindowCodon('GAG', 67626589, 3, True),
            WindowCodon('CAA', 67626592, -1, True),
        ]

        builder = MutationBuilder(guide, cds, 'BRCA1')
        window = builder.build_edit_window()
        codons = window.get_window_codons()

        self.assertEqual(list(map(vars, codons)), list(map(vars, control_codons)))
        #self.assertEqual(codons, control_codons)

    def test_get_window_frame_CTCF(self):
        guide = GuideSequence(67610855, 67610877, is_positive_strand=True,
                              chromosome='16', frame=0)
        cds = CodingRegion(676108336, 67611613, is_positive_strand=True,
                           chromosome='16', frame=0)

        control_codons = [
            WindowCodon('GCC', 67610856, 8, True),
            WindowCodon('ATT', 67610859, 5, True),
            WindowCodon('GTG', 67610862, 2, True),
            WindowCodon('GAG', 67610865, -2, True),
       ]

    ##   TODO: Mixed strands case

    #    builder = MutationBuilder(guide, cds)
    #    window = builder.build_edit_window()

    #    codons = window.get_window_codons()

    #    self.assertEqual(codons, control_codons)

    def test_get_window_frame_ATRX(self):
        guide = GuideSequence(77696636, 77696658, is_positive_strand=True,
                              chromosome='X', frame=0)
        cds = CodingRegion(77696577, 77696704, is_positive_strand=False,
                           chromosome='X', frame=0)

        control_codons = [
            WindowCodon('GAT', 77696658, 9, False),
            WindowCodon('GAT', 77696653, 6, False),
            WindowCodon('TTG', 77696650, 3, False),
            WindowCodon('CCT', 77696647, -1, False),
        ]

        builder = MutationBuilder(guide, cds, 'BRCA1')
        window = builder.build_edit_window()
        codons = window.get_window_codons()

    ##   TODO: Mixed strands case
    #    self.assertEqual(codons, control_codons)


class TestGetWindow(TestCase):
    def test_get_window(self):
        bases = "CAGCATTCCTATATTGAGCAAGG"
        guide_start = 67626572
        guide_end = 67626594
        guide_frame = 0

        coding_region = CodingRegion(67626572,67626594, True, 0)


        def mock_get_sequence_by_coords():
            return bases

        window_start = 67626583
        window_end = 67626594
        window_frame = 1

        window = EditWindow(window_start, window_end, is_positive_strand=True, chromosome='X', frame=window_frame)

        with patch.object(
                BaseSequence,
                'get_sequence_by_coords',
                side_effect=mock_get_sequence_by_coords
        ):
            guide = GuideSequence(guide_start, guide_end, is_positive_strand=True, chromosome='X', frame=guide_frame)
            result_window = get_window(guide, coding_region)

    #    self.assertEqual(result_window, window)
