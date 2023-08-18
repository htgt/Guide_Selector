import re
from dataclasses import dataclass
from utils.exceptions import ParseStringToTargetRegionError


@dataclass
class TargetRegion:
    chromosome: str
    start: int
    end: int
    id: str = ""


## Input string format is "chr1:100-150"
def parse_string_to_target_region(region_string: str) -> TargetRegion:
    CHROMOSOME_PATTERN = r'chr(.{1,2})'

    if ":" not in region_string:
        raise ParseStringToTargetRegionError("Chromosome and Region should be separated by ':'")

    data_split_by_chromosome = region_string.split(":")
    chromosome = re.search(CHROMOSOME_PATTERN, data_split_by_chromosome[0])

    if "-" not in data_split_by_chromosome[1]:
        raise ParseStringToTargetRegionError("Start and end coordinates should be separated by '-'")

    data_split_by_coords = data_split_by_chromosome[1].split("-")

    region = TargetRegion(
        chromosome=chromosome.group(1),
        start=int(data_split_by_coords[0]),
        end=int(data_split_by_coords[1]),
    )

    return region
