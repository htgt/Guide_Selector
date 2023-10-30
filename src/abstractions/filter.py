from abc import ABC, abstractmethod
from typing import List

from filter.filter_response import FilterResponse
from mutation_builder import MutationBuilder


class Filter(ABC):
    key: str
    value_type: type

    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def apply(self, mbs: List[MutationBuilder]) -> FilterResponse:
        pass

    @staticmethod
    def get_filter_by_key(key: str):
        for filter_class in Filter.__subclasses__():
            if key == filter_class.key:
                return filter_class
