import unittest
from unittest.mock import Mock

from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter


class TestEditGGInPAMFilter(unittest.TestCase):
    def setUp(self) -> None:
        config = {'filters': {'min_edits_allowed': 3, 'NGG_edit_required': True}}
        self.test_instance = EditGGInPAMFilter(config)
        self.mutation_builder = Mock()
<<<<<<< HEAD
        codon_not_filtered = Mock()
        codon_not_filtered.third_base_pos = 1
        codon_filtered1 = Mock()
        codon_filtered1.third_base_pos = -2
        codon_filtered2 = Mock()
        codon_filtered2.third_base_pos = -3
        self.mutation_builder.codons = [codon_not_filtered, codon_filtered1, codon_filtered2]
=======
        codon_to_discard = Mock()
        codon_to_discard.third_base_pos = 1
        codon_to_keep1 = Mock()
        codon_to_keep1.third_base_pos = -2
        codon_to_keep2 = Mock()
        codon_to_keep2.third_base_pos = -3
        self.mutation_builder.codons = [codon_to_discard, codon_to_keep1, codon_to_keep2]
        codon_to_keep = Mock()
        codon_to_keep.third_base_pos = 1
        codon_to_discard1 = Mock()
        codon_to_discard1.third_base_pos = -2
        codon_to_discard2 = Mock()
        codon_to_discard2.third_base_pos = -3
        self.mutation_builder.codons = [codon_to_keep, codon_to_discard1, codon_to_discard2]
>>>>>>> dbafffa... TD-495code review changes

    def test_apply_when_no_mutation_builders(self):
        mutation_builders = []

        filter_response = self.test_instance.apply(mutation_builders)

<<<<<<< HEAD
        self.assertEqual(filtered_result, [])
=======
        self.assertEqual(filter_response.guides_to_keep, [])
        self.assertEqual(filter_response.guides_to_discard, [])
>>>>>>> dbafffa... TD-495code review changes

    def test_apply(self):
        mutation_builders = [self.mutation_builder]

        self.assertEqual(len(self.mutation_builder.codons), 3)

        result = self.test_instance.apply(mutation_builders)

<<<<<<< HEAD
        self.assertEqual(len(result[0].codons), 2)
        self.assertEqual(result[0].codons[0].third_base_pos, -2)
        self.assertEqual(result[0].codons[1].third_base_pos, -3)
=======
        self.assertEqual(len(result.guides_to_keep), 1)
        self.assertEqual(len(result.guides_to_keep[0].codons), 2)
        self.assertEqual(result.guides_to_keep[0].codons[0].third_base_pos, -2)
        self.assertEqual(result.guides_to_keep[0].codons[1].third_base_pos, -3)

        self.assertEqual(len(result.guides_to_discard), 1)
        self.assertEqual(len(result.guides_to_discard[0].codons), 1)
        self.assertEqual(result.guides_to_discard[0].codons[0].third_base_pos, 1)
>>>>>>> dbafffa... TD-495code review changes
