from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.frame import get_frame

def get_window_frame():
    cds = BaseSequence(
        67626555,
        67626715,
        True,
        '16',
        0
    )
    window = EditWindow(
        67626583,
        67626594,
        True,
        '16',
    )

    print(window.get_extended_window_bases())
    print(window)

    builder = MutationBuilder(cds, window)


class MutationBuilder:
    def __init__(self, cds: BaseSequence, window: EditWindow) -> None:
        self.cds = cds
        self.window = window

        self.window_frame = self.calculate_window_frame()
        print(self)

    def calculate_window_frame(self) -> int:
        return get_frame(self.cds, self.window)


    