from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse, GuideDiscarded
from mutation_builder import MutationBuilder


class EditGGInPAMFilter(Filter):
    key: str = 'NGG_edit_required'
    value_type: type = bool

    def __init__(self, config: dict):
        pass

    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = []
        guides_to_discard = []

        for mb in mbs:
            codons_with_pam_edit = [codon for codon in mb.codons if codon.third_base_pos in [-2, -3]]

            if codons_with_pam_edit:
                guides_to_keep.append(mb)
            else:
                guides_to_discard.append(GuideDiscarded(mb, EditGGInPAMFilter.key))

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
