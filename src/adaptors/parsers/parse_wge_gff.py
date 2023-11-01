from ast import literal_eval
from typing import List

import gffutils

from guide import GuideSequence


def read_wge_gff_to_guide_sequences(gff_data: str) -> List[GuideSequence]:
    guide_sequences = []

    try:
        db = gffutils.create_db(data=gff_data, dbfn=':memory:', from_string=True)

        for feature in db.features_of_type('Crispr'):
            guide_sequences.append(
                GuideSequence(
                    chromosome=feature.seqid,
                    start=int(feature.start),
                    end=int(feature.end),
                    guide_id=feature.attributes['Name'][0],
                    is_positive_strand=(feature.strand == '+'),
                    ot_summary=_OT_summary_to_dict(feature.attributes['OT_Summary']),
                )
            )
    except gffutils.interface.FeatureNotFoundError:
        print('FeatureNotFoundError: "Crispr" feature not found in the GFF data.')
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')

    return guide_sequences


def _OT_summary_to_dict(entry: List) -> dict:
    cleaned = str(entry).replace("'", "").replace("[", "").replace("]", "")
    return literal_eval(cleaned)
