import unittest
from parameterized import parameterized

from filter.filter_validator import FilterValidator
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.max_edits_number_filter import MaxEditsNumberFilter
from filter.minimum_edits_filter import MinimumEditsFilter
from filter.not_contain_TTTT_filter import NotContainTTTTFilter


class TestFilterValidator(unittest.TestCase):
    @parameterized.expand([({}, []),
        ({'filters': {'no_valid_key': 3}}, []),
        ({'filters': {}}, []),
        # MinimumEditsFilter
        ({'filters': {'min_edits_allowed': 3}}, [MinimumEditsFilter]),
        # MaxEditsNumberFilter
        ({'filters': {'max_edits_to_apply': 3}}, [MaxEditsNumberFilter]),
        ({'filters': {'max_edits_to_apply': '3'}}, []),
        # EditGGInPAMFilter
        ({'filters': {'NGG_edit_required': True}}, [EditGGInPAMFilter]),
        ({'filters': {'NGG_edit_required': False}}, []),
        ({'filters': {'NGG_edit_required': 'NO VALID VALUE'}}, []),
        # NotContainTTTTFilter
        ({'filters': {'not_contain_TTTT+': True}}, [NotContainTTTTFilter]),
        ({'filters': {'not_contain_TTTT+': False}}, []),
        ({'filters': {'not_contain_TTTT+': 'NO VALID VALUE'}}, []),
    ])
    def test_validate_filters(self, filters, expected_result):
        result = FilterValidator(filters).validated_filters()
        self.assertEqual(result, expected_result)
