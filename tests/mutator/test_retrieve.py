from unittest import TestCase
from unittest.mock import Mock, patch, call
from mutator.retrieve import get_guides_data, retrieve_data_for_region, parse_gff

class RetrieveModule(TestCase):

    @patch('mutator.retrieve.retrieve_data_for_region')
    def test_get_guides_data(self, mock_retrieve_data_for_region):
        region1 = "chr19:111-222"
        region2 = "chr2:123-155"
        regions = [ {"id": "AAA", "region": region1}, {"id": "BBB", "region": region2} ]
        config = {}

        def return_function(region, config):
            if region == region1:
                return {'guide_id': '263969621', 'chr': 'chr19', 'start': 50398851, 'end': 50398873, 'grna_strand': '+', 'ot_summary': '263969621', 'seq': 'TGGGATGAAAAACGTGGGACAGG'},
            if region == region2:
                return {'guide_id': '22222', 'chr': 'chr2', 'start': 133, 'end': 150, 'grna_strand': '-', 'ot_summary': '1111', 'seq': 'TGGGAT'},

        mock_retrieve_data_for_region.side_effect = return_function

        result = get_guides_data(regions, config)

        expected_result = [
            {'guide_id': '263969621', 'chr': 'chr19', 'start': 50398851, 'end': 50398873, 'grna_strand': '+', 'ot_summary': '263969621', 'seq': 'TGGGATGAAAAACGTGGGACAGG'},
            {'guide_id': '22222', 'chr': 'chr2', 'start': 133, 'end' : 150, 'grna_strand': '-', 'ot_summary': '1111', 'seq': 'TGGGAT'},
        ]

        self.assertEqual(result, expected_result)

        calls = [call(region1, config), call(region2, config)]
        mock_retrieve_data_for_region.assert_has_calls(calls)

    def test_parse_gff(self):
        gff_data = """##gff-version 3
    ##sequence-region lims2-region 48898521 48902973
    # Crisprs for region Human (GRCh38) X:48898521-48902973
    X	WGE	Crispr	48900478	48900500	.	-	.	ID=C_285858433;Name=285858433;Sequence=GCACCTAAGG AATCCGGCAG TGG (reversed);CopySequence=GCACCTAAGGAATCCGGCAGTGG;;OT_Summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98}
    X	WGE	CDS	48900480	48900500	.	-	.	ID=Cr_285858433;Parent=C_285858433;Name=285858433;color=#45A825;Sequence=GCACCTAAGGAATCCGGCAGTGG;
    X	WGE	CDS	48900478	48900480	.	-	.	ID=PAM_285858433;Parent=C_285858433;Name=285858433;color=#1A8599;Sequence=GCACCTAAGGAATCCGGCAGTGG"""

        expected_entries = [
            {'guide_id'     : '285858433', 'chr': 'chrX', 'start': 48900478,
                'end'       : 48900500, 'grna_strand': '-',
                'ot_summary': '285858433', 'seq': 'GCACCTAAGGAATCCGGCAGTGG'}]

        parsed_entries = parse_gff(gff_data)
        self.assertCountEqual(parsed_entries, expected_entries)
