from mutator.frame import get_frame, SequenceRegion
from mutator.base_sequence import BaseSequence

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

    window.frame = get_frame(cds, window)

    print(window.get_extended_window_coordinates())
    print(window)


class EditWindow(BaseSequence):

    def get_extended_window_coordinates(self):
        start = self.start
        end = self.end

        if self.isPositiveStrand:
            start = self.start - self.frame
        else:
            end = self.end + self.frame

        print(self._get_sequence_by_coords('16', start, end))

        return start, end
