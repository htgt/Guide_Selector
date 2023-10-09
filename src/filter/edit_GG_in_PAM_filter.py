import copy
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
            codons = mb.codons
            codons_in = list(filter(lambda codon: codon.third_base_pos in [-2, -3], codons))
            codons_out = list(filter(lambda codon: codon.third_base_pos not in [-2, -3], codons))

            if len(codons_in) == 0:
                guides_to_discard.append(mb)
            elif len(codons_out) == 0:
                guides_to_keep.append(mb)
            else:
                mb_out = copy.deepcopy(mb)
                mb_out.codons = codons_out
                guides_to_discard.append(mb_out)

                mb.codons = codons_in
                guides_to_keep.append(mb)

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
