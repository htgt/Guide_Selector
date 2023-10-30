import copy
from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse, GuideDiscarded
from mutation_builder import MutationBuilder


class MaxEditsNumberFilter(Filter):
    key: str = 'max_edits_to_apply'
    value_type: type = int

    def __init__(self, config: dict):
        self.max_edits = config['filters']['max_edits_to_apply']

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_with_codons_to_keep = []
        guides_with_discarded_codons = []

        for mb in mbs:
            if len(mb.codons) > self.max_edits:
                sorted_codons = sorted(mb.codons, key=lambda codon: abs(codon.third_base_pos))

                codons_to_keep = sorted_codons[: self.max_edits]
                codons_to_discard = sorted_codons[self.max_edits :]

                guide_with_discarded_codons = copy.deepcopy(mb)
                guide_with_discarded_codons.codons = codons_to_discard
                guides_with_discarded_codons.append(
                    GuideDiscarded(guide_with_discarded_codons, MaxEditsNumberFilter.key)
                )

                mb.codons = codons_to_keep

            guides_with_codons_to_keep.append(mb)

        return FilterResponse(guides_to_keep=guides_with_codons_to_keep, guides_to_discard=guides_with_discarded_codons)
