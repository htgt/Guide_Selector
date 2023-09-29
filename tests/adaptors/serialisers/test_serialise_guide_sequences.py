from pyfakefs.fake_filesystem_unittest import TestCase

# fmt: off
from adaptors.serialisers.serialise_guide_sequences import serialise_guide_sequence, write_guide_sequences_to_tsv  # NOQA # fmt: on
from guide import GuideSequence


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
                target_region_id='123',
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 3, 4: 69},
                target_region_id='321',
            ),
        ]
        expected = (
            'target_region_id\tguide_id\tchr\tstart\tend\tgrna_strand\tot_summary\twge_percentile\n'
            '123\t1139540371\tchr16\t67610855\t67610877\t+\t{0: 1, 1: 0, 2: 1, 3: 8, 4: 98}\t50\n'
            '321\t1139541475\tchr16\t67620712\t67620734\t-\t{0: 1, 1: 0, 2: 0, 3: 3, 4: 69}\t10\n'
        )

        # act
        write_guide_sequences_to_tsv('guides.tsv', guides)
        with open('guides.tsv') as f:
            actual = f.read()

        # assert
        self.assertEqual(expected, actual)

    def test_serialise_guide_sequence_with_all_fields(self):
        expected = {
            'chr': 'chr19',
            'end': 50398874,
            'grna_strand': '+',
            'guide_id': 1167589901,
            'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            'wge_percentile': 25,
            'start': 50398852,
            'target_region_id': '123456',
        }

        guide_sequence = GuideSequence(
            start=50398852,
            end=50398874,
            is_positive_strand=True,
            chromosome='chr19',
            frame=0,
            ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            target_region_id='123456',
            guide_id=1167589901,
        )

        serialised_guide = serialise_guide_sequence(guide_sequence)

        self.assertEqual(serialised_guide, expected)

    def test_serialise_guide_sequence_with_just_required_fields(self):
        expected = {
            'chr': 'chr19',
            'end': 50398874,
            'grna_strand': '+',
            'guide_id': '',
            'ot_summary': None,
            'wge_percentile': None,
            'start': 50398852,
            'target_region_id': None,
        }

        guide_sequence = GuideSequence(
            start=50398852,
            end=50398874,
            is_positive_strand=True,
            chromosome='chr19',
            frame=0,
            ot_summary=None,
            target_region_id=None,
        )

        serialised_guide = serialise_guide_sequence(guide_sequence)

        self.assertEqual(serialised_guide, expected)
