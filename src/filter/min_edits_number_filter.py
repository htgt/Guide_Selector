from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse, GuideDiscarded
from mutation_builder import MutationBuilder


class MinEditsNumberFilter(Filter):
    key: str = 'min_edits_allowed'
    value_type: type = int

    def __init__(self, config: dict):
        self.min_edits = config['filters']['min_edits_allowed']

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            if len(mb.codons) >= self.min_edits:
                guides_to_keep.append(mb)
            else:
                guides_to_discard.append(GuideDiscarded(mb, MinEditsNumberFilter.key))

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
