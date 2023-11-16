from typing import List

import gffutils

from abstractions.command import Command
from abstractions.reader import Reader
from abstractions.writer import Writer
from adaptors.parsers.parse_wge_gff import read_wge_gff_to_guide_sequences
from guide import GuideSequence
from retriever.retriever_reader import RetrieverReader
from retriever.retriever_writer import RetrieverWriter
from target_region import TargetRegion
from utils.exceptions import GuidesNotFoundError
from utils.get_data.wge import get_data_from_wge_by_coords


class Retriever(Command, Reader, Writer):
    def __init__(self, config: dict):
        self._target_regions: List[TargetRegion] = []
        self.guide_sequences: List[GuideSequence] = []
        self.config = config

    def read_inputs(self, args: dict):
        reader = RetrieverReader().read_inputs(args)

        self._target_regions = reader.target_regions

    def run(self):
        request_options = {
            'wge_species_id': self.config['wge_species_id'],
            'assembly': self.config['assembly'],
        }
        self.guide_sequences = _get_guides_data(self._target_regions, request_options)

        if not self.guide_sequences:
            raise GuidesNotFoundError('No guides found in given regions.')

    def write_outputs(self, output_dir: str):
        RetrieverWriter(self.guide_sequences).write_outputs(output_dir)


def _get_guides_data(regions: List[TargetRegion], request_options: dict) -> List[GuideSequence]:
    guide_sequences_for_all_regions = []

    for region in regions:
        print(f'Retrieve data for Target Region {region.id} {region.__repr__()}')

        guide_sequences_for_region = _retrieve_guides_for_region(region, request_options)

        if not guide_sequences_for_region:
            print(f'No guides found in region: {region.id} {region.__repr__()}')
        guide_sequences_for_all_regions.extend(guide_sequences_for_region)

    return guide_sequences_for_all_regions


def _retrieve_guides_for_region(region: TargetRegion, request_options: dict) -> List[GuideSequence]:
    gff_data = get_data_from_wge_by_coords(
        chromosome=region.chromosome,
        start=region.start,
        end=region.end,
        species_id=request_options['wge_species_id'],
        assembly=request_options['assembly'],
    )

    guide_sequences = read_wge_gff_to_guide_sequences(gff_data)

    for guide in guide_sequences:
        guide.target_region = region

    return guide_sequences
