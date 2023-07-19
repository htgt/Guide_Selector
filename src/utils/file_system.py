from os import path
import csv
from typing import List, TYPE_CHECKING
from pathlib import Path
from mutator.runner import Runner, mutator_to_dict_list
from td_utils.src.utils.vcf_utils import write_to_vcf, Variant, Variants, REQUIRED_FIELDS, VCFHeader

if TYPE_CHECKING:
    from pandas import DataFrame

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
        
def write_mutator_to_vcf(file_path:str, runners:List[Runner]) -> str:  
    variants = transform_mutator_to_variants(runners)      
    file_path = Path(file_path)
    file_path.with_suffix(".vcf")
    # mutation to vcf format.
    write_to_vcf(file_path, variants)
    return file_path

def transform_mutator_to_variants(runners:List[Runner]) -> Variants:
    variants = []
    chrom = runners[0].guide.chromosome
    sgrna_number = 1
    
    translation_dict = {
        "CHROM":"chromosome",
        "ID":"guide_id",
        "POS":"pos",
        "REF":"ref_pos_three",
        "ALT":"alt_pos_three"
    }
    
    list_runners = mutator_to_dict_list(runners)
    for row in list_runners:
        
        variant_dict={}
        for variant_key, row_key in translation_dict.items():
            variant_dict[variant_key] = row[row_key]
        variants.append(Variant(**variant_dict))

    return Variants(variants, chrom, sgrna_number)
