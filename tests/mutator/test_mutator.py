from unittest import TestCase

import pandas as pd

from mutator.mutator import Mutator
from utils.exceptions import MutatorError


class TestMutator(TestCase):
    def setUp(self):
        self.gtf_data = pd.DataFrame({
            'Chromosome': ['chr16', 'chr16', 'chr16'],
            'Feature': ['CDS', 'CDS', 'CDS'],
            'Start': [67610833, 67616745, 67616745],
            'End': [67611613, 67616878, 67616878],
            'Strand': ['+', '+', '+'],
            'Frame': [0, 2, 2],
            'gene_name': ['CTCF', 'CTCF', 'CTCF'],
            'exon_number': ['3', '5', '5'],
        })

    def test_get_coding_region_for_guide(self):
        # arrange
        guide_data = {
            'guide_id': '1139540371',
            'chr': 'chr16',
            'start': '67610855',
            'end': '67610877',
        }
        expected = pd.DataFrame({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 67610833,
            'End': 67611613,
            'Strand': '+',
            'Frame': 0,
            'gene_name': 'CTCF',
            'exon_number': '3',
        }, index=pd.Index([1139540371], name='guide_id'))

        # act
        actual = Mutator.get_coding_region_for_guide(self.gtf_data, guide_data)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)

    def test_get_coding_region_for_guide_raises_error_when_no_region_found(self):
        # arrange
        guide_data = {
            'guide_id': '1139541475',
            'chr': 'chr16',
            'start': '67620712',
            'end': '67620734',
        }
        expected = 'Guide 1139541475 does not overlap with any coding regions'

        # act
        with self.assertRaises(MutatorError) as cm:
            print(Mutator.get_coding_region_for_guide(self.gtf_data, guide_data))

        # assert
        self.assertEqual(str(cm.exception), expected)

    def test_get_coding_region_for_guide_raises_error_when_multiple_regions_found(self):
        # arrange
        guide_data = {
            'guide_id': '1139541055',
            'chr': 'chr16',
            'start': '67616774',
            'end': '67616796'
        }
        expected = 'Guide 1139541055 overlaps with multiple coding regions'

        # act
        with self.assertRaises(MutatorError) as cm:
            Mutator.get_coding_region_for_guide(self.gtf_data, guide_data)

        # assert
        self.assertEqual(str(cm.exception), expected)
