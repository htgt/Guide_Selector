from typing import List

from abstractions.filter import Filter

# The following imports are required to access filters via Filter.__subclasses__()
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.max_edits_number_filter import MaxEditsNumberFilter
from filter.min_edits_number_filter import MinEditsNumberFilter
from filter.omit_TTTT_filter import OmitTTTTFilter


class FilterValidator:
    def __init__(self, config: dict):
        self._config_filters = config.get('filters', {})
        self._sort_filters()

    def validated_filters(self) -> List[Filter]:
        valid_filters = []

        for key, value in self._config_filters.items():
            filter_class = _get_filter(key, value)

            if value is not False:
                valid_filters.append(filter_class)

        return valid_filters
    
    def _sort_filters(self) -> None:
        filters = self._config_filters.copy()

        min_filter = filters.pop('min_edits_allowed', None)
        max_filter = filters.pop('max_edits_to_apply', None)

        sorted_filters = {key: filters[key] for key in sorted(filters)}

        if min_filter is not None:
            sorted_filters['min_edits_allowed'] = min_filter
        if max_filter is not None:
            sorted_filters['max_edits_to_apply'] = max_filter

        self._config_filters = sorted_filters


def _get_filter(key: str, value: any) -> Filter:
    _check_filter_key(key)

    filter_class = Filter.get_filter_by_key(key)
    _check_value_type(value, filter_class)

    return filter_class


def _check_filter_key(key: str):
    if key not in [_filter.key for _filter in Filter.__subclasses__()]:
        raise ValueError(f'Invalid filter: the given key "{key}" is not a filter key')


def _check_value_type(value: any, filter_cls: Filter):
    if not isinstance(value, filter_cls.value_type):
        raise ValueError(
            f'Invalid filter: the value given for "{filter_cls.key}" is not of type {filter_cls.value_type.__name__}'
        )