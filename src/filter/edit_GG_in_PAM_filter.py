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
            mb.codons = [codon for codon in mb.codons if codon.third_base_pos == -2 or codon.third_base_pos == -3]
            filtered_mbs.append(mb)
        return filtered_mbs
