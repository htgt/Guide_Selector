from dataclasses import dataclass
from typing import List

from mutation_builder import MutationBuilder


@dataclass
class GuideDiscarded:
    mutation_builder: MutationBuilder
    filter_applied: str


@dataclass
class FilterResponse:
    guides_to_keep: List[MutationBuilder]
    guides_to_discard: List[GuideDiscarded]
