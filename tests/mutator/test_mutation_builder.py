from unittest import TestCase
from unittest.mock import patch

from mutator.mutation_builder import get_window_frame_and_codons, get_window
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow, WindowCodon, BaseWithPosition


class TestGuideSequence(TestCase):
    pass
   # def test_get_window_frame_plus_plus(self):
   #     cds = BaseSequence(67626555, 67626715, True, '16', 2)
   #     window = EditWindow(67626583, 67626594, True, '16')

    #    control_codons = [
    #        WindowCodon('TAT', BaseWithPosition('T', 67626583, 9)),
    #        WindowCodon('ATT', BaseWithPosition('T', 67626586, 6)),
    #        WindowCodon('GAG', BaseWithPosition('G', 67626589, 3)),
    #        WindowCodon('CAA', BaseWithPosition('A', 67626592, -1)),
    #    ]

    #    codons = get_window_frame_and_codons(cds, window)

    #    self.assertEqual(codons, control_codons)

    #def test_get_window_frame_CTCF(self):
    #    cds = BaseSequence(676108336, 67611613, True, '16', 2)
    #    window = EditWindow(67610855, 67610866, True, '16', )

    #    control_codons = [
    #        WindowCodon('GCC', BaseWithPosition('C', 67610856, 8)),
    #        WindowCodon('ATT', BaseWithPosition('T', 67610859, 5)),
    #        WindowCodon('GTG', BaseWithPosition('G', 67610862, 2)),
    #        WindowCodon('GAG', BaseWithPosition('G', 67610865, -2)),
    #   ]

    #    codons = get_window_frame_and_codons(cds, window)

     #   self.assertEqual(codons, control_codons)

   # def test_get_window_frame_ATRX(self):
   #     cds = BaseSequence(77696577, 77696704, False, 'X', 0)
   #     window = EditWindow(77696647, 77696658, True, 'X', )

   #     control_codons = [
   #         WindowCodon('GAT', BaseWithPosition('T', 77696647, 9)),
   #         WindowCodon('GAT', BaseWithPosition('T', 77696650, 6)),
   #         WindowCodon('TTG', BaseWithPosition('G', 77696653, 3)),
   #         WindowCodon('CCT', BaseWithPosition('T', 77696656, -1)),
   #     ]

    #    codons = get_window_frame_and_codons(cds, window)

     #   self.assertEqual(codons, control_codons)


   # def test_return_edit_window(self):
   #     window = EditWindow(67626583, 67626594, True)

   #     guide = self.test_positive_guide

    #    test_edit_window = guide.build_edit_window()

    #    self.assertEqual(test_edit_window, window)

class TestGetWindow(TestCase):
    def test_get_window(self):
        bases = "CAGCATTCCTATATTGAGCAAGG"
        guide_start = 67626572
        guide_end = 67626594
        guide_frame = 0

        def mock_get_sequence_by_coords():
            return bases

        window_start = 67626583
        window_end = 67626594
        window_frame = 1

        window = EditWindow(window_start, window_end, is_positive_strand=True, chromosome='X', frame=window_frame)

        with patch.object(
                BaseSequence,
                '_get_sequence_by_coords',
                side_effect=mock_get_sequence_by_coords
        ):
            guide = GuideSequence(guide_start, guide_end, is_positive_strand=True, chromosome='X', frame=guide_frame)
            result_window = get_window(guide)

        self.assertEqual(result_window, window)
