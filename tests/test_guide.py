from unittest import TestCase
from unittest.mock import Mock

from guide import GuideSequence, SequenceFragment
from utils.exceptions import PamNotFoundError


class TestGuideSequence(TestCase):
    def test_strand_symbol_positive(self):
        # arrange
        mock_obj = Mock(is_positive_strand=True)
        expected = '+'

        # act
        actual = GuideSequence.strand_symbol.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_strand_symbol_negative(self):
        # arrange
        mock_obj = Mock(is_positive_strand=False)
        expected = '-'

        # act
        actual = GuideSequence.strand_symbol.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_guide_find_pam_real_coords_positive_strand(self):
        bases = "ATATTGAGCAAGG"

        guide = GuideSequence('chr16', 67626582, 67626594, is_positive_strand=True)
        pam = SequenceFragment("AGG", 67626592, 67626594)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam)

    def test_guide_find_pam_negative_strand(self):
        bases = "GCCATTGTCCGGGAGTCAGAAACT"
        guide = GuideSequence('chr1', 0, 22, is_positive_strand=False)

        pam_fragment_negative = SequenceFragment("CCA", 1, 3)

        test_pam = guide.find_pam(bases)

        self.assertEqual(test_pam, pam_fragment_negative)

    def test_centrality_score_perfect(self):
        # arrange
        mock_obj = Mock(target_region=Mock(start=50398851, end=50399053))
        mock_obj.find_pam.return_value = Mock(start=50398951)
        expected = 1

        # act
        actual = GuideSequence.centrality_score.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_centrality_score_pam_closer_to_end(self):
        # arrange
        mock_obj = Mock(target_region=Mock(start=50398851, end=50399053))
        mock_obj.find_pam.return_value = Mock(start=50399050)
        expected = 0.5099

        # act
        actual = GuideSequence.centrality_score.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_centrality_score_pam_closer_to_start(self):
        # arrange
        mock_obj = Mock(target_region=Mock(start=50398851, end=50399053))
        mock_obj.find_pam.return_value = Mock(start=50398900)
        expected = 0.7475

        # act
        actual = GuideSequence.centrality_score.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_centrality_score_no_target_region(self):
        # arrange
        mock_obj = Mock(target_region=Mock(start=None, end=None))
        expected = None

        # act
        actual = GuideSequence.centrality_score.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)

    def test_centrality_score_pam_not_found(self):
        # arrange
        mock_obj = Mock(target_region=Mock(start=50398851, end=50399053))
        mock_obj.find_pam.return_value = PamNotFoundError()
        expected = None

        # act
        actual = GuideSequence.centrality_score.fget(mock_obj)

        # assert
        self.assertEqual(expected, actual)
