from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.frame import get_frame


class MutationBuilder:
    def __init__(self, cds: BaseSequence, window: EditWindow) -> None:
        self.cds = cds
        self.window = window

        self.window.frame = self.calculate_window_frame()
        print(self)

    def calculate_window_frame(self) -> int:
        return get_frame(self.cds, self.window)


def get_window_frame(cds : BaseSequence, window : EditWindow):
    print(window)

    builder = MutationBuilder(cds, window)

    return window.get_window_codons()

