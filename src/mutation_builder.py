import copy
from typing import List
from guide import GuideSequence
from edit_window import EditWindow
from frame import get_frame
from coding_region import CodingRegion
from codon import WindowCodon
from utils.exceptions import PamNotFoundError


class MutationBuilder:
    def __init__(
            self,
            guide: GuideSequence,
            cds: CodingRegion,
            gene_name: str,
            window_length: int,
    ) -> None:
        self.gene_name = gene_name
        self.codons = []

        self.guide = self._build_guide_sequence(guide)
        self.cds = self._build_coding_region(cds)
        self.window = self._build_edit_window(window_length)

    def __repr__(self):
        return (f"guide: {self.guide}, cds: {self.cds}, window: {self.window}, "
                f"target region id: {self.guide.target_region_id}")

    def _build_guide_sequence(self, guide: GuideSequence) -> GuideSequence:
        return copy.deepcopy(guide)

    def _build_coding_region(self, cds: CodingRegion) -> CodingRegion:
        return copy.deepcopy(cds)

    def _build_edit_window(self, window_length) -> EditWindow:
        window = get_window(self.guide, self.cds, window_length)
        self.window = window

        return window

    def build_window_codons(self) -> List[WindowCodon]:
        codons = self.window.get_window_codons()
        self.codons = codons

        return codons


def get_window(guide: GuideSequence, cds: CodingRegion, window_length: int) -> EditWindow:
    window_coordinates = guide.define_window(window_length)
    if type(window_coordinates) == PamNotFoundError:
        return

    window = EditWindow(
        start=window_coordinates[0],
        end=window_coordinates[1],
        window_length=window_length,
        is_positive_strand=cds.is_positive_strand,
        chromosome=guide.chromosome,
        frame=0,
        guide_strand_is_positive=guide.is_positive_strand
    )

    window.frame = get_frame(cds, window)
    return window
