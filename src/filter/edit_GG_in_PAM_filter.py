from typing import List

from abstractions.filter import Filter
from mutation_builder import MutationBuilder


class EditGGInPAMFilter(Filter):

    def __init__(self, config: dict):
        pass

    def apply(self, mbs: List[MutationBuilder]) -> List[MutationBuilder]:
        filtered_mbs = []
        for mb in mbs:
            mb.codons = [codon for codon in mb.codons if codon.third_base_pos != -2 and codon.third_base_pos != -3]
            filtered_mbs.append(mb)
        return filtered_mbs
