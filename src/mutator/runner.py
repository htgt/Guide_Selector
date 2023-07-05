from dataclasses import dataclass
from typing import List

from mutator.mutation_builder import get_window_frame
from mutator.edit_window import WindowCodon, BaseWithPosition
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.guide import GuideSequenceLoci

@dataclass
class Runner:
    cds: BaseSequence
    window: EditWindow
    codon: WindowCodon
    guide: GuideSequenceLoci
    gene_name: str

    def __init__(self):
        self.cds = None
        self.window = None
        self.codon = None
        self.guide = None
        self.gene_name = None


    def window_frame(self, row : dict) -> None:
        self.build_coding_region_objects(row)
        get_window_frame(self.cds, self.window)

        base = BaseWithPosition('A', 23, 1)
        self.codon = WindowCodon('TCA', base)
    
    def build_coding_region_objects(self, data : dict) -> None:
        self.cds = BaseSequence(
            int(data['cds_start']),
            int(data['cds_end']),
            _booleanise_strand(data['cds_strand']),
            _trim_chromosome(data['chromosome']),
            int(data['cds_frame'])
        )
        self.window = EditWindow(
            int(data['window_start']),
            int(data['window_end']),
            _booleanise_strand(data['guide_strand']),
            _trim_chromosome(data['chromosome']),
        )
        self.guide = GuideSequenceLoci(
            guide_id=int(data['guide_id']),
            start=int(data['guide_start']),
            end=int(data['guide_end']),
            isPositiveStrand=_booleanise_strand(data['guide_strand']),
            chromosome=_trim_chromosome(data['chromosome']),
        )
        self.gene_name = data['gene_name']

    def as_row(self) -> dict:
        return {
            'guide_id' : self.guide.guide_id,
            'chromosome' : self.cds.chromosome,
            'cds_strand' : self.cds.isPositiveStrand,
            'gene_name' : 'ACT',
            'guide_strand' : self.guide.isPositiveStrand,
            'guide_start' : self.guide.start,
            'guide_end' : self.guide.end,
            'window_pos' : self.codon.third.window_position,
            'pos' : self.codon.third.coordinate,
            'ref_codon' : self.codon.bases,
            'ref_pos_three' : self.codon.third.base
        }


def _booleanise_strand(strand : str) -> bool:
    return strand == '+'

def _trim_chromosome(chr : str) -> str:
    return chr[3:]

def mutator_to_dict_list(runners : List[Runner]) -> List[dict]:
    return [r.as_row() for r in runners]

