from typing import List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from filter.filter_validator import FilterValidator
from mutation_builder import MutationBuilder


class FilterManager:
    def __init__(self, config: dict):
        self._filters: List[Filter] = FilterValidator(config).validated_filters()
        self._config = config

    def apply_filters(self, data: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = data
        guides_to_discard = []

        for filter_class in self._filters:
            filter_instance = filter_class(self._config)
            filter_response = filter_instance.apply(guides_to_keep)

            guides_to_keep = filter_response.guides_to_keep
            guides_to_discard += filter_response.guides_to_discard

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
