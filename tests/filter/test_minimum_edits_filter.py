import unittest
from unittest.mock import Mock

from filter.filter_response import GuideDiscarded
from filter.minimum_edits_filter import MinimumEditsFilter


class TestMinimumEditsFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.filter_dict = {'filters': {'min_edits_allowed': 3}}
        self.mb_1codons = Mock()
        self.mb_1codons.codons = ['codon1']
        self.mb_2codons = Mock()
        self.mb_2codons.codons = ['codon1', 'codon2']
        self.mb_3codons = Mock()
        self.mb_3codons.codons = ['codon1', 'codon2', 'codon3']
        self.mb_4codons = Mock()
        self.mb_4codons.codons = ['codon1', 'codon2', 'codon3', 'codon4']

    def test_apply_filter(self):
        test_instance = MinimumEditsFilter(self.filter_dict)

        result = test_instance.apply([self.mb_1codons, self.mb_2codons, self.mb_3codons, self.mb_4codons])

        self.assertEqual(result.guides_to_keep, [self.mb_3codons, self.mb_4codons])
        self.assertCountEqual(result.guides_to_discard,
                              [GuideDiscarded(self.mb_2codons, 'min_edits_allowed'),
                               GuideDiscarded(self.mb_1codons, 'min_edits_allowed')]
                              )
