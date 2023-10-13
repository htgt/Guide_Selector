from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class EditGGInPAMFilter(Filter):
    def __init__(self, config: dict):
        pass

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            codons_with_pam_edit = [
                codon for codon in mb.codons if codon.third_base_pos == -2 or codon.third_base_pos == -3
            ]

            if codons_with_pam_edit:
                guides_to_keep.append(mb)
            else:
                guides_to_discard.append(mb)

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
