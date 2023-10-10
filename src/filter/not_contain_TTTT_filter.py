import re
from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class NotContainTTTTFilter(Filter):
    def __init__(self):
        self.pattern = r'T{4,}'

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            matches = re.findall(self.pattern, mb.guide.bases)

            if len(matches) == 0:
                guides_to_keep.append(mb)
            else:
                guides_to_discard.append(mb)

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
