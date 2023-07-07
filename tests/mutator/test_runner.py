import unittest
from mutator.runner import Runner, mutator_to_dict_list
from mutator.base_sequence import BaseSequence
from mutator.guide import GuideSequenceLoci
from mutator.edit_window import EditWindow, WindowCodon, BaseWithPosition


class RunnerTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = Runner()

    def test_window_frame(self):
        row = {
            'cds_start': '100',
            'cds_end': '200',
            'cds_strand': '+',
            'chromosome': 'chr1',
            'cds_frame': '1',
            'window_start': '150',
            'window_end': '180',
            'guide_strand': '+',
            'guide_id': '123',
            'guide_start': '160',
            'guide_end': '170',
            'gene_name': 'ACT'
        }

        self.runner.window_frame(row)

        self.assertIsInstance(self.runner.cds, BaseSequence)
        self.assertIsInstance(self.runner.window, EditWindow)
        self.assertIsInstance(self.runner.codons[0], WindowCodon)

    def test_build_coding_region_objects(self):
        data = {
            'cds_start': '100',
            'cds_end': '200',
            'cds_strand': '+',
            'chromosome': 'chr1',
            'cds_frame': '1',
            'window_start': '150',
            'window_end': '180',
            'guide_strand': '+',
            'guide_id': '123',
            'guide_start': '160',
            'guide_end': '170',
            'gene_name': 'ACT'
        }

        self.runner.build_coding_region_objects(data)

        self.assertIsInstance(self.runner.cds, BaseSequence)
        self.assertIsInstance(self.runner.window, EditWindow)
        self.assertIsInstance(self.runner.guide, GuideSequenceLoci)

    def test_as_row(self):
        self.runner.cds = BaseSequence(100, 200, True, '1', 1)
        self.runner.window = EditWindow(150, 180, True, '1')
        self.runner.guide = GuideSequenceLoci(
            guide_id=123,
            start=160,
            end=170,
            isPositiveStrand=True,
            chromosome='1'
        )
        self.runner.codon = WindowCodon('TCA', BaseWithPosition('A', 23, 1))

        row = self.runner.as_row()

        expected_row = {
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
        }

        self.assertEqual(row, expected_row)

    def test_mutator_to_dict_list(self):
        # Create a list of Runner objects
        runners = [
            Runner(100, 200, True, 'chr1', 0),
            Runner(150, 250, False, 'chrX', 1),
            Runner(200, 300, True, 'chr2', 2)
        ]

        # Convert the Runner objects to a list of dictionaries
        dict_list = mutator_to_dict_list(runners)

        # Assert that the dict_list is of the correct length
        self.assertEqual(len(dict_list), len(runners))

        # Assert that the dictionaries in dict_list match the expected format
        for i, runner in enumerate(runners):
            expected_dict = runner.as_row()
            actual_dict = dict_list[i]
            self.assertDictEqual(actual_dict, expected_dict)
        


if __name__ == '__main__':
    unittest.main()
