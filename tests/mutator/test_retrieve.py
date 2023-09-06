from unittest import TestCase
from unittest.mock import Mock, patch, call
from mutator.target_region import TargetRegion
from mutator.retrieve import parse_dicts_to_target_regions, retrieve_data_for_region, parse_gff

class TestRetrieveModule(TestCase):

    def test_parse_dicts_to_target_regions(self):
        region1 = "chr19:111-222"
        region2 = "chr2:123-155"
        regions = [ {"id": "AAA", "region": region1}, {"id": "BBB", "region": region2} ]

        result = parse_dicts_to_target_regions(regions)

        expected_result = [
            TargetRegion(id="AAA", chromosome="19", start=111, end=222),
            TargetRegion(id="BBB", chromosome="2", start=123, end=155),
        ]

        self.assertEqual(result, expected_result)


    def test_parse_gff(self):
        gff_data = """##gff-version 3
    ##sequence-region lims2-region 48898521 48902973
    # Crisprs for region Human (GRCh38) X:48898521-48902973
    X	WGE	Crispr	48900478	48900500	.	-	.	ID=C_285858433;Name=285858433;Sequence=GCACCTAAGG AATCCGGCAG TGG (reversed);CopySequence=GCACCTAAGGAATCCGGCAGTGG;;OT_Summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98}
    X	WGE	CDS	48900480	48900500	.	-	.	ID=Cr_285858433;Parent=C_285858433;Name=285858433;color=#45A825;Sequence=GCACCTAAGGAATCCGGCAGTGG;
    X	WGE	CDS	48900478	48900480	.	-	.	ID=PAM_285858433;Parent=C_285858433;Name=285858433;color=#1A8599;Sequence=GCACCTAAGGAATCCGGCAGTGG"""

        expected_entries = [{
            'guide_id': '285858433',
            'chr': 'chrX',
            'start': 48900478,
            'end' : 48900500,
            'grna_strand': '-',
            'ot_summary': {0: 1, 1: 0, 2: 1, 3: 8, 4: 98},
            'seq': 'GCACCTAAGGAATCCGGCAGTGG',
        }]

        parsed_entries = parse_gff(gff_data)
        self.assertCountEqual(parsed_entries, expected_entries)
