import unittest
from parameterized import parameterized

from filter.filter_validator import FilterValidator
from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.max_edits_number_filter import MaxEditsNumberFilter
from filter.minimum_edits_filter import MinimumEditsFilter
from filter.not_contain_TTTT_filter import NotContainTTTTFilter


class TestFilterValidator(unittest.TestCase):
    @parameterized.expand([({}, []),
        # MinimumEditsFilter
        ({'filters': {'no_valid_key': 3}}, []),
        ({'filters': {'min_edits_allowed': 3}}, [MinimumEditsFilter]),
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

    def test_validate_filters_when_no_filters(self):
        no_filters = {}

        result = FilterValidator(no_filters).validated_filters()

        self.assertEqual(result, [])

    def test_validate_filters_when_not_valid_filters(self):
        not_valid_filters = {'filters': {'no_valid_key': 3}}

        result = FilterValidator(not_valid_filters).validated_filters()

        self.assertEqual(result, [])

    def test_validate_filters_minimum_edit_filter(self):
        minimum_edit_filter = {'filters': {'min_edits_allowed': 3}}

        result = FilterValidator(minimum_edit_filter).validated_filters()

        self.assertEqual(len(result), 1)
        self.assertIs(result[0], MinimumEditsFilter)

    def test_validate_filters_NGG_edit_required_true(self):
        minimum_edit_filter = {'filters': {'NGG_edit_required': True}}

        result = FilterValidator(minimum_edit_filter).validated_filters()

        self.assertEqual(len(result), 1)
        self.assertIs(result[0], EditGGInPAMFilter)

    def test_validate_filters_NGG_edit_required_false(self):
        minimum_edit_filter = {'filters': {'NGG_edit_required': False}}

        result = FilterValidator(minimum_edit_filter).validated_filters()

        self.assertEqual(result, [])

    def test_validate_filters_NGG_edit_required_with_not_valid_value(self):
        minimum_edit_filter = {'filters': {'NGG_edit_required': "NO VALID VALUE"}}

        result = FilterValidator(minimum_edit_filter).validated_filters()

        self.assertEqual(result, [])

    def test_validate_filters_max_edits_filter(self):
        max_edit_filter = {'filters': {'max_edits_to_apply': 3}}

        result = FilterValidator(max_edit_filter).validated_filters()

        self.assertEqual(len(result), 1)
        self.assertIs(result[0], MaxEditsNumberFilter)

    def test_validate_filters_max_edits_filter_when_no_int_value(self):
        max_edit_filter = {'filters': {'max_edits_to_apply': '3'}}

        result = FilterValidator(max_edit_filter).validated_filters()

        self.assertEqual(result, [])
