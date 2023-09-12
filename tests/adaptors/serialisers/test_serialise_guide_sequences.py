from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from adaptors.serialisers.serialise_guide_sequences import write_guide_sequences_to_tsv
from mutator.guide import GuideSequence


class TestWriteGuideSequencesToInputTSV(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_guide_sequences_to_tsv(self):
        # arrange
        guides = [
            GuideSequence(
                'chr16',
                67610855,
                67610877,
                is_positive_strand=True,
                guide_id='1139540371',
                ot_summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98},
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 3, 4: 69},
            ),
        ]
        expected = (
            'guide_id\tchr\tstart\tend\tgrna_strand\tot_summary\n'
            '1139540371\tchr16\t67610855\t67610877\t+\t{0: 1, 1: 0, 2: 1, 3: 8, 4: 98}\n'
            '1139541475\tchr16\t67620712\t67620734\t-\t{0: 1, 1: 0, 2: 0, 3: 3, 4: 69}\n'
        )

        # act
        write_guide_sequences_to_tsv('guides.tsv', guides)
        with open('guides.tsv') as f:
            actual = f.read()

        # assert
        self.assertEqual(expected, actual)
