import unittest
from unittest.mock import Mock

from filter.edit_GG_in_PAM_filter import EditGGInPAMFilter


class TestEditGGInPAMFilter(unittest.TestCase):
    def setUp(self) -> None:
        config = {'filters': {'min_edits_allowed': 3, 'NGG_edit_required': True}}
        self.test_instance = EditGGInPAMFilter(config)
        self.mutation_builder = Mock()
        codon_filtered = Mock()
        codon_filtered.third_base_pos = 1
        codon_not_filtered1 = Mock()
        codon_not_filtered1.third_base_pos = -2
        codon_not_filtered2 = Mock()
        codon_not_filtered2.third_base_pos = -3
        self.mutation_builder.codons = [codon_filtered, codon_not_filtered1, codon_not_filtered2]

    def test_apply_when_no_mutation_builders(self):
        mutation_builders = []

        filtered_result = self.test_instance.apply(mutation_builders)

        self.assertEqual(filtered_result, [])

    def test_apply(self):
        mutation_builders = [self.mutation_builder]

        self.assertEqual(len(self.mutation_builder.codons), 3)

        result = self.test_instance.apply(mutation_builders)

        self.assertEqual(len(result[0].codons), 1)
        self.assertEqual(result[0].codons[0].third_base_pos, 1)
