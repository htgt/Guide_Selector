from dataclasses import dataclass
from typing import List
import copy

from mutator.mutation_builder import get_window_frame_and_codons
from mutator.edit_window import WindowCodon, BaseWithPosition
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.guide import GuideSequenceLoci

@dataclass
class Runner:
    cds: BaseSequence
    window: EditWindow
    codons: List[WindowCodon]
    guide: GuideSequenceLoci
    gene_name: str

    def __init__(self) -> None:
        self.cds = None
        self.window = None
        self.codons = None
        self.guide = None
        self.gene_name = None

    def parse_guide_loci(self) -> None: 
        print('Dummy function for upcoming feature')

    def run_window_frame(self, row : dict) -> None:
        self.build_coding_region_objects(row)

        codons = get_window_frame_and_codons(self.cds, self.window)

        self.codons = codons

        return codons
    
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
            is_positive_strand=_booleanise_strand(data['guide_strand']),
            chromosome=_trim_chromosome(data['chromosome']),
        )
        self.gene_name = data['gene_name']

    def as_rows(self) -> dict:
        rows = []
        base = {
            'guide_id' : self.guide.guide_id,
            'chromosome' : self.cds.chromosome,
            'cds_strand' : self.cds.is_positive_strand,
            'gene_name' : self.gene_name,
            'guide_strand' : self.guide.is_positive_strand,
            'guide_start' : self.guide.start,
            'guide_end' : self.guide.end,
        }

        for codon in (self.codons):
            row = base
            row.update({
                'window_pos' : codon.third.window_position,
                'pos' : codon.third.coordinate,
                'ref_codon' : codon.bases,
                'ref_pos_three' : codon.third.base
            })
            rows.append(copy.deepcopy(row))

        return rows


def _booleanise_strand(strand : str) -> bool:
    return strand == '+'

def _trim_chromosome(chr : str) -> str:
    return chr[3:]

def mutator_to_dict_list(runners : List[Runner]) -> List[dict]:
    rows = []
    for runner in runners:
        rows.extend(runner.as_rows())

    return rows

