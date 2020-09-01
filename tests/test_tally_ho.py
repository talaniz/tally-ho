#!/usr/bin/env python

"""Tests for `tally_ho` package."""
import os
import sqlite3
import unittest

from tally_ho import tally_ho


class TestTally_ho(unittest.TestCase):
    """Tests for `tally_ho` package."""

    def create_category(self, category, db_name):
        tally = tally_ho.TallyHo()
        tally.create_category("bugs", "test.db")

    def tearDown(self):
        os.remove('test.db')

    def test_create_category(self):
        """Create a category"""
        self.create_category("bugs", "test.db")

        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT * FROM categories WHERE name='bugs'")

        records = c.fetchall()
        first_record = records[0]

        self.assertEqual(len(records), 1)
        self.assertEqual(first_record[1], 'bugs')

    def test_create_tally_item(self):
        """Creates a tally item under a category"""

        self.create_category("bugs", "test.db")
        tally = tally_ho.TallyHo()
        tally.create_tally("bugs", "stuck deployments", "test.db")

        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tally WHERE name='stuck deployments'")

        records = c.fetchall()
        first_record = records[0]
        tally_name = first_record[1]
        tally_count = first_record[2]

        self.assertEqual(len(records), 1)
        self.assertEqual(tally_name, 'stuck deployments')
        self.assertEqual(tally_count, 1)
