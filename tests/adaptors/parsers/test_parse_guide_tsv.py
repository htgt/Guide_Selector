from pyfakefs.fake_filesystem_unittest import TestCase

from mutator.guide import GuideSequence
from adaptors.parsers.parse_guide_tsv import read_guide_tsv_to_guide_sequences


class TestReadGuideTsvToGuideSequences(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_read_guide_tsv_to_guide_sequences_with_ot_summary(self):
        # arrange
        contents = (
            'guide_id\tchr\tstart\tend\tgrna_strand\tot_summary\n'
            '1139540371\tchr16\t67610855\t67610877\t+\t{0: 1, 1: 0, 2: 0, 3: 4, 4: 76}\n'
            '1139541475\tchr16\t67620712\t67620734\t-\t{0: 1, 1: 0, 2: 0, 3: 26, 4: 265}\n'
        )
        self.fs.create_file('guides.tsv', contents=contents)

        expected = [
            GuideSequence(
                'chr16',
                67610855,
                67610877,
                is_positive_strand=True,
                guide_id='1139540371',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76}
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 26, 4: 265}
            ),
        ]

        # act
        actual = read_guide_tsv_to_guide_sequences('guides.tsv')

        # assert
        self.assertEqual(list(map(vars, expected)), list(map(vars, actual)))

    def test_read_guide_tsv_to_guide_sequences_without_ot_summary(self):
        # arrange
        contents = (
            'guide_id\tchr\tstart\tend\tgrna_strand\n'
            '1139540371\tchr16\t67610855\t67610877\t+\n'
            '1139541475\tchr16\t67620712\t67620734\t-\n'
        )
        self.fs.create_file('guides.tsv', contents=contents)

        expected = [
            GuideSequence(
                'chr16',
                67610855,
                67610877,
                is_positive_strand=True,
                guide_id='1139540371',
                ot_summary=None,
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                ot_summary=None,
            ),
        ]

        # act
        actual = read_guide_tsv_to_guide_sequences('guides.tsv')

        # assert
        self.assertEqual(list(map(vars, expected)), list(map(vars, actual)))
