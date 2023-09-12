from dataclasses import dataclass
from typing import List
import copy

from mutator.mutation_builder import get_window_frame_and_codons, MutationBuilder
from mutator.edit_window import WindowCodon, BaseWithPosition, EditWindow
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.coding_region import CodingRegion
from td_utils.vcf_utils import Variants

from pprint import pprint
import pandas as pd


@dataclass
class Runner:
    mutation_builders: List[MutationBuilder]
    failed_mutations: List[MutationBuilder]

    def __init__(self, config: dict) -> None:
        self._config = config
        self.mutation_builders = None
        self.failed_mutations = None

    def build_mutations(self, region_data: pd.DataFrame) -> None:
        guide = self.fill_guide_sequence(region_data)
        coding_region = self.fill_coding_region(region_data)
        gene_name = region_data['gene_name']
        target_region_id = region_data['target_region_id']
        mutation_builder = MutationBuilder(
            guide=guide,
            cds=coding_region,
            gene_name=gene_name,
            window_length=self._config["window_length"],
            target_region_id=target_region_id
        )

        return mutation_builder

    def fill_guide_sequence(self, row: pd.Series) -> GuideSequence:
        return GuideSequence(
            start=row['guide_start'],
            end=row['guide_end'],
            chromosome=row['chromosome'],
            is_positive_strand=(row['guide_strand'] == '+'),
            guide_id=row.name,
            frame=row['guide_frame'],
            ot_summary=row.get('ot_summary', None)
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

    def create_mutation_builders(self, guide_data: pd.DataFrame) -> None:
        mutation_builder_objects = []

        for index, row in guide_data.iterrows():
            mutation_builder_objects.append(self.build_mutations(row))

        self.mutation_builders = mutation_builder_objects

    def as_rows(self, config: str) -> dict:
        rows = []

        for mb in self.mutation_builders:
            base = {
                'guide_id': mb.guide.guide_id,
                'chromosome': mb.cds.chromosome,
                'cds_strand': _get_char_for_bool(mb.cds.is_positive_strand),
                'gene_name': mb.gene_name,
                'guide_strand': _get_char_for_bool(mb.guide.is_positive_strand),
                'guide_start': mb.guide.start,
                'guide_end': mb.guide.end,
                'ot_summary': mb.guide.ot_summary,
                'target_region_id': mb.guide.target_region_id,
            }

            for codon in mb.codons:
                row = base
                lost_amino = ','.join(codon.amino_acids_lost_from_edit) if codon.amino_acids_lost_from_edit else 'N/A'

                row.update({
                    'window_pos': codon.third_base_pos,
                    'pos': codon.third_base_coord,
                    'ref_codon': codon.bases,
                    'ref_pos_three': codon.bases[2],
                    'alt': codon.edited_bases[2],
                    'lost_amino_acids': lost_amino,
                    'permitted': codon.is_edit_permitted(config)
                })

                rows.append(copy.deepcopy(row))
        return rows

    def generate_edit_windows_for_builders(self) -> None:
        failed_mutations = []
        for mb in self.mutation_builders:
            if mb.window is None:
                failed_mutations.append(mb)
                self.mutation_builders.remove(mb)
            else:
                mb.build_window_codons()

        self.failed_mutations = failed_mutations

    def write_output_to_vcf(self, file_path: str) -> str:
        file_path = Path(file_path)
        file_path.with_suffix(".vcf")

        variants = self.to_variants_obj()
        write_to_vcf(variants, file_path)

        return str(file_path)

    def to_variants_obj(self) -> Variants:
        chroms = map(_get_chromosome, self.mutation_builders)
        chroms = list(set(chroms))
        variants = Variants(chroms)

        for mb in self.mutation_builders:
            for codon in mb.codons:
                if codon.is_edit_permitted(self._config):
                    guide_id = mb.guide.guide_id
                    variants.append(
                        mb.cds.chromosome,
                        codon.third_base_coord,
                        id=guide_id,
                        ref=codon.third_base_on_positive_strand,
                        alt=codon.edited_third_base_on_positive_strand,
                        info={"SGRNA": f"sgRNA_{guide_id}"}
                    )
        return variants


def _booleanise_strand(strand: str) -> bool:
    return strand == '+'


def _get_char_for_bool(is_true: bool) -> str:
    return "+" if is_true else "-"


def _trim_chromosome(chr: str) -> str:
    return chr[3:]


def _get_chromosome(mb: MutationBuilder) -> str:
    return mb.cds.chromosome
