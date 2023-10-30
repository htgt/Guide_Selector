from typing import List

from abstractions.filter import Filter
# The following imports are required to access filters via Filter.__subclasses__()
from filter.minimum_edits_filter import MinimumEditsFilter
from filter.max_edits_number_filter import MaxEditsNumberFilter
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.not_contain_TTTT_filter import NotContainTTTTFilter


class FilterValidator:
    def __init__(self, config: dict):
        self._config_filters = config.get('filters', {})

    def validated_filters(self) -> List[Filter]:
        valid_filters = []

        for key, value in self._config_filters.items():
            filter_class = _get_filter(key, value)

            if value is not False:
                valid_filters.append(filter_class)

        return valid_filters


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
