import unittest

from ranker.rank_criteria import TargetRegionId, CentralityRankCriteria, OffTargetRankCriteria, OnTargetRankCriteria  # NOQA
from ranker.rank_criteria_validator import RankCriteriaValidator


class TestRankCriteriaValidator(unittest.TestCase):
    def test_validate_ranking_criteria(self):
        config = {"ranking_priority_order": ["off_target", "centrality", "on_target"]}

        result = RankCriteriaValidator(config).validated_criteria()

        self.assertEqual(result, [TargetRegionId, OffTargetRankCriteria, CentralityRankCriteria, OnTargetRankCriteria])

    def test_validate_ranking_criteria_when_no_config(self):
        config = {}

        result = RankCriteriaValidator(config).validated_criteria()

        self.assertEqual(result, [TargetRegionId])

    def test_validate_ranking_criteria_when_invalid_ranking_criterion(self):
        config = {"ranking_priority_order": ["INVALID_CRITERIA"]}

        with self.assertRaises(ValueError) as error:
            RankCriteriaValidator(config).validated_criteria()

        self.assertEqual(
            str(error.exception), 'Invalid ranking criteria: the given rank criterion "INVALID_CRITERIA" is not valid'
        )

    def test_validate_ranking_criteria_when_repeated_rank_criterion(self):
        config = {"ranking_priority_order": ["off_target", "off_target"]}

        with self.assertRaises(ValueError) as error:
            RankCriteriaValidator(config).validated_criteria()

        self.assertEqual(
            str(error.exception), 'Repeated ranking criteria: the given rank criterion "off_target" is repeated'
        )
