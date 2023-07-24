from dataclasses import dataclass

from utils.exceptions import MutatorError


@dataclass
class BaseWithPosition:
    base: str
    coordinate: int
    window_position: int = 0


@dataclass
class WindowCodon:
    bases: str
    third: BaseWithPosition


class CodonEdit:
    def __init__(self, codon: str, window_pos: int) -> None:
        self._original_codon = codon.upper()
        self._window_pos = window_pos

    @property
    def original_codon(self) -> str:
        return self._original_codon

    @property
    def window_pos(self) -> int:
        return self._window_pos

    @property
    def edited_codon(self) -> str:
        base_edits = {'T': 'C', 'C': 'T', 'A': 'G', 'G': 'A'}
        new_codon = self.original_codon[:2] + base_edits[self.original_codon[2]]
        return new_codon

    def is_permitted(self, config: dict) -> bool:
        if self.original_codon in ('ATG', 'TGG', 'ATA', 'TGA'):
            return False
        try:
            if self.window_pos in config['ignore_positions']:
                return False
            if (not config['allow_codon_loss']) and self.lost_amino_acids:
                return False
        except KeyError:
            raise MutatorError('Field missing from config')
        return True

    @property
    def lost_amino_acids(self) -> list:
        edited_codon = self.edited_codon
        if edited_codon in ('ATG', 'TGG', 'ATA', 'TGA'):
            # rules don't apply
            return []
        lost_amino_acids = []
        if edited_codon[0] == 'A' or edited_codon[1] == 'T':
            if edited_codon[2] == 'A':
                lost_amino_acids.append('M')
            elif edited_codon[2] == 'G':
                lost_amino_acids.append('I')
        if (edited_codon[0] == 'T' or edited_codon[1] == 'G') and (edited_codon[2] == 'A'):
            lost_amino_acids.append('W')
        elif edited_codon[1] == 'G' and edited_codon[2] == 'G':
            lost_amino_acids.append('*')
        return lost_amino_acids
