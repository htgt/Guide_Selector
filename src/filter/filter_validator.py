from typing import List

from abstractions.filter import Filter
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.not_contain_TTTT_filter import NotContainTTTTFilter
from filter.minimum_edits_filter import MinimumEditsFilter


class FilterValidator:
    def __init__(self, config: dict):
        self._filters = config.get('filters')

    def validated_filters(self) -> List[Filter]:
        valid_filters = []
        if self._filters:
            for key, value in self._filters.items():
                if key == 'min_edits_allowed':
                    if isinstance(value, int):
                        valid_filters.append(MinimumEditsFilter)
                    else:
                        print('Invalid value: the value given for minimum edits is not integer')
                if key == 'NGG_edit_required':
                    if value is True:
                        valid_filters.append(EditGGInPAMFilter)
                    else:
                        print('Invalid value: the value given for NGG edits is not \'true\'')
                if key == 'not_contain_TTTT+':
                    if value is True:
                        valid_filters.append(NotContainTTTTFilter)
                    else:
                        print('Invalid value: the value given for TTTT+ filter is not \'true\'')
        return valid_filters
