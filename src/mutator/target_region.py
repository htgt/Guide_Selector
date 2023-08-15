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
def parse_str_to_target_region(str) -> TargetRegion:
    if ":" not in str:
        raise ParseStringToTargetRegionError("Chromosome should be separated by ':'")

    data_split_by_chr = str.split(":")

    chromosome_pattern = r'chr(..)'
    chromosome = re.search(chromosome_pattern, data_split_by_chr[0]).group(1)

    if "-" not in data_split_by_chr[1]:
        raise ParseStringToTargetRegionError("Start and end coordinates should be separated by '-'")

    data_split_by_coords = data_split_by_chr[1].split("-")

    region = TargetRegion(
        chromosome=chromosome,
        start=int(data_split_by_coords[0]),
        end=int(data_split_by_coords[1]),
    )

    return region
