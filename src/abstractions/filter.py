from abc import ABC, abstractmethod
from typing import List

from mutation_builder import MutationBuilder


class Filter(ABC):
    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def apply(self, mbs: List[MutationBuilder]) -> List[MutationBuilder]:
        pass
