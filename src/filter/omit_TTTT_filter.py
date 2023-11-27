from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse, GuideDiscarded
from mutation_builder import MutationBuilder


class OmitTTTTFilter(Filter):
    key: str = 'omit_TTTT+'
    value_type: type = bool

    def __init__(self, config: dict):
        pass

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            pattern = 'TTTT' if mb.guide.is_positive_strand else 'AAAA'
            if pattern not in mb.guide.bases:
                guides_to_keep.append(mb)
            else:
                guides_to_discard.append(GuideDiscarded(mb, OmitTTTTFilter.key))

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
