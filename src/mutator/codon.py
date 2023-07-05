class CodonEdit:
    def __init__(self, codon: str) -> None:
        self._original_codon = codon.upper()

    @property
    def original_codon(self) -> str:
        return self._original_codon

    @property
    def edited_codon(self) -> str:
        base_edits = {'T': 'C', 'C': 'T', 'A': 'G', 'G': 'A'}
        new_codon = self.original_codon[:2] + base_edits[self.original_codon[2]]
        return new_codon

    @property
    def is_permitted(self) -> bool:
        if self.original_codon in ('ATG', 'TGG', 'ATA', 'TGA'):
            return False
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
