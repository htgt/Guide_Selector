from os import path
import csv
import json
from typing import List

import pandas as pd
import pyranges as pr

from utils.exceptions import FileFormatError
from mutator.mutation_builder import MutationBuilder


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


def write_json_failed_guides(file_path: str, failed_mutations: List[MutationBuilder]) -> None:
    with open(file_path, 'w') as json_file:
        json.dump(failed_mutations, json_file, default=lambda x: x.__dict__, indent=4)


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
