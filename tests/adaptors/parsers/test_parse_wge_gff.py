from unittest import TestCase

from guide import GuideSequence
from adaptors.parsers.parse_wge_gff import read_wge_gff_to_guide_sequences


class TestReadGffToGuideSequences(TestCase):
    def test_read_gff_to_guide_sequences(self):
        # arrange
        gff_data = (
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
            guide_id='285858433',
            is_positive_strand=False,
            ot_summary={0: 1, 1: 0, 2: 1, 3: 8, 4: 98},
        )]

        # act
        actual = read_wge_gff_to_guide_sequences(gff_data)

        # assert
        self.assertEqual(list(map(vars, expected)), list(map(vars, actual)))
