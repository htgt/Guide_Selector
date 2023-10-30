from typing import List
import pandas as pd

from abstractions.command import Command

class Ranker(Command):
    def __init__(self, config: dict, mutations: pd.DataFrame) -> None:
        self._config = self._get_ranking_config(config)
        self._dataframe = mutations

    def run(self):
        self._sort_dataframe(self._dataframe)

    def _get_ranking_config(self, config: dict) -> List:
        return config["ranking"]

    def _sort_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        sorted_df = df.sort_values(by=self._column_list, ascending=self._column_list_orders)

        print(sorted_df)

    @property
    def _column_list(self):
        return list(self._config.keys())

    @property
    def _column_list_orders(self):
        return list(self._config.values())



