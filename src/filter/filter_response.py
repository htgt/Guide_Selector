from dataclasses import dataclass
from typing import List

from mutation_builder import MutationBuilder


@dataclass
class FilterResponse:
    guides_to_keep: List[MutationBuilder]
    guides_to_discard: List[MutationBuilder]
