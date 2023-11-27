from io import StringIO
from unittest import TestCase

import pandas as pd
from pandas.testing import assert_frame_equal

from ranker.ranker import Ranker


class RankerTest(TestCase):
    def test_ranker(self):
        config = {"ranking_priority_order": ["off_target", "centrality", "on_target"]}

        data = '''
            wge_percentile    centrality    on_target_score
            1    4    3
            1    4    2
            2    3    5
            1    1    2
            '''
        expected = '''
            wge_percentile    centrality    on_target_score
            1    4    3
            1    4    2
            1    1    2
            2    3    5
            '''

        ranked_df = Ranker(config).rank(_create_dataframe(data))

        assert_frame_equal(ranked_df, _create_dataframe(expected))

    def test_ranker_when_no_on_target_score(self):
        config = {"ranking_priority_order": ["centrality", "off_target", "on_target"]}

        data = '''
            wge_percentile    centrality    on_target_score
            2    4    N/A
            1    4    N/A
            1    1    N/A
            '''
        expected = '''
            wge_percentile    centrality    on_target_score
            1    4    N/A
            2    4    N/A
            1    1    N/A
            '''

        ranked_df = Ranker(config).rank(_create_dataframe(data))

        assert_frame_equal(ranked_df, _create_dataframe(expected))

    def test_ranker_when_invalid_ranking_criteria(self):
        config = {"ranking_priority_order": ["INVALID_CRITERIA"]}

        with self.assertRaises(ValueError) as error:
            Ranker(config)

        self.assertEqual(
            str(error.exception), 'Invalid ranking criteria: the given rank criterion "INVALID_CRITERIA" is not valid'
        )

    def test_ranker_when_repeated_rank_criteria(self):
        config = {"ranking_priority_order": ["off_target", "off_target"]}

        with self.assertRaises(ValueError) as error:
            Ranker(config)

        self.assertEqual(
            str(error.exception), 'Repeated ranking criteria: the given rank criterion "off_target" is repeated'
        )


def _create_dataframe(data: str) -> pd.DataFrame:
    data_io = StringIO(data)

    return pd.read_csv(data_io, delim_whitespace=True)
