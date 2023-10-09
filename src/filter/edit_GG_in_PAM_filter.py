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
            codons_to_keep = list(filter(lambda codon: codon.third_base_pos in [-2, -3], codons))
            codons_to_discard = list(filter(lambda codon: codon.third_base_pos not in [-2, -3], codons))

            if len(codons_to_keep) == 0:
                guides_to_discard.append(mb)
            elif len(codons_to_discard) == 0:
                guides_to_keep.append(mb)
            else:
                guide_to_discard = copy.deepcopy(mb)
                guide_to_discard.codons = codons_to_discard
                guides_to_discard.append(guide_to_discard)

                mb.codons = codons_to_keep
                guides_to_keep.append(mb)

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
