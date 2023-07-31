from dataclasses import dataclass
from typing import List
import copy

from mutator.mutation_builder import MutationBuilder
from mutator.codon import WindowCodon
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow
from mutator.guide import GuideSequence
from mutator.coding_region import CodingRegion



from pprint import pprint
import pandas as pd

@dataclass
class Runner:
    cds: BaseSequence
    window: EditWindow
    codons: List[WindowCodon]
    guide: GuideSequence
    gene_name: str
    mutation_builders: List[MutationBuilder]
    failed_mutations: List[MutationBuilder]

    def __init__(self) -> None:
        self.cds = None
        self.window = None
        self.codons = None
        self.guide = None
        self.gene_name = None
        self.mutation_builders = None
        self.failed_mutations = None

    def build_mutations(self, region_data : pd.DataFrame) -> None:
        guide = self.fill_guide_sequence(region_data)
        coding_region = self.fill_coding_region(region_data)
        mutation_builder = MutationBuilder(
            guide=guide,
            cds=coding_region
        )
        return mutation_builder

    def fill_guide_sequence(self, row: pd.Series) -> GuideSequence:
        return GuideSequence(
            start=row['guide_start'],
            end=row['guide_end'],
            chromosome=row['chromosome'],
            is_positive_strand=(row['guide_strand'] == '+'),
            guide_id=row.name,
            frame=row['guide_frame']
        )

    def fill_coding_region(self, row: pd.Series) -> CodingRegion:
        return CodingRegion(
            start=row['cds_start'],
            end=row['cds_end'],
            chromosome=row['chromosome'],
            is_positive_strand=(row['cds_strand'] == '+'),
            exon_number=row['exon_number'],
            frame=row['cds_frame']
        )

    def parse_coding_regions(self, guide_data : pd.DataFrame) -> None: 
        mutation_builder_objects = []

        for index, row in guide_data.iterrows():
            mutation_builder_objects.append(self.build_mutations(row))

        self.mutation_builders = mutation_builder_objects
    
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
        self.guide = GuideSequence(
            guide_id=int(data['guide_id']),
            start=int(data['guide_start']),
            end=int(data['guide_end']),
            is_positive_strand=_booleanise_strand(data['guide_strand']),
            chromosome=_trim_chromosome(data['chromosome']),
        )
        self.gene_name = data['gene_name']

    def as_rows(self, config : str) -> dict:
        rows = []
        for mb in (self.mutation_builders):
            base = {
                'guide_id' : mb.guide.guide_id,
                'chromosome' : mb.cds.chromosome,
                'cds_strand' : mb.cds.is_positive_strand,
                'gene_name' : self.gene_name,
                'guide_strand' : mb.guide.is_positive_strand,
                'guide_start' : mb.guide.start,
                'guide_end' : mb.guide.end,
            }

            for codon in (mb.codons):
                row = base
                lost_amino = ','.join(codon.amino_acids_lost_from_edit) if codon.amino_acids_lost_from_edit else 'N/A'

                row.update({
                    'window_pos' : codon.third_base_pos,
                    'pos' : codon.third_base_coord,
                    'ref_codon' : codon.bases,
                    'ref_pos_three' : codon.bases[2],
                    'alt' : codon.edited_bases[2],
                    'lost_amino_acids' : lost_amino, 
                    'permitted' : codon.is_edit_permitted(config)
                })
                rows.append(copy.deepcopy(row))

        return rows

    def generate_edit_windows_for_builders(self) -> None:
        failed_mutations = []
        for mb in self.mutation_builders:
            mb.build_edit_window()
            if mb.window is None:
                failed_mutations.append(mb)
                self.mutation_builders.remove(mb)
            else:
                mb.build_window_codons()

        self.failed_mutations = failed_mutations


def _booleanise_strand(strand : str) -> bool:
    return strand == '+'

def _trim_chromosome(chr : str) -> str:
    return chr[3:]


