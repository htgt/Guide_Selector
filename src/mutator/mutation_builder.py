from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.frame import get_frame
from utils.file_system import read_csv_to_list_dict


class MutationBuilder:
    def __init__(self, cds: BaseSequence, window: EditWindow) -> None:
        self.cds = cds
        self.window = window

        self.window.frame = self.calculate_window_frame()
        print(self)

    def calculate_window_frame(self) -> int:
        return get_frame(self.cds, self.window)


def get_window_frame(file : str):
    file_data = read_csv_to_list_dict(file, "\t")
    for row in (file_data):
        cds, window = build_coding_region_objects(row)

        print(window.get_extended_window_bases())
        print(window)

        builder = MutationBuilder(cds, window)

def build_coding_region_objects(data : dict) -> [BaseSequence, EditWindow]:
    cds = BaseSequence(
        int(data['cds_start']),
        int(data['cds_end']),
        _booleanise_strand(data['cds_strand']),
        _trim_chromosome(data['chromosome']),
        int(data['cds_frame'])
    )
    window = EditWindow(
        int(data['window_start']),
        int(data['window_end']),
        _booleanise_strand(data['guide_strand']),
        _trim_chromosome(data['chromosome']),
    )

    return cds, window

def _booleanise_strand(strand : str) -> bool:
    return strand == '+'

def _trim_chromosome(chr : str) -> str:
    return chr[3:]

