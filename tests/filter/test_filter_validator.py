import unittest

from parameterized import parameterized

from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.filter_validator import FilterValidator
from filter.max_edits_number_filter import MaxEditsNumberFilter
from filter.min_edits_number_filter import MinEditsNumberFilter
from filter.omit_TTTT_filter import OmitTTTTFilter


class TestFilterValidator(unittest.TestCase):
    # fmt: off
    @parameterized.expand([
        # No filters
        ({}, []),
        ({'filters': {}}, []),
        # MinEditsNumberFilter
        ({'filters': {'min_edits_allowed': 3}}, [MinEditsNumberFilter]),
        # MaxEditsNumberFilter
        ({'filters': {'max_edits_to_apply': 3}}, [MaxEditsNumberFilter]),
        # EditGGInPAMFilter
        ({'filters': {'NGG_edit_required': True}}, [EditGGInPAMFilter]),
        ({'filters': {'NGG_edit_required': False}}, []),
        # NotContainTTTTFilter
        ({'filters': {'omit_TTTT+': True}}, [OmitTTTTFilter]),
        ({'filters': {'omit_TTTT+': False}}, []),
    ])  # fmt: on
    def test_validate_filters(self, filters, expected_result):
        result = FilterValidator(filters).validated_filters()

        self.assertEqual(result, expected_result)

    # fmt: off
    @parameterized.expand([
        ({'filters': {'NGG_edit_required': 'NO VALID VALUE'}}, 'NGG_edit_required', 'bool'),
        ({'filters': {'omit_TTTT+': 'NO VALID VALUE'}}, 'omit_TTTT+', 'bool'),
        ({'filters': {'min_edits_allowed': 'NO VALID VALUE'}}, 'min_edits_allowed', 'int'),
        ({'filters': {'max_edits_to_apply': 'NO VALID VALUE'}}, 'max_edits_to_apply', 'int'),
    ])  # fmt: on
    def test_validate_filters_when_no_valid_filter_value_type(self, filters, key, expected_value_type):

        with self.assertRaises(ValueError) as error:
            FilterValidator(filters).validated_filters()

        self.assertEqual(
            str(error.exception),
            f'Invalid filter: the value given for "{key}" is not of type {expected_value_type}'
        )

    def test_validate_filters_when_no_valid_key_filter(self):
        with self.assertRaises(ValueError) as error:
            FilterValidator({"filters": {"NO FILTER KEY": True}}).validated_filters()

        self.assertEqual(str(error.exception), 'Invalid filter: the given key "NO FILTER KEY" is not a filter key')

    def test_sort_filters(self):
        input_filters = {'filters': {'max_edits_to_apply': 3, 'NGG_edit_required': True, 'omit_TTTT+': True, 'min_edits_allowed': 3}}
        
        expected_output = {'filters': {'NGG_edit_required': True, 'omit_TTTT+': True, 'min_edits_allowed': 3, 'max_edits_to_apply': 3}}
        
        filter_validator = FilterValidator(input_filters)
        sorted_filters = filter_validator._config_filters
        
        self.assertEqual(sorted_filters, expected_output['filters'])