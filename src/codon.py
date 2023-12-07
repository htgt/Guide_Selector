from utils.exceptions import MutatorError


class WindowCodon:
    def __init__(
        self,
        bases: str,
        third_base_coord: int,
        third_base_pos: int,
        is_positive_strand: bool,
    ) -> None:
        self._bases = bases.upper()
        self._third_base_coord = third_base_coord
        self._third_base_pos = third_base_pos
        self._is_positive_strand = is_positive_strand

    def __repr__(self):
        return f'bases: {self.bases} third_base_coord: {str(self.third_base_coord)}'

    @property
    def bases(self) -> str:
        return self._bases

    @property
    def third_base_coord(self) -> int:
        return self._third_base_coord

    @property
    def third_base_pos(self) -> int:
        return self._third_base_pos

    @property
    def is_positive_strand(self) -> bool:
        return self._is_positive_strand

    @property
    def edited_bases(self) -> str:
        base_edits = {'T': 'C', 'C': 'T', 'A': 'G', 'G': 'A'}
        new_codon = self.bases[:2] + base_edits[self.bases[2]]
        return new_codon

    def is_edit_permitted(self, config: dict, cds_start: int, cds_end: int) -> bool:
        if self.bases in ('ATG', 'TGG', 'ATA', 'TGA'):
            return False
        try:
            if self.third_base_pos in config['ignore_positions']:
                return False
            if (not config['allow_codon_loss']) and self.amino_acids_lost_from_edit:
                return False
            distance = config['splice_mask_distance']
        except KeyError:
            raise MutatorError('Field missing from config')

        if not (cds_start + distance) <= self.third_base_coord <= (cds_end - distance):
            return False

        return True

    @property
    def amino_acids_lost_from_edit(self) -> list:
        edited_codon = self.edited_bases
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

    @property
    def third_base_on_positive_strand(self) -> str:
        return get_third_base_on_positive_strand(self.bases, self.is_positive_strand)

    @property
    def edited_third_base_on_positive_strand(self) -> str:
        return get_third_base_on_positive_strand(self.edited_bases, self.is_positive_strand)


def get_third_base_on_positive_strand(bases: str, is_positive_strand: bool) -> str:
    complements = {'T': 'A', 'C': 'G', 'A': 'T', 'G': 'C'}

    return bases[2] if is_positive_strand else complements[bases[2]]
