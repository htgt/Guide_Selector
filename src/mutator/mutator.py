from typing import List

import pandas as pd
import warnings

from tdutils.utils.vcf_utils import Variants

from abstractions.command import Command
from adaptors.serialisers.mutation_builder_serialiser import convert_mutation_builders_to_df, serialise_mutation_builder  # NOQA
from coding_region import CodingRegion
from filter.filter_manager import FilterManager
from filter.filter_response import GuideDiscarded
from guide import GuideSequence
from guide_determiner import GuideDeterminer
from mutation_builder import MutationBuilder
from mutator.mutator_reader import MutatorReader
from mutator.mutator_writer import MutatorWriter
from ranker.ranker import Ranker
from target_region import TargetRegion

from utils.warnings import NoGuidesRemainingWarning


class Mutator(Command):
    def __init__(self, config: dict) -> None:
        self._config = config
        self._guides_df: pd.DataFrame = None
        self.mutation_builders: List[MutationBuilder] = []
        self.discarded_guides: List[GuideDiscarded] = []
        self.failed_mutations = None
        self.ranked_guides_df: pd.DataFrame = None

    def read_inputs(self, args: dict, guide_sequences=None):
        reader = MutatorReader().read_inputs(args, guide_sequences=guide_sequences)

        # Prepare data frame for the mutator
        self._guides_df = GuideDeterminer().parse_loci(reader.gtf_data, reader.guide_sequences)

    def run(self):
        self._set_mutation_builders(self._guides_df)
        self._generate_edit_windows_for_builders()
        self._filter_mutation_builders()
        self._rank_mutation_builders()

    def write_outputs(self, output_dir: str):
        writer = MutatorWriter(
            self._kept_mb_to_guides_and_codons(self.mutation_builders),
            self._discarded_mb_to_guides_and_codons(self.discarded_guides),
            self.variants,
            self.failed_mutations,
            self.ranked_guides_df,
            self.get_variants_by_guide_id(self.best_guide.guide_id),
        )

        writer.write_outputs(output_dir)

    def _set_mutation_builders(self, guide_data: pd.DataFrame) -> None:
        mutation_builder_objects = [self._build_mutations(row) for index, row in guide_data.iterrows()]

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
            self._append_mb_to_variants(mb, variants)

        return variants

    @property
    def best_guide(self) -> GuideSequence:
        best_guide_id = self.ranked_guides_df.at[0, 'guide_id']
        for mb in self.mutation_builders:
            if mb.guide.guide_id == best_guide_id:
                return mb.guide

    def get_variants_by_guide_id(self, id: str) -> Variants:
        chrom = [self.best_guide.chromosome]
        best_guide_mutations = Variants(chroms=chrom, variant_list=[])

        for mb in self.mutation_builders:
            if mb.guide.guide_id == id:
                self._append_mb_to_variants(mb, best_guide_mutations)

        return best_guide_mutations

    def _append_mb_to_variants(self, mb: MutationBuilder, variants: Variants) -> Variants:
        for codon in mb.codons:
            if codon.is_edit_permitted(
                    self._config,
                    mb.cds.start,
                    mb.cds.end
            ):
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
        return MutationBuilder(
            guide=guide,
            cds=coding_region,
            gene_name=gene_name,
            window_length=self._config["window_length"],
        )

    def _filter_mutation_builders(self):
        filters_response = FilterManager(self._config).apply_filters(self.mutation_builders)

        self.mutation_builders = filters_response.guides_to_keep
        self.discarded_guides = filters_response.guides_to_discard

        if not self.mutation_builders:
            warning_msg = '\n\tNo guides remaining after filtering, consider relaxing filters.'
            warnings.warn(NoGuidesRemainingWarning(warning_msg))

    def _rank_mutation_builders(self):
        df = convert_mutation_builders_to_df(self.mutation_builders, self._config)

        self.ranked_guides_df = Ranker(self._config).rank(df)

    def _kept_mb_to_guides_and_codons(self, mutation_builders: List[MutationBuilder]) -> List[dict]:
        result = []
        for mutation_builder in mutation_builders:
            result += serialise_mutation_builder(mutation_builder, self._config)

        return result

    def _discarded_mb_to_guides_and_codons(self, discarded_guide: List[GuideDiscarded]) -> List[dict]:
        result = []
        for guide in discarded_guide:
            result += serialise_mutation_builder(guide.mutation_builder, self._config, guide.filter_applied)

        return result


def _get_chromosome(mb: MutationBuilder) -> str:
    return mb.cds.chromosome


def _fill_guide_sequence(row: pd.Series) -> GuideSequence:
    target_region = TargetRegion(
        row['chromosome'],
        row.get('target_region_start'),
        row.get('target_region_end'),
        row.get('target_region_id', ''),
    )
    return GuideSequence(
        start=row['guide_start'],
        end=row['guide_end'],
        chromosome=row['chromosome'],
        is_positive_strand=(row['guide_strand'] == '+'),
        guide_id=row.name,
        frame=row['guide_frame'],
        ot_summary=row.get('ot_summary'),
        target_region=target_region,
        on_target_score=row.get('on_target_score'),
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
