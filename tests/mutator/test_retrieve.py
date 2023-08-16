from unittest import TestCase
from mutator.retrieve import parse_gff

class RetrieveModule(TestCase):
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
