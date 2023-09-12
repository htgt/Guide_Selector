from unittest import TestCase
from unittest.mock import patch

from mutator.mutation_builder import get_window, MutationBuilder
from mutator.base_sequence import BaseSequence
from mutator.coding_region import CodingRegion
from mutator.guide import GuideSequence
from mutator.edit_window import EditWindow
from mutator.codon import WindowCodon


class TestMutationBuilder(TestCase):

    @patch.object(GuideSequence, 'get_sequence_by_coords', return_value='CAGCATTCCTATATTGAGCAAGG')
    @patch.object(EditWindow, '_get_extended_window_bases', return_value='TATATTGAGCAAGG')
    def test_build_window_codons_plus_plus(self, mock_guide_sequence, mock_edit_window):
        guide = GuideSequence(
            chromosome='16',
            start=67626572,
            end=67626594,
            is_positive_strand=True,
            frame=0
        )
        cds = CodingRegion(
            start=67626555,
            end=67626715,
            is_positive_strand=True,
            chromosome='16',
            frame=2
        )

        control_codons = [
            WindowCodon('TAT', 67626583, 9, True),
            WindowCodon('ATT', 67626586, 6, True),
            WindowCodon('GAG', 67626589, 3, True),
            WindowCodon('CAA', 67626592, -1, True),
        ]

        builder = MutationBuilder(
            guide=guide,
            cds=cds,
            gene_name='BRCA1',
            window_length=12,
        )
        window = builder.window
        codons = builder.build_window_codons()

        self.assertEqual(list(map(vars, codons)), list(map(vars, control_codons)))


class TestGetWindow(TestCase):
    def test_get_window(self):
        bases = "CAGCATTCCTATATTGAGCAAGG"
        guide_start = 67626572
        guide_end = 67626594
        guide_frame = 0

        coding_region = CodingRegion(67626572, 67626594, True, 0)

        def mock_get_sequence_by_coords():
            return bases

        window_start = 67626583
        window_end = 67626594
        window_frame = 1
        window_length = 12

        window = EditWindow(
            start=window_start,
            end=window_end,
            is_positive_strand=True,
            chromosome='X',
            frame=window_frame,
            window_length=window_length,
        )

        with patch.object(
                GuideSequence,
                'get_sequence_by_coords',
                side_effect=mock_get_sequence_by_coords
        ):
            guide = GuideSequence(
                chromosome='X',
                start=guide_start,
                end=guide_end,
                is_positive_strand=True,
                frame=guide_frame,
            )
            result_window = get_window(guide, coding_region, window_length)

        self.assertEqual(result_window.start, window.start)
        self.assertEqual(result_window.end, window.end)
        