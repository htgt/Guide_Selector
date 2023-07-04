from os import path
import csv
from typing import List
from mutator.runner import Runner


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


def write_dict_list_to_csv(file_name, dict_list, headers=None, delimiter=','):
    if not headers:
        headers = list(dict_list[0].keys())

    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, delimiter=delimiter, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dict_list)
