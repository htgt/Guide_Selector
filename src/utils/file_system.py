from os import path
import csv
from typing import List, TYPE_CHECKING
from pathlib import Path
from td_utils.src.utils.write_output_files import OutputFilesData

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
        
def write_mutator_to_vcf(file_path:str, mutation:DataFrame) -> str:
    file_path = Path(file_path)
    od = OutputFilesData(file_path.parent)
    file_path.with_suffix(".vcf")
    # mutation to vcf format.
    return od.write_output(mutation.to_dict(), file_path)