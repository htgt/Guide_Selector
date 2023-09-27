from typing import List, Dict

from abstractions.filter import Filter
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

    def filter_data(self, data: List[MutationBuilder]) -> List[MutationBuilder]:
        for filter_name, filter_instance in self._active_filters.items():
            data = filter_instance.apply(data)
        return data
