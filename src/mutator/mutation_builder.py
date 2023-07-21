import copy
from typing import List
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow, WindowCodon
from mutator.frame import get_frame
from mutator.coding_region import CodingRegion

class MutationBuilder:
    def __init__(self, guide: GuideSequence, cds) -> None:
        self.guide = self._build_guide_sequence(guide)
        self.cds = cds

        self.window = EditWindow(0,0)

    def _build_guide_sequence(self, guide) -> GuideSequence:
        return copy.deepcopy(guide)

    def _build_coding_region(self, cds) -> CodingRegion:
        return copy.deepcopy(cds)

    def _build_edit_window(self) -> EditWindow:
        return get_window(self.guide)

def get_window(guide:GuideSequence) -> EditWindow:
    window_coordinates = guide.define_window()
    window = EditWindow(window_coordinates[0], window_coordinates[1],
        guide.is_positive_strand)

    return window

def get_window_frame_and_codons(cds, guide: GuideSequence) -> List[WindowCodon]:
    builder = MutationBuilder(cds, guide)

    result_window.frame = builder.calculate_window_frame()

    return builder.get_window_codons()
