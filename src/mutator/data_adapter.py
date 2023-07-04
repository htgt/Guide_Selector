from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow

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