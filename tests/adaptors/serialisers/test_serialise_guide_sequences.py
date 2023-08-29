from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from adaptors.serialisers.serialise_guide_sequences import write_guide_sequences_to_input_tsv
from mutator.guide import GuideSequence


class TestWriteGuideSequencesToInputTSV(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @patch('builtins.print')
    def test_write_guide_sequences_to_input_tsv(self, mock_print):
        # arrange
        guides = [
            GuideSequence(
                'chr16',
                67610855,
                67610877,
                is_positive_strand=True,
                guide_id='1139540371',
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
            ),
        ]
        expected = (
            'guide_id\tchr\tstart\tend\tgrna_strand\n'
            '1139540371\tchr16\t67610855\t67610877\t+\n'
            '1139541475\tchr16\t67620712\t67620734\t-\n'
        )

        # act
        write_guide_sequences_to_input_tsv('guides.tsv', guides)
        with open('guides.tsv') as f:
            actual = f.read()

        # assert
        self.assertEqual(expected, actual)
