import unittest
from unittest.mock import Mock

from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter
from filter.filter_response import GuideDiscarded


class TestEditGGInPAMFilter(unittest.TestCase):
    def setUp(self) -> None:
        config = {'filters': {'NGG_edit_required': True}}
        self.test_instance = EditGGInPAMFilter(config)
        codon_third_pos_4 = Mock()
        codon_third_pos_4.third_base_pos = 4
        codon_third_pos_minus_2 = Mock()
        codon_third_pos_minus_2.third_base_pos = -2
        codon_third_pos_minus_3 = Mock()
        codon_third_pos_minus_3.third_base_pos = -3

        self.mb_to_keep1 = Mock()
        self.mb_to_keep1.codons = [codon_third_pos_4, codon_third_pos_minus_2]
        self.mb_to_keep2 = Mock()
        self.mb_to_keep2.codons = [codon_third_pos_4, codon_third_pos_minus_3]
        self.mb_to_discard = Mock()
        self.mb_to_discard.codons = [codon_third_pos_4]

    def test_apply_when_no_mutation_builders(self):
        mutation_builders = []

        filter_response = self.test_instance.apply(mutation_builders)

        self.assertEqual(filter_response.guides_to_keep, [])
        self.assertEqual(filter_response.guides_to_discard, [])

    def test_apply(self):
        mutation_builders = [self.mb_to_keep1, self.mb_to_keep2, self.mb_to_discard]

        filter_response = self.test_instance.apply(mutation_builders)

        self.assertEqual(len(filter_response.guides_to_keep), 2)
        self.assertEqual(filter_response.guides_to_keep[0], self.mb_to_keep1)
        self.assertEqual(filter_response.guides_to_keep[1], self.mb_to_keep2)

        self.assertEqual(len(filter_response.guides_to_discard), 1)
        self.assertEqual(filter_response.guides_to_discard[0], GuideDiscarded(self.mb_to_discard, 'NGG_edit_required'))
