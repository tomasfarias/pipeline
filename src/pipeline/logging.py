import logging.config

import yaml

with open('src/pipeline/logging.yml', 'r') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)


def get_logger(name: str, debug: bool = False):
    import logging

    logger = logging.getLogger(name)
    if debug is True:
        logger.setLevel(logging.DEBUG)

    return logger
