from mutator.frame import get_frame, SequenceRegion

def get_sequence_by_coords(cromosome, start, end) -> str:
    return get_seq_from_ensembl_by_coords(cromosome, start, end)

def get_window_frame():
    cds = SequenceRegion(True, 67626555, 67626715, 0)
    window = SequenceRegion(True, 67626583, 67626594, 0)

    window.frame = get_frame(cds, window)

    print(get_extended_window_coordinates(window))
    print(window)


def get_extended_window_coordinates(window):
    start = window.start
    end = window.end

    if window.isPositiveStrand:
        start = window.start - window.frame
    else:
        end = window.end + window.frame

    return start, end