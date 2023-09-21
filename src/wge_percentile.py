from typing import Optional


def calculate_wge_percentile(off_target: Optional[dict]) -> Optional[int]:
    if off_target is None:
        return None

    # Wge off-target count distribution are taken from:
    # https://wge.stemcell.sanger.ac.uk/crispr_help#ot_distributions
    off_target_count_distributions = [
        {10: 1, 25: 1, 50: 1},
        {10: 0, 25: 0, 50: 0},
        {10: 0, 25: 0, 50: 1},
        {10: 4, 25: 9, 50: 17},
        {10: 71, 25: 119, 50: 195},
    ]

    percentiles = [
        _find_percentile(off_target[number_mismatches], distribution) for number_mismatches, distribution in
        enumerate(off_target_count_distributions)
    ]

    return max(percentiles)


def _find_percentile(count: int, count_distribution: dict) -> int:
    for percentile in sorted(count_distribution.keys()):
        if count <= count_distribution[percentile]:
            return percentile

    return 100
