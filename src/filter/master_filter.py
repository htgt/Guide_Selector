from typing import List, Dict

from abstractions.filter import Filter
from filter.minimum_edits_filter import MinimumEditsFilter
from mutation_builder import MutationBuilder
from utils.exceptions import FilterNotFoundException


class MasterFilter:
    def __init__(self, config: dict):
        self._active_filters: Dict[str, Filter] = {}
        self._config = config

    def load_filter(self, filter_name: str):
        self._active_filters[filter_name] = self._create_filter_instance(filter_name)

    def unload_filter(self, filter_name: str):
        if filter_name in self._active_filters:
            del self._active_filters[filter_name]

    def filter_data(self, data: List[MutationBuilder]) -> List[MutationBuilder]:
        for filter_name, filter_instance in self._active_filters.items():
            data = filter_instance.apply(data)
        return data

    def _create_filter_instance(self, filter_name) -> Filter:
        filter_class = Filter.find_filter(filter_name)
        if filter_class is not None:
            return filter_class(self._config)
        else:
            raise FilterNotFoundException(filter_name)


if __name__ == "__main__":
    # data_filter = MasterFilter({"min_edits_allowed": 2})
    # print(data_filter._active_filters)
    # data_filter.load_filter("MinimumEditsFilter")
    # print(data_filter._active_filters)
    print(Filter.get_filter_implementation_names())
    # data_filter.load_filter("MinimumEditsFilter")
