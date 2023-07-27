from unittest import TestCase, mock

from utils.bio_utils import add_chr_prefix, remove_chr_prefix


class TestAddChrPrefix(TestCase):
    def test_add_chr_prefix_existing_prefix(self):
        # arrange
        expected = 'chr16'

        # act
        actual = add_chr_prefix('chr16')

        # assert
        self.assertEqual(expected, actual)

    def test_add_chr_prefix_no_prefix(self):
        # arrange
        expected = 'chr16'

        # act
        actual = add_chr_prefix('16')

        # assert
        self.assertEqual(expected, actual)


class TestRemoveChrPrefix(TestCase):
    def test_remove_chr_prefix_existing_prefix(self):
        # arrange
        expected = '16'

        # act
        actual = remove_chr_prefix('chr16')

        # assert
        self.assertEqual(expected, actual)

    def test_remove_chr_prefix_no_prefix(self):
        # arrange
        expected = '16'

        # act
        actual = remove_chr_prefix('16')

        # assert
        self.assertEqual(expected, actual)
