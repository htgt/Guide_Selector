from mutator.frame import get_frame
from mutator.base_sequence import BaseSequence


class EditWindow(BaseSequence):
    def _get_extended_window_coordinates(self):
        start = self.start
        end = self.end

        if self.isPositiveStrand:
            start = self.start - self.frame
        else:
            end = self.end + self.frame

        return start, end

    def get_extended_window_bases(self):
        extended_window = self._get_extended_window_coordinates()
        bases = self._get_sequence_by_coords(
            self.chromosome,
            extended_window[0],
            extended_window[1]
        )

        return bases
