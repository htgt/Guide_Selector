from unittest import TestCase

from mutator.mutation_builder import get_window_frame
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow, WindowCodon, BaseWithPosition



class TestGuideSequence(TestCase):
    def testget_window_frame_plus_plus(self):
        cds = BaseSequence(67626555, 67626715, True, '16', 2)
        window = EditWindow(67626583, 67626594, True, '16', )

        control_codons = [
            WindowCodon('TAT', BaseWithPosition('T', 67626583)),
            WindowCodon('ATT', BaseWithPosition('T', 67626586)),
            WindowCodon('GAG', BaseWithPosition('G', 67626589)),
            WindowCodon('CAA', BaseWithPosition('A', 67626592)),
        ]

        codons = get_window_frame(cds, window)

        self.assertEqual(codons, control_codons)

    def test_get_window_frame_CTCF(self):
        cds = BaseSequence(676108336, 67611613, True, '16', 2)
        window = EditWindow(67610855, 67610866, True, '16', )

        control_codons = [
            WindowCodon('GCC', BaseWithPosition('C', 67610856)),
            WindowCodon('ATT', BaseWithPosition('T', 67610859)),
            WindowCodon('GTG', BaseWithPosition('G', 67610862)),
            WindowCodon('GAG', BaseWithPosition('G', 67610865)),
        ]

        codons = get_window_frame(cds, window)

        self.assertEqual(codons, control_codons)

    def test_get_window_frame_ATRX(self):
        cds = BaseSequence(77696577, 77696704, False, 'X', 0)
        window = EditWindow(77696647, 77696658, True, 'X', )

        control_codons = [
            WindowCodon('CCT', BaseWithPosition('T', 77696656)),
            WindowCodon('TTG', BaseWithPosition('G', 77696653)),
            WindowCodon('GAT', BaseWithPosition('T', 77696650)),
            WindowCodon('GAT', BaseWithPosition('T', 77696647)),
        ]

       # codons = get_window_frame(cds, window)

       # self.assertEqual(codons, control_codons)