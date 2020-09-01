#!/usr/bin/env python

"""Tests for `tally_ho` package."""
import os
import sqlite3
import unittest

from tally_ho import tally_ho


class TestTally_ho(unittest.TestCase):
    """Tests for `tally_ho` package."""

    def create_category(self, category, db_name):
        th = tally_ho.TallyHo(db_name)
        th.create_category(category)

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
        th = tally_ho.TallyHo("test.db")
        th.create_tally("bugs", "stuck deployments")

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

    def test_get_tally(self):
        """Increments a tally by one"""
        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")
        th.create_tally("bugs", "stuck deployments")

        tally = th.get_tally("stuck deployments")
        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, 1)
        self.assertEqual(tally.count, 1)
