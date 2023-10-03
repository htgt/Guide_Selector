from dataclasses import dataclass
from typing import List

from mutation_builder import MutationBuilder


@dataclass
class FilterResponse:
    filtered: List[MutationBuilder]
    not_filtered: List[MutationBuilder]
