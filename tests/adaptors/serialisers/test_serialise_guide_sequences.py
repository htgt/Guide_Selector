from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch, PropertyMock

# fmt: off
from adaptors.serialisers.guide_sequences_serialiser import serialise_guide_sequence, write_guide_sequences_to_tsv  # NOQA
# fmt: on
from guide import GuideSequence
from target_region import TargetRegion


class TestWriteGuideSequencesToInputTSV(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @patch('guide.GuideSequence.centrality_score', new_callable=PropertyMock, return_value=0.5)
    def test_write_guide_sequences_to_tsv(self, mock):
        # arrange
        guides = [
            GuideSequence(
                'chr16',
                67610855,
                67610877,
                is_positive_strand=True,
                guide_id='1139540371',
                ot_summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98},
                target_region=TargetRegion('chr16', 67610850, 67611000, '123'),
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 3, 4: 69},
                target_region=TargetRegion('chr16', 67620700, 67620800, '321'),
            ),
        ]
        expected = (
            'target_region_id\tchr\ttarget_region_start\ttarget_region_end\tguide_id\t'
            'guide_start\tguide_end\tguide_strand\tot_summary\twge_percentile\tcentrality_score\n'
            '123\tchr16\t67610850\t67611000\t1139540371\t'
            '67610855\t67610877\t+\t{0: 1, 1: 0, 2: 1, 3: 8, 4: 98}\t50\t0.5\n'
            '321\tchr16\t67620700\t67620800\t1139541475\t'
            '67620712\t67620734\t-\t{0: 1, 1: 0, 2: 0, 3: 3, 4: 69}\t10\t0.5\n'
        )

        # act
        write_guide_sequences_to_tsv('guides.tsv', guides)
        with open('guides.tsv') as f:
            actual = f.read()

        # assert
        self.assertEqual(expected, actual)

    @patch('guide.GuideSequence.centrality_score', new_callable=PropertyMock, return_value=0.5)
    def test_serialise_guide_sequence_with_all_fields(self, mock):
        expected = {
            'chr': 'chr19',
            'guide_end': 50398874,
            'guide_strand': '+',
            'guide_id': 1167589901,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'wge_percentile': 25,
            'guide_start': 50398852,
            'target_region_id': '123456',
            'target_region_start': 50398850,
            'target_region_end': 50399000,
            'centrality_score': 0.5,
        }

        guide_sequence = GuideSequence(
            start=50398852,
            end=50398874,
            is_positive_strand=True,
            chromosome='chr19',
            frame=0,
            ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            target_region=TargetRegion('chr19', 50398850, 50399000, '123456'),
            guide_id=1167589901,
        )

        serialised_guide = serialise_guide_sequence(guide_sequence)

        self.assertEqual(serialised_guide, expected)

    def test_serialise_guide_sequence_only_required_fields(self):
        expected = {
            'chr': 'chr19',
            'guide_end': 50398874,
            'guide_strand': '+',
            'guide_id': '',
            'ot_summary': None,
            'wge_percentile': None,
            'guide_start': 50398852,
            'target_region_id': '',
            'target_region_start': None,
            'target_region_end': None,
            'centrality_score': None,
        }

        guide_sequence = GuideSequence(
            start=50398852,
            end=50398874,
            is_positive_strand=True,
            chromosome='chr19',
            frame=0,
            ot_summary=None,
            target_region=TargetRegion('chr19', None, None),
        )

        serialised_guide = serialise_guide_sequence(guide_sequence)

        self.assertEqual(serialised_guide, expected)
