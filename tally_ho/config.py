"""This module handles configuration files."""
import configparser
import os

CONFIG_PATH = os.path.expanduser('~/.tally')
CONFIG_FILE = os.path.expanduser('~/.tally/tally.ini')
DB_NAME = 'tally.db'

def has_config(config_file=CONFIG_FILE):

    if os.path.isfile(config_file):
        return True
    return False

def create_config(config_path=CONFIG_PATH, config_file=CONFIG_FILE, db_name=DB_NAME):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'db': db_name}

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    with open(config_file, 'w') as config_file:
        config.write(config_file)

def read_config(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.defaults()

def delete_config(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)
    os.remove(config_file)
    return config.defaults()
