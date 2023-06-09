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
            'Frame': ['0', '2', '2'],
            'gene_name': ['CTCF', 'CTCF', 'CTCF'],
            'exon_number': ['3', '5', '5'],
        })
        self.coding_region = pd.DataFrame({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 67610833,
            'End': 67611613,
            'Strand': '+',
            'Frame': '0',
            'gene_name': 'CTCF',
            'exon_number': '3',
        }, index=[0])
        self.guide_data = {
            'guide_id': '1139540371',
            'chr': 'chr16',
            'start': '67610855',
            'end': '67610877',
        }

    def test_get_coding_region_for_guide_success(self):
        # arrange
        expected = self.coding_region

        # act
        actual = Mutator.get_coding_region_for_guide(self.gtf_data, self.guide_data)

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

    def test_add_guide_data_to_dataframe(self):
        # arrange
        expected = pd.DataFrame({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 67610833,
            'End': 67611613,
            'Strand': '+',
            'Frame': '0',
            'gene_name': 'CTCF',
            'exon_number': '3',
            'guide_start': 67610855,
            'guide_end': 67610877,
        }, index=pd.Index([1139540371], name='guide_id'))

        # act
        actual = Mutator.add_guide_data_to_dataframe(self.coding_region, self.guide_data)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)

    def test_determine_frame_for_guide_within_forward_strand_cds(self):
        # arrange
        test_row = pd.Series({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 67610833,
            'End': 67611613,
            'Strand': '+',
            'Frame': '0',
            'gene_name': 'CTCF',
            'exon_number': '3',
            'guide_start': 67610855,
            'guide_end': 67610877,
        }, name=1139540371)
        expected = '2'

        # act
        actual = Mutator.determine_frame_for_guide(test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_determine_frame_for_guide_starting_before_forward_strand_cds(self):
        # arrange
        test_row = pd.Series({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 67610856,
            'End': 67611613,
            'Strand': '+',
            'Frame': '0',
            'gene_name': 'CTCF',
            'exon_number': '3',
            'guide_start': 67610855,
            'guide_end': 67610877,
        }, name=1139540371)
        expected = '0'

        # act
        actual = Mutator.determine_frame_for_guide(test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_determine_frame_for_guide_within_reverse_strand_cds(self):
        # arrange
        test_row = pd.Series({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 3791981,
            'End': 3792094,
            'Strand': '-',
            'Frame': '2',
            'gene_name': 'CREBBP',
            'exon_number': '5',
            'guide_start': 3791982,
            'guide_end': 3792004,
        }, name=1133146650)
        expected = '2'

        # act
        actual = Mutator.determine_frame_for_guide(test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_determine_frame_for_guide_ending_after_reverse_strand_cds(self):
        # arrange
        test_row = pd.Series({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 3791981,
            'End': 3792003,
            'Strand': '-',
            'Frame': '2',
            'gene_name': 'CREBBP',
            'exon_number': '5',
            'guide_start': 3791982,
            'guide_end': 3792004,
        }, name=1133146650)
        expected = '2'

        # act
        actual = Mutator.determine_frame_for_guide(test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_adjust_columns_for_output(self):
        # arrange
        data = pd.DataFrame({
            'Chromosome': 'chr16',
            'Feature': 'CDS',
            'Start': 67610833,
            'End': 67611613,
            'Strand': '+',
            'Frame': '0',
            'gene_name': 'CTCF',
            'exon_number': '3',
            'guide_start': 67610855,
            'guide_end': 67610877,
            'guide_frame': '2',
        }, index=pd.Index([1139540371], name='guide_id'))
        expected = pd.DataFrame({
            'chromosome': 'chr16',
            'cds_start': 67610833,
            'cds_end': 67611613,
            'cds_strand': '+',
            'cds_frame': '0',
            'gene_name': 'CTCF',
            'exon_number': '3',
            'guide_start': 67610855,
            'guide_end': 67610877,
            'guide_frame': '2',
        }, index=pd.Index([1139540371], name='guide_id'))

        # act
        actual = Mutator.adjust_columns_for_output(data)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)