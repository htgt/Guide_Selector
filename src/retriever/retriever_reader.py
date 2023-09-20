from typing import List

from abstractions.reader import Reader
from target_region import TargetRegion, parse_string_to_target_region
from utils.exceptions import NoTargetRegionDataError
from utils.file_system import read_tsv_to_list_dict


class RetrieverReader(Reader):

    def __init__(self):
        self.target_regions = None

    def read_inputs(self, args: dict, **kwargs) -> Reader:
        self.target_regions = _get_target_regions(region=args['region'], region_file=args['region_file'])
        return self


def _get_target_regions(region: str = None, region_file: str = None) -> List[TargetRegion]:
    region_strings = _get_regions_dict(region, region_file)
    regions = _parse_dicts_to_target_regions(region_strings)

    return regions


def _get_regions_dict(region: str = None, region_file: str = None) -> List[dict]:
    if region:
        return [{'region': region, 'id': region}]
    else:
        if region_file:
            return read_tsv_to_list_dict(region_file)
        else:
            raise NoTargetRegionDataError('No input data for Target Regions')


def _parse_dicts_to_target_regions(data: List[dict]) -> List[TargetRegion]:
    target_regions = []

    for line in data:
        region = parse_string_to_target_region(line["region"])
        region.id = line["id"] if "id" in line else "ID"
        target_regions.append(region)

    return target_regions
