import copy
from typing import List
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow, WindowCodon
from mutator.frame import get_frame


class MutationBuilder:
    def __init__(self, guide: GuideSequence) -> None:
        self.guide = self._build_guide_sequence(guide)
        self.cds = self._build_coding_region()
        self.window = self._build_edit_window()

    def calculate_window_frame(self) -> int:
        return get_frame(self.cds, self.window)

    def _build_guide_sequence(self, guide) -> GuideSequence:
        return copy.deepcopy(guide)

    def _build_coding_region(self) -> BaseSequence:
        return "Coding Region here"

    def _build_edit_window(self) -> EditWindow:
        return get_window(self.guide)

def get_window(guide:GuideSequence) -> EditWindow:
    window_coordinates = guide.define_window()
    window = Editwindow(window_coordinates[0], window_coordinates[1],
        self.guide.is_positive_strand)

    return window

def get_window_frame_and_codons(cds : BaseSequence, window : EditWindow) -> List[WindowCodon]:
    builder = MutationBuilder(cds, window)

    result_window = copy.deepcopy(window)
    result_window.frame = builder.calculate_window_frame()

    return result_window.get_window_codons()

