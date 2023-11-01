from pyfakefs.fake_filesystem_unittest import TestCase

from adaptors.parsers.parse_on_target_score_tsv import get_guides_on_target_scores


class TestReadOnTargetScoreFile(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_read_on_target_file(self):
        contents = (
            'Guide\tOn-target Score\n'
            '1167589901\t0.86\n'
            '1167589902\t0.4\n'
        )
        expected = {1167589901: 0.86, 1167589902: 0.4}
        file_name = 'on_target_score.tsv'
        self.fs.create_file(file_name, contents=contents)

        result = get_guides_on_target_scores(file_name)

        self.assertEqual(result, expected)

    def test_read_on_target_file_when_no_file_passed(self):
        result = get_guides_on_target_scores('')

        self.assertEqual(result, {})

    def test_read_on_target_file_when_file_does_not_exists(self):
        with self.assertRaises(FileNotFoundError) as error:
            get_guides_on_target_scores('Non existing file.txt')

        self.assertEqual(str(error.exception), 'Unable to find file: Non existing file.txt')
