from pathlib import Path

from utils.arguments_parser import InputArguments
from utils.file_system import parse_json

DEFAULT_CONFIG_FILE = Path(__file__).parent / '../../config/default_config.json'


class Config:

    def __init__(self, input_args: InputArguments):
        self.args = input_args.arguments
        self.config_dict = prepare_config(self.args['conf'])
        self.command = input_args.command


def prepare_config(config_file: str) -> dict:
    default_config = parse_json(str(DEFAULT_CONFIG_FILE))
    if config_file:
        config = parse_json(config_file)
        for field in default_config.keys():
            config.setdefault(field, default_config[field])
    else:
        config = default_config
    return config
