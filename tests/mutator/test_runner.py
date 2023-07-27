import unittest
import copy
from mutator.runner import Runner
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequence
from mutator.coding_region import CodingRegion
from mutator.edit_window import EditWindow
from mutator.codon import WindowCodon
import pandas as pd

class RunnerTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = Runner()

    def test_build_coding_region_objects(self):
        data = {
            'cds_start': 100,
            'cds_end': 200,
            'cds_strand': '+',
            'chromosome': 'chr1',
            'cds_frame': 1,
            'window_start': 150,
            'window_end': 180,
            'guide_strand': '+',
            'guide_id': 123,
            'guide_start': 160,
            'guide_end': 170,
            'gene_name': 'ACT'
        }

        self.runner.build_coding_region_objects(data)

        self.assertIsInstance(self.runner.cds, BaseSequence)
        self.assertIsInstance(self.runner.window, EditWindow)
        self.assertIsInstance(self.runner.guide, GuideSequence)

    def test_as_row(self):
        self.runner.cds = BaseSequence(100, 200, True, '1', 1)
        self.runner.window = EditWindow(150, 180, True, '1')
        self.runner.guide = GuideSequence(
            start=160,
            end=170,
            is_positive_strand=True,
            guide_id=123,
            chromosome='1'
        )
        self.runner.gene_name = 'ACT'
        self.runner.codons = [WindowCodon('TCA', 23, 1, True)]

        rows = self.runner.as_rows()

        expected_rows = [{
            'guide_id': 123,
            'chromosome': '1',
            'cds_strand': True,
            'gene_name': 'ACT',
            'guide_strand': True,
            'guide_start': 160,
            'guide_end': 170,
            'window_pos': 1,
            'pos': 23,
            'ref_codon': 'TCA',
            'ref_pos_three': 'A'
        }]

        self.assertEqual(rows, expected_rows)

    def test_fill_guide_sequence(self):
        row = pd.Series({
            'guide_start': 160,
            'guide_end': 170,
            'chromosome': 'chr1',
            'cds_strand': '+',
            'guide_frame': 2
        })

        guide_sequence = self.runner.fill_guide_sequence(row)

        self.assertIsInstance(guide_sequence, GuideSequence)
        self.assertEqual(guide_sequence.start, 160)
        self.assertEqual(guide_sequence.end, 170)
        self.assertEqual(guide_sequence.chromosome, 'chr1')
        self.assertEqual(guide_sequence.is_positive_strand, True)
        self.assertEqual(guide_sequence.guide_id, None)  # Ensure guide_id is not set in the test

    def test_fill_coding_region(self):
        row = pd.Series({
            'cds_start': 100,
            'cds_end': 200,
            'chromosome': 'chr1',
            'cds_strand': '+',
            'exon_number': 1,
            'cds_frame': 1
        })

        coding_region = self.runner.fill_coding_region(row)

        self.assertIsInstance(coding_region, CodingRegion)
        self.assertEqual(coding_region.start, 100)
        self.assertEqual(coding_region.end, 200)
        self.assertEqual(coding_region.chromosome, 'chr1')
        self.assertEqual(coding_region.is_positive_strand, True)
        self.assertEqual(coding_region.exon_number, 1)
        self.assertEqual(coding_region.frame, 1)

if __name__ == '__main__':
    unittest.main()
