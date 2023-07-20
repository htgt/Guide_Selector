from os import path
import csv
from typing import List
from pathlib import Path
from mutator.runner import Runner
from td_utils.src.utils.vcf_utils import write_to_vcf, Variants

# copied from targeton-designer- need to make a shared repo
def check_file_exists(file):
    if not path.exists(file):
        raise FileNotFoundError(f'Unable to find file: {file}')


def read_csv_to_list_dict(csv_path, delimiter=',') -> List[dict]:
    check_file_exists(csv_path)

    data = []
    with open(csv_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        for row in reader:
            data.append(row)

    return data


def write_dict_list_to_csv(file_name, dict_list, headers=None, delimiter=',') -> None:
    if not headers:
        headers = list(dict_list[0].keys())

    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, delimiter=delimiter, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dict_list)
        
def write_mutator_to_vcf(file_path:str, runner:Runner) -> str:  
    variants = transform_runner_to_variants(runner)      
    file_path = Path(file_path)
    file_path.with_suffix(".vcf")
    # mutation to vcf format.
    write_to_vcf(file_path, variants)
    return file_path

def transform_runner_to_variants(runner:Runner) -> Variants:
    variants = []
    chrom = runner.mutation_builder[0].guide
    sgrna_number = 1
    variants = Variants(chrom, sgrna_number)
    
    for mb in runner.mutation_builder:
        for codon in mb.codons:
            if codon.is_permitted:
                variants.append(
                    mb.guide.chromosome,
                    codon.third.window_position,
                    ID = mb.guide.id,
                    REF = codon.third.base,
                    ALT = codon.editted.third.base, 
                    INFO = {"SGRNA":mb.guide.id}
                )
    return variants