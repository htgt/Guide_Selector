from typing import List

from abstractions.filter import Filter
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.not_contain_TTTT_filter import NotContainTTTTFilter
from filter.max_edits_number_filter import MaxEditsNumberFilter
from filter.minimum_edits_filter import MinimumEditsFilter


class FilterValidator:
    def __init__(self, config: dict):
        self._filters = config.get("filters")

    def validated_filters(self) -> List[Filter]:
        valid_filters = []
        filter_validations = {
            'min_edits_allowed': (int, MinimumEditsFilter),
            'max_edits_to_apply': (int, MaxEditsNumberFilter),
            'NGG_edit_required': (bool, EditGGInPAMFilter),
            'not_contain_TTTT+': (bool, NotContainTTTTFilter),
        }

        if self._filters:
            for key, value in self._filters.items():

                filter_data = filter_validations.get(key)
                if filter_data:
                    (expected_type, filter_class) = filter_data
            
                    if isinstance(value, expected_type):
                        if value is not False:
                            valid_filters.append(filter_class)
                    else:
                        print(f'Invalid value: the value given for {key} is not {expected_type.__name__}')
                else:
                    print(f'{key}: filter not recognised')

        return valid_filters
