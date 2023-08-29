def add_chr_prefix(chromosome: str) -> str:
    if not chromosome.startswith('chr'):
        return 'chr' + chromosome
    return chromosome


def remove_chr_prefix(chromosome: str) -> str:
    if chromosome.startswith('chr'):
        return chromosome[3:]
    return chromosome
