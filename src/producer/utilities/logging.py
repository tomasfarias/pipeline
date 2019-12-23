import logging.config

import yaml


def setup_logging(config_file: str, debug: bool = False):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f.read())

    if debug is True:
        config['root']['level'] = 'DEBUG'
    logging.config.dictConfig(config)

