from unittest import TestCase
from unittest.mock import patch

from mutator.mutation_builder import get_window, MutationBuilder
from mutator.base_sequence import BaseSequence
from mutator.coding_region import CodingRegion
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow, WindowCodon, BaseWithPosition


class TestGuideSequence(TestCase):
    def test_get_window_frame_plus_plus(self):
        guide = GuideSequence(67626572, 67626594, is_positive_strand=True, chromosome='16', frame=0)
        cds = CodingRegion(67626555, 67626715, is_positive_strand=True, chromosome='16', frame=2)

        control_codons = [
            WindowCodon('TAT', BaseWithPosition('T', 67626583, 9)),
            WindowCodon('ATT', BaseWithPosition('T', 67626586, 6)),
            WindowCodon('GAG', BaseWithPosition('G', 67626589, 3)),
            WindowCodon('CAA', BaseWithPosition('A', 67626592, -1)),
        ]

        builder = MutationBuilder(guide, cds)
        window = builder.build_edit_window()
        codons = window.get_window_codons()

        self.assertEqual(codons, control_codons)

    def test_get_window_frame_CTCF(self):
        guide = GuideSequence(67610855, 67610877, is_positive_strand=True,
                              chromosome='16', frame=0)
        cds = CodingRegion(676108336, 67611613, is_positive_strand=True,
                           chromosome='16', frame=0)

        control_codons = [
            WindowCodon('GCC', BaseWithPosition('C', 67610856, 8)),
            WindowCodon('ATT', BaseWithPosition('T', 67610859, 5)),
            WindowCodon('GTG', BaseWithPosition('G', 67610862, 2)),
            WindowCodon('GAG', BaseWithPosition('G', 67610865, -2)),
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
            WindowCodon('GAT', BaseWithPosition('T', 77696658, 9)),
            WindowCodon('GAT', BaseWithPosition('T', 77696653, 6)),
            WindowCodon('TTG', BaseWithPosition('G', 77696650, 3)),
            WindowCodon('CCT', BaseWithPosition('T', 77696647, -1)),
        ]

        builder = MutationBuilder(guide, cds)
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
