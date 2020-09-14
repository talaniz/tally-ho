"""This module handles configuration files."""
import configparser
import os

CONFIG_PATH = os.path.expanduser('~/.tally')
CONFIG_FILE = os.path.expanduser('~/.tally/tally.ini')
DB_NAME = 'tally.db'

class ConfigHandler(object):
    """CRUD manager for configs."""

    def __init__(self, config_path=CONFIG_PATH, config_file=CONFIG_FILE):
        self.config_path = config_path
        self.config_file = config_file
        self.db = ''

    def has_config(self):

        if os.path.isfile(self.config_file):
            return True
        return False

    def create_config(self, db_name=DB_NAME):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'db': db_name}

        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)

        with open(self.config_file, 'w') as config_file:
            config.write(config_file)

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config.defaults()

    def delete_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        os.remove(self.config_file)
        return config.defaults()
