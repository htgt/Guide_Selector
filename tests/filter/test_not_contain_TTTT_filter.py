import unittest
from unittest.mock import Mock

from filter.filter_response import GuideDiscarded
from filter.omit_TTTT_filter import OmitTTTTFilter


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

        test_instance = OmitTTTTFilter({})
        result = test_instance.apply([mb1, mb2, mb3])

        self.assertCountEqual(result.guides_to_keep, [mb2, mb3])
        self.assertCountEqual(result.guides_to_discard, [GuideDiscarded(mb1, OmitTTTTFilter.key)])
