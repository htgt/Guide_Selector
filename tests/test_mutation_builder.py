from unittest import TestCase
from unittest.mock import patch

from coding_region import CodingRegion
from codon import WindowCodon
from edit_window import EditWindow
from guide import GuideSequence
from mutation_builder import MutationBuilder, get_window


class TestMutationBuilder(TestCase):
    @patch.object(GuideSequence, 'get_sequence_by_coords', return_value='CAGCATTCCTATATTGAGCAAGG')
    @patch.object(EditWindow, '_get_extended_window_bases', return_value='TATATTGAGCAAGG')
    def test_build_window_codons_plus_plus(self, mock_guide_sequence, mock_edit_window):
        guide = GuideSequence(
            chromosome='16',
            start=67626572,
            end=67626594,
            is_positive_strand=True,
            frame=0,
        )
        cds = CodingRegion(start=67626555, end=67626715, is_positive_strand=True, chromosome='16', frame=2)

        control_codons = [
            WindowCodon('TAT', 67626583, 9, True),
            WindowCodon('ATT', 67626586, 6, True),
            WindowCodon('GAG', 67626589, 3, True),
        ]

        config = {
            'edit_rules': {
                'ignore_positions': [-1, 1],
                'allow_codon_loss': True,
                'splice_mask_distance': 5,
            }
        }

        builder = MutationBuilder(
            guide=guide,
            cds=cds,
            gene_name='BRCA1',
            window_length=12,
            edits_config=config['edit_rules'],
        )

        window = builder.window
        codons = builder.build_window_codons()

        self.assertEqual(list(map(vars, codons)), list(map(vars, control_codons)))


class TestGetWindow(TestCase):
    @patch.object(GuideSequence, 'get_sequence_by_coords', return_value='CAGCATTCCTATATTGAGCAAGG')
    def test_get_window(self, mock_guide_sequence):
        # arrange
        coding_region = CodingRegion(
            start=67626572,
            end=67626594,
            is_positive_strand=True,
            frame=0,
        )

        expected_window = EditWindow(
            start=67626583,
            end=67626594,
            is_positive_strand=True,
            chromosome='chrX',
            frame=1,
            window_length=12,
        )

        guide = GuideSequence(
            chromosome='X',
            start=67626572,
            end=67626594,
            is_positive_strand=True,
            frame=0,
        )

        # act
        result_window = get_window(guide=guide, cds=coding_region, window_length=12)

        # assert
        self.assertEqual(result_window.__dict__, expected_window.__dict__)
