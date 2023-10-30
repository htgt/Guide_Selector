from typing import List

from abstractions.command import Command

class Ranker(Command):
    def __init__(self, config: dict, mutations) -> None:
        self._order = self._get_ranking_order(config)
        self._dataframe = mutations

    def _get_ranking_order(self, config: dict) -> List:
        return []

    def run(self):
        pass