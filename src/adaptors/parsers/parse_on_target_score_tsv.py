from typing import Dict

import pandas as pd

from utils.file_system import check_file_exists


def get_guides_on_target_scores(on_targets_file: str) -> Dict[int, float]:
    if on_targets_file:
        check_file_exists(on_targets_file)

        df = pd.read_csv(on_targets_file, sep='\t')

        return dict(zip(df['Guide'], df['On-target Score']))
    else:
        return {}
