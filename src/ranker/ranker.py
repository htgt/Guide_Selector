from typing import List

import pandas as pd

from config.config import Config
from ranker.rank_criteria import RankCriteria
from ranker.rank_criteria_validator import RankCriteriaValidator


class Ranker:
    def __init__(self, config: Config) -> None:
        self._ranking_order: List[RankCriteria] = RankCriteriaValidator(config).validated_criteria()

    def rank(self, df: pd.DataFrame):
        criteria_in_columns = [criteria for criteria in self._ranking_order if criteria.column in df.columns]

        columns = [criteria.column for criteria in criteria_in_columns]
        ascendings = [criteria.is_ascending for criteria in criteria_in_columns]

        ranked_df = df.sort_values(by=columns, ascending=ascendings)
        ranked_df = ranked_df.reset_index(drop=True)

        return ranked_df
