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
        filtered = data
        not_filtered = []
        for filter_instance in self._active_filters.values():
            filter_response = filter_instance.apply(filtered)
            filtered = filter_response.filtered
            not_filtered += filter_response.not_filtered

        return FilterResponse(filtered=filtered, not_filtered=not_filtered)
