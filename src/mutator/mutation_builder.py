import copy
from typing import List
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow
from mutator.frame import get_frame
from mutator.coding_region import CodingRegion
from mutator.codon import WindowCodon
from utils.exceptions import PamNotFoundError


class MutationBuilder:
    def __init__(self, guide: GuideSequence, cds: CodingRegion, gene_name: str, target_region_id: str) -> None:
        self.guide = self._build_guide_sequence(guide)
        self.cds = self._build_coding_region(cds)
        self.gene_name = gene_name
        self.target_region_id = target_region_id
        self.window = EditWindow(0,0)
        self.codons = []

    def __repr__(self):
        return f"guide: {self.guide}, cds: {self.cds}, window: {self.window}"

    def _build_guide_sequence(self, guide: GuideSequence) -> GuideSequence:
        return copy.deepcopy(guide)

    def _build_coding_region(self, cds: CodingRegion) -> CodingRegion:
        return copy.deepcopy(cds)

    def build_edit_window(self) -> EditWindow:
        window = get_window(self.guide, self.cds)
        self.window = window

        return window

    def build_window_codons(self) -> List[WindowCodon]:
        codons = self.window.get_window_codons()
        self.codons = codons

        return codons


def get_window(guide:GuideSequence, cds: CodingRegion) -> EditWindow:
    window_coordinates = guide.define_window()
    if type(window_coordinates) == PamNotFoundError:
        return

    window = EditWindow(
        start=window_coordinates[0],
        end=window_coordinates[1],
        is_positive_strand=cds.is_positive_strand,
        chromosome=guide.chromosome,
        frame=0,
        guide_strand_is_positive=guide.is_positive_strand
    )

    window.frame = get_frame(cds, window)
    return window


