import copy
from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class EditGGInPAMFilter(Filter):
    def __init__(self, config: dict):
        pass

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        filtered = []
        not_filtered = []
        for mb in mbs:
            codons = mb.codons
            codons_in = list(filter(lambda codon: codon.third_base_pos not in [-2, -3], codons))
            codons_out = list(filter(lambda codon: codon.third_base_pos in [-2, -3], codons))

            if len(codons_in) == 0:
                not_filtered.append(mb)
            elif len(codons_out) == 0:
                filtered.append(mb)
            else:
                mb_out = copy.deepcopy(mb)
                mb_out.codons = codons_out
                not_filtered.append(mb_out)

                mb.codons = codons_in
                filtered.append(mb)

        return FilterResponse(filtered=filtered, not_filtered=not_filtered)
