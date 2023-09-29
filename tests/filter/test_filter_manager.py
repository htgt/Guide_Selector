import unittest
from typing import List
from unittest.mock import Mock

from filter.filter_manager import FilterManager
from filter.minimum_edits_filter import MinimumEditsFilter
from mutation_builder import MutationBuilder


class TestFilterManager(unittest.TestCase):
    def setUp(self) -> None:
        self.filter_dict = {"filters": {"min_edits_allowed": 3}}
        self.filter_to_load = MinimumEditsFilter
        mb_1codons = Mock()
        mb_1codons.codons = ["codon1"]
        mb_2codons = Mock()
        mb_2codons.codons = ["codon1", "codon2"]
        mb_3codons = Mock()
        mb_3codons.codons = ["codon1", "codon2", "codon3"]
        mb_4codons = Mock()
        mb_4codons.codons = ["codon1", "codon2", "codon3", "codon4"]
        self.mutations_builder_to_filter = [mb_1codons, mb_2codons, mb_3codons, mb_4codons]

        self.test_instance = FilterManager(self.filter_dict)

    def test_load_filter(self):
        self.assertDictEqual(self.test_instance._active_filters, {}, 'There is not active filters')

        self.test_instance.load_filter(self.filter_to_load)

        self.assertEqual(len(self.test_instance._active_filters), 1)
        self.assertIsInstance(self.test_instance._active_filters["MinimumEditsFilter"], self.filter_to_load)

    def test_unload_filter_when_exists(self):
        self.test_instance.load_filter(self.filter_to_load)

        self.assertEqual(len(self.test_instance._active_filters), 1)

        self.test_instance.unload_filter("MinimumEditsFilter")

        self.assertEqual(len(self.test_instance._active_filters), 0)

    def test_unload_filter_when_do_not_exists(self):
        self.test_instance.load_filter(self.filter_to_load)

        self.assertEqual(len(self.test_instance._active_filters), 1)

        self.test_instance.unload_filter("Not Existing Filter Name")

        self.assertEqual(len(self.test_instance._active_filters), 1)

    def test_filter_data(self):
        self.test_instance.load_filter(self.filter_to_load)

        self.assertEqual(len(self.mutations_builder_to_filter), 4)

        result = self.test_instance.apply_filters(self.mutations_builder_to_filter)

        self.assertEqual(len(result), 2)
