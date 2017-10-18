"""
lightspeed_sdk.utils
~~~~~~~~~~~~~~~~~~~~

Utilities used within the lightspeed_sdk.

Returns entries from configuration file as index
"""

import configparser
from pathlib import Path


def config():
    configuration = configparser.ConfigParser()
    home_path = str(Path.home())
    configuration.read(home_path + "/.lightspeed")
    if not configuration.sections():
        print("Configuration ~/.lightspeed file does not exist")
        exit()
    return configuration


config = config()
