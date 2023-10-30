import unittest
from unittest.mock import Mock

from filter.filter_manager import FilterManager
from filter.minimum_edits_filter import MinimumEditsFilter


class TestFilterManager(unittest.TestCase):
    def setUp(self) -> None:
        mb_1codons = Mock()
        mb_1codons.codons = ["codon1"]
        mb_2codons = Mock()
        mb_2codons.codons = ["codon1", "codon2"]
        mb_3codons = Mock()
        mb_3codons.codons = ["codon1", "codon2", "codon3"]
        mb_4codons = Mock()
        mb_4codons.codons = ["codon1", "codon2", "codon3", "codon4"]
        self.mutations_builder_to_filter = [mb_1codons, mb_2codons, mb_3codons, mb_4codons]

    def test_filter_data(self):
        self.assertEqual(len(self.mutations_builder_to_filter), 4)
        test_instance = FilterManager({"filters": {"min_edits_allowed": 3}})

        self.assertEqual(test_instance._filters, [MinimumEditsFilter])

        result = test_instance.apply_filters(self.mutations_builder_to_filter)

        self.assertEqual(len(result.guides_to_keep), 2)

    def test_filter_manager_init_fail_when_invalid_filter_value(self):
        with self.assertRaises(ValueError) as error:
            FilterManager({"filters": {"min_edits_allowed": 'NO VALID VALUE'}})

        self.assertEqual(
            str(error.exception), 'Invalid filter: the value given for "min_edits_allowed" is not of type int'
        )

    def test_filter_manager_init_fail_when_invalid_filter_key(self):
        with self.assertRaises(ValueError) as error:
            FilterManager({"filters": {"NO FILTER KEY": True}})

        self.assertEqual(str(error.exception), 'Invalid filter: the given key "NO FILTER KEY" is not a filter key')
