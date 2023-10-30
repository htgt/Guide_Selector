from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse, GuideDiscarded
from mutation_builder import MutationBuilder


class NotContainTTTTFilter(Filter):
    def __init__(self, config: dict):
        pass

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            if 'TTTT' not in mb.guide.bases:
                guides_to_keep.append(mb)
            else:
                guides_to_discard.append(GuideDiscarded(mb, 'not_contain_TTTT+'))

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
