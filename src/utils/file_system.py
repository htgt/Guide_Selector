from os import path
import csv
import json
from typing import List
from pathlib import Path
from mutator.runner import Runner
from td_utils.src.utils.vcf_utils import write_to_vcf

from utils.exceptions import FileFormatError


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


def write_mutator_to_vcf(file_path: str, runner: Runner) -> str:
    variants = runner.to_variants()
    file_path = Path(file_path)
    file_path.with_suffix(".vcf")
    # mutation to vcf format.
    write_to_vcf(file_path, variants)
    return str(file_path)


def parse_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        try:
            result = json.load(file)
        except Exception as err:
            raise FileFormatError

    return result
