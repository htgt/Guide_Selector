from pathlib import Path

from utils.file_system import parse_json

DEFAULT_CONFIG_FILE = Path(__file__).parent / '../../config/default_config.json'


def prepare_config(config_file: str) -> dict:
    default_config = parse_json(DEFAULT_CONFIG_FILE)
    if config_file:
        config = parse_json(config_file)
        for field in default_config.keys():
            config.setdefault(field, default_config[field])
    else:
        config = default_config
    return config
