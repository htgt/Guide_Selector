from pathlib import Path

from utils.arguments_parser import InputArguments
from utils.file_system import parse_json

DEFAULT_CONFIG_FILE = Path(__file__).parent / '../../config/default_config.json'


class Config:
    def __init__(self, input_args: InputArguments):
        args = input_args.arguments
        conf = prepare_config(args.get('conf'))

        self.command = input_args.command

        self.output_dir = args.get('out_dir') or conf.get('input_args', {}).get('out_dir') or './output'
        self.on_target = args.get('on_target') or conf.get('input_args', {}).get('on_target') or ''
        self.region = args.get('region') or conf.get('input_args', {}).get('region') or ''
        self.region_file = args.get('region_file') or conf.get('input_args', {}).get('region_file') or ''
        self.gtf = args.get('gtf') or conf.get('input_args', {}).get('gtf') or ''
        self.tsv = args.get('tsv') or conf.get('input_args', {}).get('tsv') or ''

        self.edit_rules = conf['edit_rules']
        self.wge_species_id = conf['wge_species_id']
        self.assembly = conf['assembly']
        self.window_length = conf['window_length']
        self.filters = conf.get('filters', {})
        self.ranking_priority_order = conf.get('ranking_priority_order', [])

        self._check_configuration()

    def _check_configuration(self):
        if self.command == 'retrieve':
            self._require_region()
        if self.command == 'mutator':
            self._require_gtf()
            self._require_tsv()
        if self.command == 'guide_selector':
            self._require_region()
            self._require_gtf()

    def _require_region(self):
        if not self.region and not self.region_file:
            raise ValueError(f'"region" or "region_file" is required to run {self.command}')

    def _require_gtf(self):
        if not self.gtf:
            raise ValueError(f'"gtf" is required to run {self.command}')

    def _require_tsv(self):
        if not self.tsv:
            raise ValueError(f'"tsv" is required to run {self.command}')

    def to_dict(self):
        return self.__dict__


def prepare_config(config_file: str) -> dict:
    default_config = parse_json(str(DEFAULT_CONFIG_FILE))
    if config_file:
        config = parse_json(config_file)
        for field in default_config.keys():
            config.setdefault(field, default_config[field])
    else:
        config = default_config
    return config
