from pyfakefs.fake_filesystem_unittest import TestCase

from guide import GuideSequence
from adaptors.parsers.parse_guide_tsv import read_guide_tsv_to_guide_sequences, deserialise_guide_sequence


class TestReadGuideTsvToGuideSequences(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_read_guide_tsv_to_guide_sequences_with_ot_summary(self):
        # arrange
        contents = (
            'guide_id\tchr\tstart\tend\tgrna_strand\ttarget_region_id\tot_summary\n'
            '1139540371\tchr16\t67610855\t67610877\t+\t44445\t{0: 1, 1: 0, 2: 0, 3: 4, 4: 76}\n'
            '1139541475\tchr16\t67620712\t67620734\t-\t44444\t{0: 1, 1: 0, 2: 0, 3: 26, 4: 265}\n'
        )
        self.fs.create_file('guides.tsv', contents=contents)

        expected = [
            GuideSequence(
                'chr16',
                67610855,
                67610877,
                is_positive_strand=True,
                guide_id='1139540371',
                target_region_id='44445',
                ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76}
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                target_region_id='44444',
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
            'guide_id\tchr\tstart\tend\tgrna_strand\ttarget_region_id\n'
            '1139540371\tchr16\t67610855\t67610877\t+\t12345\n'
            '1139541475\tchr16\t67620712\t67620734\t-\t54321\n'
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
                target_region_id='12345',
            ),
            GuideSequence(
                'chr16',
                67620712,
                67620734,
                is_positive_strand=False,
                guide_id='1139541475',
                ot_summary=None,
                target_region_id='54321',
            ),
        ]

        # act
        actual = read_guide_tsv_to_guide_sequences('guides.tsv')

        # assert
        self.assertEqual(list(map(vars, expected)), list(map(vars, actual)))

    def test_deserialise_guide_sequence_with_all_fields(self):
        guide = {
            'chr': 'chr19', 'end': '50398874',
            'grna_strand': '+',
            'guide_id': '1167589901',
            'ot_summary': '{0: 1, 1: 0, 2: 0, 3: 4, 4: 76}',
            'start': '50398852',
            'target_region_id': '123456'}

        expected = GuideSequence(
            start=50398852,
            end=50398874,
            is_positive_strand=True,
            chromosome='chr19',
            frame=0,
            ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            target_region_id='123456',
        )

        deserialised_guide = deserialise_guide_sequence(guide)

        self.assertEqual(deserialised_guide, expected)

    def test_deserialise_guide_sequence_with_just_required_fields(self):
        guide = {
            'chr': 'chr19', 'end': '50398874',
            'grna_strand': '+',
            'guide_id': '1167589901',
            'start': '50398852',
        }

        expected = GuideSequence(
            start=50398852,
            end=50398874,
            is_positive_strand=True,
            chromosome='chr19',
            frame=0,
            ot_summary=None,
            target_region_id=None,
        )

        deserialised_guide = deserialise_guide_sequence(guide)

        self.assertEqual(deserialised_guide, expected)
