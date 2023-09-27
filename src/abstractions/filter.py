from abc import ABC, abstractmethod
from typing import List, Optional, Any
import inspect

from mutation_builder import MutationBuilder
import filter


class Filter(ABC):

    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def apply(self, mbs: List[MutationBuilder]) -> List[MutationBuilder]:
        pass

    @classmethod
    def get_filter_implementation_names(cls):
        return [cls.__name__ for cls in cls.__subclasses__()]
