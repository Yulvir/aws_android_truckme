"""
Created on Aug 10, 2017

@author: Lab Cave
"""

import os
import yaml
import logging.config


def _setup_logging(default_yaml='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    :param default_yaml: File with the configuration for the logger
    :param default_level: INFO, WARN, ERROR etc,
    :param env_key: To setup path to yaml file as system variable
    :return: nothing
    """

    path = f'{os.path.dirname(os.path.abspath(__file__))}/{default_yaml}'
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_logger(name):

    logger = logging.getLogger(name)
    _setup_logging()
    return logger
