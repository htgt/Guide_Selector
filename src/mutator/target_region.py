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
    REGION_PATTERN = r'(chr?){0,1}(.{1,2}):(\d+)-(\d+)'

    match = re.match(REGION_PATTERN, region_string)
    if match:
        prefix, chromosome, start, end = match.groups()
    else:
        raise ParseStringToTargetRegionError(f"Region string {region_string} doesn't match pattern chr1:100-120")

    region = TargetRegion(
        chromosome=chromosome,
        start=start,
        end=end,
    )

    return region
