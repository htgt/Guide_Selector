from typing import List

import gffutils

from mutator.guide import GuideSequence


def read_wge_gff_to_guide_sequences(gff_data: dict) -> List[GuideSequence]:
    db = gffutils.create_db(data=gff_data, dbfn=':memory:', from_string=True)
    guide_sequences = []

    for feature in db.features_of_type('Crispr'):
        print(feature.attributes)
        guide_sequences.append(GuideSequence(
            chromosome=feature.seqid,
            start=int(feature.start),
            end=int(feature.end),
            guide_id=feature.attributes['Name'][0],
            is_positive_strand=(feature.strand == '+'),
        ))

    return guide_sequences
