"""Module to test config file operations."""
import configparser
import os
import unittest

from tally_ho.config import ConfigHandler


class TestConfigHandler(unittest.TestCase):

    def setUp(self):
        self.cfg_path = '/tmp'
        self.cfg_file = os.path.join(self.cfg_path, 'tally.ini')
        self.cfgh = ConfigHandler(self.cfg_path, self.cfg_file)

    def tearDown(self):
        if os.path.exists(self.cfg_file):
            os.remove(self.cfg_file)

    def test_can_create_config(self):
        result = self.cfgh.has_config()
        self.assertEqual(result, False)

        self.cfgh.create_config()
        result = self.cfgh.has_config()

        self.assertEqual(result, True)
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(self.cfg_file)
        db = cfg_parser.get('DEFAULT', 'db')
        self.assertEqual(db, 'tally.db')

    def test_can_read_config(self):
        result = self.cfgh.has_config()
        self.assertEqual(result, False)

        self.cfgh.create_config()
        result = self.cfgh.has_config()

        settings = self.cfgh.read_config()

        self.assertEqual(settings['db'], 'tally.db')

    def test_can_delete_config(self):
        result = self.cfgh.has_config()
        self.assertEqual(result, False)

        self.cfgh.create_config()
        result = self.cfgh.has_config()

        self.cfgh.delete_config()

        result = self.cfgh.has_config()
        self.assertEqual(result, False)

    def test_can_load_config(self):
        self.assertEqual(self.cfgh.db, '')

        self.cfgh.load_config()

        self.assertEqual(self.cfgh.db, 'tally.db')
