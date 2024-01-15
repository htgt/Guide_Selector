from typing import List

from abstractions.command import Command
from adaptors.parsers.parse_wge_gff import read_wge_gff_to_guide_sequences
from config.config import Config
from guide import GuideSequence
from retriever.retriever_reader import RetrieverReader
from retriever.retriever_writer import RetrieverWriter
from target_region import TargetRegion
from utils.exceptions import GuidesNotFoundError
from utils.get_data.wge import get_data_from_wge_by_coords


class Retriever(Command):
    def __init__(self, config: Config):
        super().__init__(config)
        self._target_regions: List[TargetRegion] = []
        self.guide_sequences: List[GuideSequence] = []

    def run(self):
        print('Run retrieve command with config:', self._config.to_dict())
        self._read_inputs()
        self._process()
        self._write_outputs()

    def _read_inputs(self):
        reader = RetrieverReader(self._config).read_inputs()

        self._target_regions = reader.target_regions

    def _process(self):
        request_options = {
            'wge_species_id': self._config.wge_species_id,
            'assembly': self._config.assembly
        }
        self.guide_sequences = _get_guides_data(self._target_regions, request_options)

        if not self.guide_sequences:
            raise GuidesNotFoundError('No guides found in given regions.')

    def _write_outputs(self):
        RetrieverWriter(self.guide_sequences, self._config.version_stamp).write_outputs(self._config.output_dir)


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
