from typing import Dict, List

from abstractions.filter import Filter
from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class FilterManager:
    def __init__(self, config: dict):
        self._active_filters: Dict[str, Filter] = {}
        self._config = config

    def load_filter(self, filter_class):
        self._active_filters[filter_class.__name__] = filter_class(self._config)

    def unload_filter(self, filter_name: str):
        if filter_name in self._active_filters:
            del self._active_filters[filter_name]

    def apply_filters(self, data: List[MutationBuilder]) -> FilterResponse:
        guides_to_keep = data
        guides_to_discard = []
        for filter_instance in self._active_filters.values():
            filter_response = filter_instance.apply(guides_to_keep)
            guides_to_keep = filter_response.guides_to_keep
            guides_to_discard += filter_response.guides_to_discard

        return FilterResponse(guides_to_keep=guides_to_keep, guides_to_discard=guides_to_discard)
