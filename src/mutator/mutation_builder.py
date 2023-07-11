import copy
from typing import List
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow, WindowCodon
from mutator.frame import get_frame


class MutationBuilder:
    def __init__(self, cds: BaseSequence, window: EditWindow) -> None:
        self.cds = copy.deepcopy(cds)
        self.window = copy.deepcopy(window)

    def calculate_window_frame(self) -> int:
        return get_frame(self.cds, self.window)


def get_window_frame_and_codons(cds : BaseSequence, window : EditWindow) -> List[WindowCodon]:
    builder = MutationBuilder(cds, window)

    result_window = copy.deepcopy(window)
    result_window.frame = builder.calculate_window_frame()

    return result_window.get_window_codons()
