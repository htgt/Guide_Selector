import unittest
from unittest.mock import Mock

from filter.filter_response import GuideDiscarded
from filter.omit_TTTT_filter import OmitTTTTFilter


def create_mutation_builder_with_bases_and_strand(bases, is_positive_strand):
    mb = Mock()
    mb.guide = Mock()
    mb.guide.bases = bases
    mb.guide.is_positive_strand = is_positive_strand

    return mb


class TestNotContainTTTTFilter(unittest.TestCase):
    def test_apply_filter_TTTT(self):
        mb1 = create_mutation_builder_with_bases_and_strand('CACATTTTTTAAACCCCC', True)
        mb2 = create_mutation_builder_with_bases_and_strand('CACAAACTCTTTCCCTTCCAAAAAAA', True)
        mb3 = create_mutation_builder_with_bases_and_strand('CACAAACAA', True)

        test_instance = OmitTTTTFilter({})
        result = test_instance.apply([mb1, mb2, mb3])

        self.assertCountEqual(result.guides_to_keep, [mb2, mb3])
        self.assertCountEqual(result.guides_to_discard, [GuideDiscarded(mb1, OmitTTTTFilter.key)])

    def test_apply_filter_TTTT_for_negative_strand(self):
        mb1 = create_mutation_builder_with_bases_and_strand('CACATTTTTTAAACCCCC', False)
        mb2 = create_mutation_builder_with_bases_and_strand('CACAAACTCTTTCCCTTCCAAAAAAA', False)
        mb3 = create_mutation_builder_with_bases_and_strand('CACAAACAA', False)

        test_instance = OmitTTTTFilter({})
        result = test_instance.apply([mb1, mb2, mb3])

        self.assertCountEqual(result.guides_to_keep, [mb1, mb3])
        self.assertCountEqual(result.guides_to_discard,
                              [GuideDiscarded(mb2, OmitTTTTFilter.key)])
        