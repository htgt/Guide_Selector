import unittest
from unittest.mock import Mock

from filter.max_edits_number_filter import MaxEditsNumberFilter


def _create_codon_with_third_pos(third_pos: int) -> Mock:
    codon = Mock()
    codon.third_base_pos = third_pos
    return codon


class TestMaxEditsNumberFilter(unittest.TestCase):
    def setUp(self) -> None:
        config = {'filters': {'max_edits_to_apply': 3}}
        self.max_edits_number_filter = MaxEditsNumberFilter(config)

        self.codon_3th_pos_4 = _create_codon_with_third_pos(4)
        self.codon_3th_pos_minus_2 = _create_codon_with_third_pos(-2)
        self.codon_3th_pos_minus_3 = _create_codon_with_third_pos(-3)
        self.codon_3th_pos_10 = _create_codon_with_third_pos(10)

        self.mutation_builder = Mock()

    def test_apply_when_no_mutation_builders(self):
        mutation_builders = []

        filter_response = self.max_edits_number_filter.apply(mutation_builders)

        self.assertEqual(filter_response.guides_to_keep, [])
        self.assertEqual(filter_response.guides_to_discard, [])

    def test_apply_when_more_than_max_edits(self):
        self.mutation_builder.codons = [
            self.codon_3th_pos_4,
            self.codon_3th_pos_minus_2,
            self.codon_3th_pos_minus_3,
            self.codon_3th_pos_10,
        ]

        mutation_builders = [self.mutation_builder]

        filter_response = self.max_edits_number_filter.apply(mutation_builders)

        third_pos_of_kept_codons = [codon.third_base_pos for codon in filter_response.guides_to_keep[0].codons]
        self.assertEqual(third_pos_of_kept_codons, [-2, -3, 4])

        third_pos_of_discarded_codons = [codon.third_base_pos for codon in filter_response.guides_to_discard[0].codons]
        self.assertEqual(third_pos_of_discarded_codons, [10])

    def test_apply_when_less_than_max_edits(self):
        self.mutation_builder.codons = [self.codon_3th_pos_4, self.codon_3th_pos_minus_3, self.codon_3th_pos_10]
        mutation_builders = [self.mutation_builder]

        filter_response = self.max_edits_number_filter.apply(mutation_builders)

        third_pos_of_kept_codons = [codon.third_base_pos for codon in filter_response.guides_to_keep[0].codons]
        self.assertEqual(third_pos_of_kept_codons, [4, -3, 10])

        self.assertEqual(filter_response.guides_to_discard, [])