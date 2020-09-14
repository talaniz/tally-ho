"""Module to test config file operations."""
import configparser
import os
import unittest

from tally_ho.config import has_config, create_config, read_config

class TestConfigHandler(unittest.TestCase):

    def setUp(self):
        self.cfg_path = '/tmp'
        self.cfg_file = os.path.join(self.cfg_path, 'tally.ini')

    def tearDown(self):
        os.remove(self.cfg_file)

    def test_can_create_config(self):
        result = has_config(self.cfg_file)
        self.assertEqual(result, False)

        create_config(config_path=self.cfg_path, config_file=self.cfg_file)
        result = has_config(self.cfg_file)

        self.assertEqual(result, True)
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(self.cfg_file)
        db = cfg_parser.get('DEFAULT', 'db')
        self.assertEqual(db, 'tally.db')

    def test_can_read_config(self):
        result = has_config(self.cfg_file)
        self.assertEqual(result, False)

        create_config(config_path=self.cfg_path, config_file=self.cfg_file)
        result = has_config(self.cfg_file)

        settings = read_config(self.cfg_file)

        self.assertEqual(settings['db'], 'tally.db')
