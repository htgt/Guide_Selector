from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class MinimumEditsFilter(Filter):
    def __init__(self, config: dict):
        self.min_edits = config['filters']['min_edits_allowed']

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        filtered = []
        not_filtered = []

        for mb in mbs:
            if len(mb.codons) >= self.min_edits:
                filtered.append(mb)
            else:
                not_filtered.append(mb)

        return FilterResponse(filtered=filtered, not_filtered=not_filtered)
