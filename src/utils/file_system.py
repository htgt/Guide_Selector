import csv
import json
from os import path
from typing import List

import pandas as pd
import pyranges as pr
from tdutils.utils.vcf_utils import Variants, write_to_vcf

from mutation_builder import MutationBuilder
from utils.exceptions import FileFormatError

# copied from targeton-designer- need to make a shared repo


def check_file_exists(file):
    if not path.exists(file):
        raise FileNotFoundError(f'Unable to find file: {file}')


def read_tsv_to_list_dict(csv_path) -> List[dict]:
    check_file_exists(csv_path)

    data = []
    with open(csv_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')
        for row in reader:
            data.append(row)

    return data


def write_list_dict_in_tsv(file_name: str, dict_list: List[dict], headers=None) -> None:
    if not headers:
        headers = list(dict_list[0].keys())

    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, delimiter='\t', fieldnames=headers)
        writer.writeheader()
        writer.writerows(dict_list)


def write_json_failed_guides(file_path: str, failed_mutations: List[MutationBuilder]) -> None:
    with open(file_path, 'w') as json_file:
        json.dump(failed_mutations, json_file, default=lambda x: x.__dict__, indent=4)


def write_variants_to_vcf(file_path: str, variants: Variants):
    write_to_vcf(variants, file_path)


def parse_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        try:
            result = json.load(file)
        except Exception as err:
            raise FileFormatError

    return result


def read_gtf_to_df(gtf: str) -> pd.DataFrame:
    gtf_df = pr.read_gtf(gtf, as_df=True)
    gtf_df['Start'] += 1  # pyranges uses 0-based coords
    return gtf_df
