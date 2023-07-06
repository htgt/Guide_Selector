from unittest import TestCase

from mutator.mutation_builder import get_window_frame
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow, WindowCodon

cds = BaseSequence(
    67626555,
    67626715,
    True,
    '16',
    2
)
window = EditWindow(
    67626583,
    67626594,
    True,
    '16',
)

control_codons = [
    WindowCodon('TAT', 'T'),
    WindowCodon('ATT', 'T'),
    WindowCodon('GAG', 'G'),
    WindowCodon('CAA', 'A'),
]

class TestGuideSequence(TestCase):
    def test_get_window_frame_plus_plus(self):
        codons = get_window_frame(cds, window)

        self.assertEqual(codons, control_codons)
