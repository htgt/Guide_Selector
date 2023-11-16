from abc import ABC


class RankCriteria(ABC):
    name: str
    ascending: bool
    column: str

    @staticmethod
    def get_criterion_by_name(name: str):
        for rank_criteria_class in RankCriteria.__subclasses__():
            if name == rank_criteria_class.name:
                return rank_criteria_class

class TargetRegionId(RankCriteria):
    name: str = 'target_region_id'
    is_ascending: bool = True
    column: str = 'target_region_id'


class OffTargetRankCriteria(RankCriteria):
    name: str = 'off_target'
    is_ascending: bool = True
    column: str = 'wge_percentile'


class CentralityRankCriteria(RankCriteria):
    name: str = 'centrality'
    is_ascending: bool = False
    column: str = 'centrality'


class OnTargetRankCriteria(RankCriteria):
    name: str = 'on_target'
    is_ascending: bool = False
    column: str = 'on_target_score'
