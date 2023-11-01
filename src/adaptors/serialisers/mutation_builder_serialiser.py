from typing import List

from mutation_builder import MutationBuilder
import pandas as pd


def serialise_mutation_builder(
    mutation_builder: MutationBuilder, config: dict, filter_applied: str = None
) -> List[dict]:

    base = _get_mutator_row(mutation_builder)

    return base


def convert_mutation_builders_to_df(mutation_builders: MutationBuilder, config) -> pd.DataFrame:
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
        'target_region_id': mutation_builder.guide.target_region_id,
        'guide_id': mutation_builder.guide.guide_id,
        'wge_percentile': mutation_builder.guide.wge_percentile,
        'valid_edits': count_valid_codons(mutation_builder),
        'chromosome': mutation_builder.cds.chromosome,
        'guide_start': mutation_builder.guide.start,
        'guide_end': mutation_builder.guide.end,
        'guide_strand': mutation_builder.guide.strand_symbol,
    }


def extract_codon_details(mutation_builder: MutationBuilder, config: dict) -> List:
    codon_details = []
    cds_start = mutation_builder.cds.start
    cds_end = mutation_builder.cds.end

    for codon in mutation_builder.codons:
        codon_data = _get_codon_row(cds_start, cds_end, codon, config)
        codon_details.append(codon_data)

    return codon_details


def _get_codon_row(cds_start, cds_end, codon, config):
    lost_amino = ','.join(codon.amino_acids_lost_from_edit) if codon.amino_acids_lost_from_edit else 'N/A'

    return {
        'window_pos': codon.third_base_pos,
        'pos': codon.third_base_coord,
        'ref_codon': codon.bases,
        'ref_pos_three': codon.bases[2],
        'alt': codon.edited_bases[2],
        'lost_amino_acids': lost_amino,
        'permitted': codon.is_edit_permitted(config, cds_start, cds_end),
    }


def _get_char_for_bool(is_true: bool) -> str:
    return "+" if is_true else "-"
