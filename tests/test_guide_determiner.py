from unittest.mock import Mock

import pandas as pd
from pyfakefs.fake_filesystem_unittest import TestCase

from guide_determiner import GuideDeterminer
from utils.exceptions import GuideDeterminerError


class TestGuideDeterminer(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.gtf_data = pd.DataFrame(
            {
                'Chromosome': ['chr16', 'chr16', 'chr16'],
                'Feature': ['CDS', 'CDS', 'CDS'],
                'Start': [67610833, 67616745, 67616745],
                'End': [67611613, 67616878, 67616878],
                'Strand': ['+', '+', '+'],
                'Frame': [0, 2, 2],
                'gene_name': ['CTCF', 'CTCF', 'CTCF'],
                'exon_number': ['3', '5', '5'],
            }
        )
        self.coding_region = pd.DataFrame(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 67610833,
                'End': 67611613,
                'Strand': '+',
                'Frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
            },
            index=[0],
        )
        self.guide_sequence = Mock(
            guide_id='1139540371',
            chromosome='chr16',
            start=67610855,
            end=67610877,
            strand_symbol='+',
            target_region_id='1139540371',
            ot_summary={0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
            on_target_score=0.87,
        )

    def test_get_coding_region_for_guide_success(self):
        # arrange
        mock_object = Mock()
        expected = self.coding_region

        # act
        actual = GuideDeterminer._get_coding_region_for_guide(mock_object, self.gtf_data, self.guide_sequence)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)

    def test_get_coding_region_for_guide_raises_error_when_no_region_found(self):
        # arrange
        mock_object = Mock()
        guide_sequence = Mock(
            guide_id='1139541475',
            chromosome='chr16',
            start=67620712,
            end=67620734,
        )
        expected = 'Guide 1139541475 does not overlap with any coding regions'

        # act
        with self.assertRaises(GuideDeterminerError) as cm:
            GuideDeterminer._get_coding_region_for_guide(mock_object, self.gtf_data, guide_sequence)

        # assert
        self.assertEqual(str(cm.exception), expected)

    def test_get_coding_region_for_guide_raises_error_when_multiple_regions_found(self):
        # arrange
        mock_object = Mock()
        guide_sequence = Mock(
            guide_id='1139541055',
            chromosome='chr16',
            start=67616774,
            end=67616796,
        )
        expected = 'Guide 1139541055 overlaps with multiple coding regions'

        # act
        with self.assertRaises(GuideDeterminerError) as cm:
            GuideDeterminer._get_coding_region_for_guide(mock_object, self.gtf_data, guide_sequence)

        # assert
        self.assertEqual(str(cm.exception), expected)

    def test_add_guide_data_to_dataframe(self):
        # arrange
        mock_object = Mock()
        expected = pd.DataFrame(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 67610833,
                'End': 67611613,
                'Strand': '+',
                'Frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
                'guide_start': 67610855,
                'guide_end': 67610877,
                'guide_strand': '+',
                'target_region_id': '1139540371',
                'ot_summary': [{0: 1, 1: 0, 2: 0, 3: 4, 4: 76}],
                'on_target_score': 0.87,
            },
            index=pd.Index(['1139540371'], name='guide_id'),
        )

        # act
        actual = GuideDeterminer._add_guide_data_to_dataframe(mock_object, self.coding_region, self.guide_sequence)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)

    def test_add_guide_data_to_dataframe_no_on_target_score(self):
        # arrange
        mock_object = Mock()
        expected = pd.DataFrame(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 67610833,
                'End': 67611613,
                'Strand': '+',
                'Frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
                'guide_start': 67610855,
                'guide_end': 67610877,
                'guide_strand': '+',
                'target_region_id': '1139540371',
                'ot_summary': [{0: 1, 1: 0, 2: 0, 3: 4, 4: 76}],
                'on_target_score': None,
            },
            index=pd.Index(['1139540371'], name='guide_id'),
        )

        # act
        self.guide_sequence.on_target_score = None
        actual = GuideDeterminer._add_guide_data_to_dataframe(mock_object, self.coding_region, self.guide_sequence)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)

    def test_determine_frame_for_guide_within_forward_strand_cds(self):
        # arrange
        mock_object = Mock()
        test_row = pd.Series(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 67610833,
                'End': 67611613,
                'Strand': '+',
                'Frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
                'guide_start': 67610855,
                'guide_end': 67610877,
            },
            name='1139540371',
        )
        expected = 2

        # act
        actual = GuideDeterminer._determine_frame_for_guide(mock_object, test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_determine_frame_for_guide_starting_before_forward_strand_cds(self):
        # arrange
        mock_object = Mock()
        test_row = pd.Series(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 67610856,
                'End': 67611613,
                'Strand': '+',
                'Frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
                'guide_start': 67610855,
                'guide_end': 67610877,
            },
            name='1139540371',
        )
        expected = 1

        # act
        actual = GuideDeterminer._determine_frame_for_guide(mock_object, test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_determine_frame_for_guide_within_reverse_strand_cds(self):
        # arrange
        mock_object = Mock()
        test_row = pd.Series(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 3791981,
                'End': 3792094,
                'Strand': '-',
                'Frame': 2,
                'gene_name': 'CREBBP',
                'exon_number': '5',
                'guide_start': 3791982,
                'guide_end': 3792004,
            },
            name='1133146650',
        )
        expected = 2

        # act
        actual = GuideDeterminer._determine_frame_for_guide(mock_object, test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_determine_frame_for_guide_ending_after_reverse_strand_cds(self):
        # arrange
        mock_object = Mock()
        test_row = pd.Series(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 3791981,
                'End': 3792003,
                'Strand': '-',
                'Frame': 2,
                'gene_name': 'CREBBP',
                'exon_number': '5',
                'guide_start': 3791982,
                'guide_end': 3792004,
            },
            name='1133146650',
        )
        expected = 0

        # act
        actual = GuideDeterminer._determine_frame_for_guide(mock_object, test_row)

        # assert
        self.assertEqual(actual, expected)

    def test_adjust_columns_for_output(self):
        # arrange
        mock_object = Mock()
        data = pd.DataFrame(
            {
                'Chromosome': 'chr16',
                'Feature': 'CDS',
                'Start': 67610833,
                'End': 67611613,
                'Strand': '+',
                'Frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
                'guide_strand': True,
                'guide_start': 67610855,
                'guide_end': 67610877,
                'guide_frame': 2,
                'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
                'target_region_id': '123',
                'on_target_score': 0.87,
            },
            index=pd.Index(['1139540371'], name='guide_id'),
        )
        expected = pd.DataFrame(
            {
                'chromosome': 'chr16',
                'cds_start': 67610833,
                'cds_end': 67611613,
                'cds_strand': '+',
                'cds_frame': 0,
                'gene_name': 'CTCF',
                'exon_number': '3',
                'guide_strand': True,
                'guide_start': 67610855,
                'guide_end': 67610877,
                'guide_frame': 2,
                'ot_summary': {0: 1, 1: 0, 2: 0, 3: 4, 4: 76},
                'on_target_score': 0.87,
                'target_region_id': '123',
            },
            index=pd.Index(['1139540371'], name='guide_id'),
        )

        # act
        actual = GuideDeterminer._adjust_columns_for_output(mock_object, data)

        # assert
        pd.testing.assert_frame_equal(actual, expected, check_exact=True)
