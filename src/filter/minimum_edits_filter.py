from typing import List

from abstractions.filter import Filter
from mutation_builder import MutationBuilder


class MinimumEditsFilter(Filter):

    def __init__(self, config: dict):
        self.min_edits = config['min_edits_allowed']

    def apply(self, mbs: List[MutationBuilder]) -> List[MutationBuilder]:
        return [mb for mb in mbs if len(mb.codons) >= self.min_edits]
