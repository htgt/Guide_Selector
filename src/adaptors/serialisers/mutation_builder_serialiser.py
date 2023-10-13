from typing import List

from mutation_builder import MutationBuilder


def serialise_mutation_builder(mutation_builder: MutationBuilder, config: dict) -> List[dict]:
    serialised_mutation_builder = []
    base = {
        'guide_id': mutation_builder.guide.guide_id,
        'chromosome': mutation_builder.cds.chromosome,
        'cds_strand': _get_char_for_bool(mutation_builder.cds.is_positive_strand),
        'gene_name': mutation_builder.gene_name,
        'guide_strand': _get_char_for_bool(mutation_builder.guide.is_positive_strand),
        'guide_start': mutation_builder.guide.start,
        'guide_end': mutation_builder.guide.end,
        'ot_summary': mutation_builder.guide.ot_summary,
        'target_region_id': mutation_builder.guide.target_region_id,
        'wge_percentile': mutation_builder.guide.wge_percentile,
    }

    for codon in mutation_builder.codons:
        lost_amino = ','.join(codon.amino_acids_lost_from_edit) if codon.amino_acids_lost_from_edit else 'N/A'

        row = {
            'window_pos': codon.third_base_pos,
            'pos': codon.third_base_coord,
            'ref_codon': codon.bases,
            'ref_pos_three': codon.bases[2],
            'alt': codon.edited_bases[2],
            'lost_amino_acids': lost_amino,
            'permitted': codon.is_edit_permitted(config),
        }

        serialised_mutation_builder.append({**base, **row})

    return serialised_mutation_builder


def _get_char_for_bool(is_true: bool) -> str:
    return "+" if is_true else "-"
