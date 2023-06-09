from os import path
import csv
from typing import List


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