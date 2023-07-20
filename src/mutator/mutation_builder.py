import copy
from typing import List
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow, WindowCodon
from mutator.frame import get_frame
from mutator.coding_region import CodingRegion
from utils.exceptions import PamNotFoundError

class MutationBuilder:
    def __init__(self, guide: GuideSequence, cds : CodingRegion) -> None:
        self.guide = self._build_guide_sequence(guide)
        self.cds = self._build_coding_region(cds)
        self.window = EditWindow()
        self.failed = False

    def _build_guide_sequence(self, guide) -> GuideSequence:
        return copy.deepcopy(guide)

    def _build_coding_region(self, cds) -> CodingRegion:
        return copy.deepcopy(cds)

    def build_edit_window(self) -> EditWindow:
        window = get_window(self.guide)
        self.window = window

        return window

def get_window(guide: GuideSequence) -> EditWindow:
    window_coordinates = guide.define_window()
    if type(window_coordinates) == PamNotFoundError:
        guide.failed = True
        return

    window = EditWindow(
        window_coordinates[0],
        window_coordinates[1],
        guide.is_positive_strand,
        guide.chromosome,
    )

    window.frame = get_frame(guide, window)

    return window


