from typing import List

import gffutils

from adaptors.parsers.parse_wge_gff import read_wge_gff_to_guide_sequences
from mutator.guide import GuideSequence
from utils.file_system import read_csv_to_list_dict, write_dict_list_to_csv
from utils.get_data.wge import get_data_from_wge_by_coords
from mutator.target_region import parse_string_to_target_region, TargetRegion
from utils.exceptions import GetDataFromWGEError, NoTargetRegionDataError


def get_target_regions(region: str = None, region_file: str = None) -> List[TargetRegion]:
    region_strings = parse_regions_data(region, region_file)
    regions = parse_dicts_to_target_regions(region_strings)

    return regions


def parse_regions_data(region: str = None, region_file: str = None) -> List[str]:
    if region:
        return [{'region': region, 'id': region}]
    else:
        if region_file:
            return read_csv_to_list_dict(region_file, delimiter='\t')
        else:
            raise NoTargetRegionDataError('No input data for Target Regions')


def parse_dicts_to_target_regions(data: List[dict]) -> List[TargetRegion]:
    target_regions = []

    for line in data:
        region = parse_string_to_target_region(line["region"])
        region.id = line["id"] if "id" in line else "ID"
        target_regions.append(region)

    return target_regions


def get_guides_data(regions: List[TargetRegion], request_options: dict) -> List[GuideSequence]:
    guide_sequences_for_all_regions = []

    for region in regions:
        print(f'Retrieve data for Target Region {region.id} {region.__repr__()}')

        try:
            guide_sequences_for_region = retrieve_guides_for_region(region, request_options)
            guide_sequences_for_all_regions.extend(guide_sequences_for_region)

        except GetDataFromWGEError:
            pass

    return guide_sequences_for_all_regions


def retrieve_guides_for_region(region: TargetRegion, request_options: dict) -> List[GuideSequence]:
    gff_data = get_data_from_wge_by_coords(
        chromosome=region.chromosome,
        start=region.start,
        end=region.end,
        species_id=request_options['species_id'],
        assembly=request_options['assembly'],
    )

    try:
        guide_sequences = read_wge_gff_to_guide_sequences(gff_data)

        for guide in guide_sequences:
            guide.target_region_id = region.id

        return guide_sequences

    except gffutils.exceptions.EmptyInputError:
        raise GetDataFromWGEError(f'No guides from WGE for given region: {region.id}')
