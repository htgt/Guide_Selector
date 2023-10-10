import unittest
from unittest.mock import Mock

from filter.not_contain_TTTT_filter import NotContainTTTTFilter


def create_mutation_builder_with_bases(bases):
    mb = Mock()
    mb.guide = Mock()
    mb.guide.bases = bases

    return mb


class TestNotContainTTTTFilter(unittest.TestCase):
    def setUp(self) -> None:
        mb1 = create_mutation_builder_with_bases('CACATTTTTTAAACCCCC')
        mb2 = create_mutation_builder_with_bases('CACAAACTCTTTCCCTTCCAAAAAAA')
        mb3 = create_mutation_builder_with_bases('CACAAACAA')

        self.mutations_builder_to_filter = [mb1, mb2, mb3]

    def test_apply_filter_TTTT(self):
        test_instance = NotContainTTTTFilter()

        self.assertEqual(len(self.mutations_builder_to_filter), 3)

        result = test_instance.apply(self.mutations_builder_to_filter)

        self.assertEqual(len(result.guides_to_keep), 2)
        self.assertEqual(len(result.guides_to_discard), 1)

