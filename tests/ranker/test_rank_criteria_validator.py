import unittest
from unittest.mock import Mock

from ranker.rank_criteria import CentralityRankCriteria, OffTargetRankCriteria, OnTargetRankCriteria, \
    TargetRegionIdCriteria  # NOQA
from ranker.rank_criteria_validator import RankCriteriaValidator


class TestRankCriteriaValidator(unittest.TestCase):
    def test_validate_ranking_criteria(self):
        ranking_priority_order = ["off_target", "centrality", "on_target"]

        result = RankCriteriaValidator(_config(ranking_priority_order)).validated_criteria()

        self.assertEqual(
            result, [TargetRegionIdCriteria, OffTargetRankCriteria, CentralityRankCriteria, OnTargetRankCriteria]
        )

    def test_validate_ranking_criteria_when_no_config(self):
        ranking_priority_order = []

        result = RankCriteriaValidator(_config(ranking_priority_order)).validated_criteria()

        self.assertEqual(result, [TargetRegionIdCriteria])

    def test_validate_ranking_criteria_when_invalid_ranking_criterion(self):
        ranking_priority_order = ["INVALID_CRITERIA"]

        with self.assertRaises(ValueError) as error:
            RankCriteriaValidator(_config(ranking_priority_order)).validated_criteria()

        self.assertEqual(
            str(error.exception), 'Invalid ranking criteria: the given rank criterion "INVALID_CRITERIA" is not valid'
        )

    def test_validate_ranking_criteria_when_repeated_rank_criterion(self):
        ranking_priority_order = ["off_target", "off_target"]

        with self.assertRaises(ValueError) as error:
            RankCriteriaValidator(_config(ranking_priority_order)).validated_criteria()

        self.assertEqual(
            str(error.exception), 'Repeated ranking criteria: the given rank criterion "off_target" is repeated'
        )


def _config(ranking_priority_order: list) -> Mock:
    config = Mock()
    config.ranking_priority_order = ranking_priority_order
    return config
