from typing import List, Union

from pprint import pprint
import pandas as pd
from tdutils.utils.vcf_utils import Variants

from abstractions.command import Command
from adaptors.serialisers.mutation_builder_serialiser import serialise_mutation_builder
from coding_region import CodingRegion
from filter.filter_manager import FilterManager
from filter.filter_validator import FilterValidator
from guide import GuideSequence
from guide_determiner import GuideDeterminer
from mutation_builder import MutationBuilder
from mutator.mutator_reader import MutatorReader
from mutator.mutator_writer import MutatorWriter


class Mutator(Command):
    def __init__(self, config: dict) -> None:
        self._config = config
        self._guides_df = None
        self.mutation_builders = None
        self.discarded_guides = None
        self.failed_mutations = None

    def read_inputs(self, args: dict, guide_sequences=None):
        reader = MutatorReader().read_inputs(args, guide_sequences=guide_sequences)

        # Prepare data frame for the mutator
        self._guides_df = GuideDeterminer().parse_loci(reader.gtf_data, reader.guide_sequences)

    def run(self):
        self._set_mutation_builders(self._guides_df)
        self._generate_edit_windows_for_builders()
        self._filter_mutation_builders()

    def write_outputs(self, output_dir: str):
        writer = MutatorWriter(
            self._mutation_builders_to_guides_and_codons(self.mutation_builders),
            self._mutation_builders_to_guides_and_codons(self.discarded_guides),
            self.variants,
            self.failed_mutations,
        )

        writer.write_outputs(output_dir)

    def _set_mutation_builders(self, guide_data: pd.DataFrame) -> None:
        mutation_builder_objects = []

        for index, row in guide_data.iterrows():
            mutation_builder_objects.append(self._build_mutations(row))

        self.mutation_builders = mutation_builder_objects

    def _generate_edit_windows_for_builders(self) -> None:
        failed_mutations = []
        for mb in self.mutation_builders:
            if mb.window is None:
                failed_mutations.append(mb)
                self.mutation_builders.remove(mb)
            else:
                mb.build_window_codons()

        self.failed_mutations = failed_mutations

    @property
    def variants(self) -> Variants:
        chroms = map(_get_chromosome, self.mutation_builders)
        chroms = list(set(chroms))
        variants = Variants(chroms)

        for mb in self.mutation_builders:
            for codon in mb.codons:
                if codon.is_edit_permitted(self._config, mb.cds.start, mb.cds.end):
                    guide_id = mb.guide.guide_id
                    variants.append(
                        mb.cds.chromosome,
                        codon.third_base_coord,
                        id=guide_id,
                        ref=codon.third_base_on_positive_strand,
                        alt=codon.edited_third_base_on_positive_strand,
                        info={"SGRNA": f"sgRNA_{guide_id}"},
                    )
        return variants

    def _build_mutations(self, region_data: pd.Series) -> MutationBuilder:
        guide = _fill_guide_sequence(region_data)
        coding_region = _fill_coding_region(region_data)
        gene_name = region_data['gene_name']
        mutation_builder = MutationBuilder(
            guide=guide,
            cds=coding_region,
            gene_name=gene_name,
            window_length=self._config["window_length"],
        )

        return mutation_builder

    def _filter_mutation_builders(self):
        filter_manager = FilterManager(self._config)
        filters_to_activate = FilterValidator(self._config).validated_filters()

        for filter_class in filters_to_activate:
            filter_manager.load_filter(filter_class)

        filters_response = filter_manager.apply_filters(self.mutation_builders)

        self.mutation_builders = filters_response.guides_to_keep
        self.discarded_guides = filters_response.guides_to_discard

    def _mutation_builders_to_guides_and_codons(self, mutation_builders: List[MutationBuilder]) -> List[dict]:
        result = []
        for mutation_builder in mutation_builders:
            result += serialise_mutation_builder(mutation_builder, self._config)

        return result


    def convert_to_dataframe(self) -> pd.DataFrame:
        mutation_builders = self.mutation_builders

        if mutation_builders is None:
            raise ValueError("Mutation builders not available in the Mutator.")

        data = {
            "guide_id": [mb.guide.guide_id for mb in mutation_builders],
            "chromosome": [mb.cds.chromosome for mb in mutation_builders],
            "cds_strand": [_get_char_for_bool(mb.cds.is_positive_strand) for mb in mutation_builders],
            "gene_name": [mb.gene_name for mb in mutation_builders],
            "guide_strand": [_get_char_for_bool(mb.guide.is_positive_strand) for mb in mutation_builders],
            "guide_start": [mb.guide.start for mb in mutation_builders],
            "guide_end": [mb.guide.end for mb in mutation_builders],
            "ot_summary": [mb.guide.ot_summary for mb in mutation_builders],
            "target_region_id": [mb.guide.target_region_id for mb in mutation_builders],
            "wge_percentile": [mb.guide.wge_percentile for mb in mutation_builders],
        }

        codon_details = [self.extract_codon_details(mb) for mb in mutation_builders]

        data["codon_details"] = codon_details

        return pd.DataFrame(data)

    def extract_codon_details(self, mutation_builder: MutationBuilder) -> List:
        codon_details = []
        cds_start = mutation_builder.cds.start
        cds_end = mutation_builder.cds.end

        for codon in mutation_builder.codons:
            lost_amino = ','.join(codon.amino_acids_lost_from_edit) if codon.amino_acids_lost_from_edit else 'N/A'
            codon_data = {
                "window_pos": codon.third_base_pos,
                "pos": codon.third_base_coord,
                "ref_codon": codon.bases,
                "ref_pos_three": codon.bases[2],
                "alt": codon.edited_bases[2],
                "lost_amino_acids": lost_amino,
                "permitted": codon.is_edit_permitted(self._config, cds_start, cds_end),
            }
            codon_details.append(codon_data)

        return codon_details

def _get_char_for_bool(value):
    return '+' if value else '-'


def _get_chromosome(mb: MutationBuilder) -> str:
    return mb.cds.chromosome

def _fill_guide_sequence(row: pd.Series) -> GuideSequence:
    return GuideSequence(
        start=row['guide_start'],
        end=row['guide_end'],
        chromosome=row['chromosome'],
        is_positive_strand=(row['guide_strand'] == '+'),
        guide_id=row.name,
        frame=row['guide_frame'],
        ot_summary=row.get('ot_summary'),
        target_region_id=row.get('target_region_id'),
    )


def _fill_coding_region(row: pd.Series) -> CodingRegion:
    return CodingRegion(
        start=row['cds_start'],
        end=row['cds_end'],
        chromosome=row['chromosome'],
        is_positive_strand=(row['cds_strand'] == '+'),
        exon_number=row['exon_number'],
        frame=row['cds_frame'],
    )
