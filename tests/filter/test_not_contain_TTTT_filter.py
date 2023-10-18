import unittest
from unittest.mock import Mock

from filter.not_contain_TTTT_filter import NotContainTTTTFilter


def create_mutation_builder_with_bases(bases):
    mb = Mock()
    mb.guide = Mock()
    mb.guide.bases = bases

    return mb


class TestNotContainTTTTFilter(unittest.TestCase):
    def test_apply_filter_TTTT(self):
        mb1 = create_mutation_builder_with_bases('CACATTTTTTAAACCCCC')
        mb2 = create_mutation_builder_with_bases('CACAAACTCTTTCCCTTCCAAAAAAA')
        mb3 = create_mutation_builder_with_bases('CACAAACAA')

        test_instance = NotContainTTTTFilter({})
        result = test_instance.apply([mb1, mb2, mb3])

        self.assertCountEqual(result.guides_to_keep, [mb2, mb3])
        self.assertCountEqual(result.guides_to_discard, [mb1])
