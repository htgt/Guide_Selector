from unittest import TestCase
from unittest.mock import patch
from guide import GuideSequence
from target_region import TargetRegion
from retriever.retriever import _retrieve_guides_for_region
from retriever.retriever_reader import _parse_dicts_to_target_regions
from utils.exceptions import GetDataFromWGEError


class TestRetrieveModule(TestCase):
    def setUp(self):
        self.target_region_1 = TargetRegion(id='AAA', chromosome='19', start=111, end=222)
        self.target_region_2 = TargetRegion(id='BBB', chromosome='2', start=123, end=155)
        self.request_options = {'species_id': 'Grch38', 'assembly': 'GRCh38'}

    def test_parse_dicts_to_target_regions(self):
        # arrange
        region1 = 'chr19:111-222'
        region2 = 'chr2:123-155'
        regions = [{'id': 'AAA', 'region': region1}, {'id': 'BBB', 'region': region2}]

        expected_result = [self.target_region_1, self.target_region_2]

        # act
        result = _parse_dicts_to_target_regions(regions)

        # assert
        self.assertEqual(result, expected_result)

    @patch('builtins.print')
    @patch('retriever.retriever.get_data_from_wge_by_coords')
    def test_retrieve_guides_for_region_success(self, mock_get_data, mock_print):
        # arrange
        mock_get_data.return_value = (
            '##gff-version 3\n'
            '##sequence-region lims2-region 48898521 48902973\n'
            '# Crisprs for region Human (GRCh38) X:48898521-48902973\n'
            'X	WGE	Crispr	48900478	48900500	.	-	.	'
            'ID=C_285858433;Name=285858433;Sequence=GCACCTAAGG AATCCGGCAG TGG (reversed);'
            'CopySequence=GCACCTAAGGAATCCGGCAGTGG;;OT_Summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98}\n'
            'X	WGE	CDS	48900480	48900500	.	-	.	ID=Cr_285858433;'
            'Parent=C_285858433;Name=285858433;color=#45A825;Sequence=GCACCTAAGGAATCCGGCAGTGG;\n'
            'X	WGE	CDS	48900478	48900480	.	-	.	ID=PAM_285858433;'
            'Parent=C_285858433;Name=285858433;color=#1A8599;Sequence=GCACCTAAGGAATCCGGCAGTGG'
        )
        expected = [GuideSequence(
            chromosome='X',
            start=48900478,
            end=48900500,
            is_positive_strand=False,
            guide_id='285858433',
            ot_summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98},
            target_region_id='AAA',
        )]

        # act
        actual = _retrieve_guides_for_region(self.target_region_1, self.request_options)

        # assert
        self.assertEqual(list(map(vars, expected)), list(map(vars, actual)))

    @patch('retriever.retriever.get_data_from_wge_by_coords')
    def test_retrieve_guides_for_region_no_data_raises_error(self, mock_get_data):
        # arrange
        mock_get_data.return_value = (
            '##gff-version 3\n'
            '##sequence-region lims2-region 503 533\n'
            '# Crisprs for region Grch38 (GRCh38) 19:503-533'
        )
        expected = 'No guides from WGE for given region: AAA'

        # act
        with self.assertRaises(GetDataFromWGEError) as cm:
            _retrieve_guides_for_region(self.target_region_1, self.request_options)

        # assert
        self.assertEqual(expected, str(cm.exception))
