from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class NotContainTTTTFilter(Filter):
    def __init__(self, config: dict):
        self.min_edits = config['filters']['min_edits_allowed']

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            print(mb.guide.bases)
            print('------------')

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
