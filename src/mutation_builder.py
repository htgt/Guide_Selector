from typing import List

from coding_region import CodingRegion
from codon import WindowCodon
from edit_window import EditWindow
from frame import get_frame
from guide import GuideSequence
from utils.exceptions import PamNotFoundError


class MutationBuilder:
    def __init__(
        self,
        guide: GuideSequence,
        cds: CodingRegion,
        gene_name: str,
        window_length: int,
        edits_config: dict = {},
    ) -> None:
        self.gene_name = gene_name
        self.codons = []
        self._edits_config = edits_config

        self.guide = guide
        self.cds = cds
        self.window = get_window(self.guide, self.cds, window_length)

    def __repr__(self):
        return (
            f"guide: {self.guide}, cds: {self.cds}, window: {self.window}, "
            f"target region id: {self.guide.target_region.id}"
        )

    def build_window_codons(self) -> List[WindowCodon]:
        codons = self.window.get_window_codons(self._edits_config, self.cds.start, self.cds.end)
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
        guide_strand_is_positive=guide.is_positive_strand,
    )

    window.frame = get_frame(cds, window)
    return window
