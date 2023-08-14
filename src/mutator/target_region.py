from dataclasses import dataclass

@dataclass
class TargetRegion:
    chromosome: str
    start: int
    end: int
    id: str = ""


def parse_str_to_target_region(str) -> TargetRegion:
    data_split_by_chr = str.split(":")
    data_split_by_coords = data_split_by_chr[1].split("-")

    region = TargetRegion(
        chromosome=data_split_by_chr[0],
        start=int(data_split_by_coords[0]),
        end=int(data_split_by_coords[1]),
    )

    return region
