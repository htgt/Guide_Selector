from typing import List

import gffutils

from abstractions.command import Command
from abstractions.reader import Reader
from abstractions.writer import Writer
from retriever.retriever_reader import RetrieverReader
from retriever.retriever_writer import RetrieverWriter
from adaptors.parsers.parse_wge_gff import read_wge_gff_to_guide_sequences
from guide import GuideSequence
from target_region import TargetRegion
from utils.get_data.wge import get_data_from_wge_by_coords
from utils.exceptions import GetDataFromWGEError


class Retriever(Command, Reader, Writer):

    def __init__(self, config: dict):
        self._target_regions = None
        self.guide_sequences = None
        self.config = config

    def read_inputs(self, args: dict):
        reader = RetrieverReader().read_inputs(args)

        self._target_regions = reader.target_regions

    def run(self):
        request_options = {
            'species_id': self.config['species_id'],
            'assembly': self.config['assembly'],
        }
        self.guide_sequences = _get_guides_data(self._target_regions, request_options)

    def write_outputs(self, output_dir: str):
        RetrieverWriter(self.guide_sequences).write_outputs(output_dir)


def _get_guides_data(regions: List[TargetRegion], request_options: dict) -> List[GuideSequence]:
    guide_sequences_for_all_regions = []

    for region in regions:
        print(f'Retrieve data for Target Region {region.id} {region.__repr__()}')

        try:
            guide_sequences_for_region = _retrieve_guides_for_region(region, request_options)
            guide_sequences_for_all_regions.extend(guide_sequences_for_region)

        except GetDataFromWGEError:
            pass

    return guide_sequences_for_all_regions


def _retrieve_guides_for_region(region: TargetRegion, request_options: dict) -> List[GuideSequence]:
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
