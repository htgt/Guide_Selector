from typing import List

from abstractions.filter import Filter
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.minimum_edits_filter import MinimumEditsFilter


class FilterValidator:
    def __init__(self, config: dict):
        self._filters = config.get("filters")

    def validated_filters(self) -> List[Filter]:
        valid_filters = []
        if self._filters:
            for key, value in self._filters.items():
                if key == "min_edits_allowed" and type(value) is int:
                    valid_filters.append(MinimumEditsFilter)
                if key == 'NGG_edit_required' and value is True:
                    valid_filters.append(EditGGInPAMFilter)
        return valid_filters
