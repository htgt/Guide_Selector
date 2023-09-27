from abc import ABC, abstractmethod
from typing import List, Optional, Any

from mutation_builder import MutationBuilder


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

    @classmethod
    def find_filter(cls, filter_name: str) -> Optional[Any]:
        for subclass in cls.__subclasses__():
            if subclass.__name__ == filter_name:
                return subclass
        return None
