from typing import List

import pandas as pd

from codon import WindowCodon
from mutation_builder import MutationBuilder


def serialise_mutation_builder(
    mutation_builder: MutationBuilder, config: dict, filter_applied: str = None
) -> List[dict]:
    serialised_mutation_builder = []

    mb_dict = _get_mutation_builder_dict(mutation_builder, filter_applied)

    cds_start = mutation_builder.cds.start
    cds_end = mutation_builder.cds.end

    for codon in mutation_builder.codons:
        codon_dict = _get_codon_dict(cds_start, cds_end, codon, config)

        serialised_mutation_builder.append({**mb_dict, **codon_dict})

    return serialised_mutation_builder


def _get_mutation_builder_dict(mutation_builder: MutationBuilder, filter_applied: str = None) -> dict:
    return {
        'target_region_id': mutation_builder.guide.target_region.id,
        'guide_id': mutation_builder.guide.guide_id,
        'chromosome': mutation_builder.cds.chromosome,
        'cds_strand': _get_char_for_bool(mutation_builder.cds.is_positive_strand),
        'gene_name': mutation_builder.gene_name,
        'guide_strand': mutation_builder.guide.strand_symbol,
        'guide_start': mutation_builder.guide.start,
        'guide_end': mutation_builder.guide.end,
        'ot_summary': mutation_builder.guide.ot_summary,
        'wge_percentile': mutation_builder.guide.wge_percentile,
        'on_target_score': mutation_builder.guide.on_target_score if mutation_builder.guide.on_target_score else 'N/A',
        'centrality_score': mutation_builder.guide.centrality_score,
        **({'filter_applied': filter_applied} if filter_applied else {}),
    }


def _get_codon_dict(cds_start: int, cds_end: int, codon: WindowCodon, config: dict) -> dict:
    lost_amino = ','.join(codon.amino_acids_lost_from_edit) if codon.amino_acids_lost_from_edit else 'N/A'

    return {
        'window_pos': codon.third_base_pos,
        'pos': codon.third_base_coord,
        'ref_codon': codon.bases,
        'ref_pos_three': codon.bases[2],
        'alt': codon.edited_bases[2],
        'lost_amino_acids': lost_amino,
        'permitted': codon.is_edit_permitted(config["edit_rules"], cds_start, cds_end),
    }


# Dataframe
def convert_mutation_builders_to_df(mutation_builders: List[MutationBuilder], config: dict) -> pd.DataFrame:
    if mutation_builders is None:
        raise ValueError("Mutation builders not available for dataframing.")
    data = []
    for mb in mutation_builders:
        row = _get_mutator_row(mb)
        data.append(row)

    return pd.DataFrame(data)


def count_valid_codons(mutation_builder: MutationBuilder) -> int:
    return len(mutation_builder.codons)


def _get_mutator_row(mutation_builder: MutationBuilder) -> dict:
    return {
        'target_region_id': mutation_builder.guide.target_region.id,
        'guide_id': mutation_builder.guide.guide_id,
        'centrality': mutation_builder.guide.centrality_score,
        'wge_percentile': mutation_builder.guide.wge_percentile,
        'valid_edits': count_valid_codons(mutation_builder),
        'on_target_score': mutation_builder.guide.on_target_score if mutation_builder.guide.on_target_score else 'N/A',
        'chromosome': mutation_builder.cds.chromosome,
        'guide_start': mutation_builder.guide.start,
        'guide_end': mutation_builder.guide.end,
        'guide_strand': mutation_builder.guide.strand_symbol,
    }


def _get_char_for_bool(is_true: bool) -> str:
    return "+" if is_true else "-"
