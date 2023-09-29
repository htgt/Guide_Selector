import unittest
from unittest.mock import Mock

from filter.minimum_edits_filter import MinimumEditsFilter


class TestMinimumEditsFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.filter_dict = {"filters": {"min_edits_allowed": 3}}
        self.filter_class_to_load = MinimumEditsFilter
        mb_1codons = Mock()
        mb_1codons.codons = ["codon1"]
        mb_2codons = Mock()
        mb_2codons.codons = ["codon1", "codon2"]
        mb_3codons = Mock()
        mb_3codons.codons = ["codon1", "codon2", "codon3"]
        mb_4codons = Mock()
        mb_4codons.codons = ["codon1", "codon2", "codon3", "codon4"]
        self.mutations_builder_to_filter = [mb_1codons, mb_2codons, mb_3codons, mb_4codons]

    def test_apply_filter(self):
        test_instance = MinimumEditsFilter(self.filter_dict)

        self.assertEqual(len(self.mutations_builder_to_filter), 4)

        result = test_instance.apply(self.mutations_builder_to_filter)

        self.assertEqual(len(result), 2)
