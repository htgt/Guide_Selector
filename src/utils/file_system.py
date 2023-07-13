from os import path
import csv
<<<<<<< HEAD
from typing import List
import json

from utils.exceptions import FileFormatError
=======
from typing import List, TYPE_CHECKING
from pathlib import Path
from td_utils.src.utils.vcf_utils import write_to_vcf, Variant, Variants, REQUIRED_FIELDS, VCFHeader
from td_utils.src.utils.file_system import read_csv

if TYPE_CHECKING:
    from pandas import DataFrame

>>>>>>> 9b54dc7... TD_421 Trying setup the functions for exporting the vcf


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
        
def write_mutator_to_vcf(tsv_file_path:str, variants:Variants) -> str:
    tsv_file_path = Path(tsv_file_path)
    tsv_data = read_csv(tsv_file_path).as_list_dicts()
    variants = []
    for row in tsv_data:
        variants.append(row)
        
    vcf_file_path = tsv_file_path.copy()
    vcf_file_path.with_suffix(".vcf")
    
    # mutation to vcf format.
    write_to_vcf()
    return vcf_file_path

def transform_tsv_to_variants(data:List[dict], chrom:str, sgrna_num:int) -> Variant:
    variants = []
    for tsv_row in data:
        lower_case_required_fields = [field.lower() for field in REQUIRED_FIELDS]
        variant_dict={}
        for key, item in tsv_row.items():
            if key.lower() in lower_case_required_fields:
                field = REQUIRED_FIELDS[lower_case_required_fields.index(key.lower())]
                variant_dict[field] = item
        variants.append(Variant(**variant_dict))
    return Variants(variants, chrom, sgrna_num)
