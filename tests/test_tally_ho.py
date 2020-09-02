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
        return th.create_category(category)

    def tearDown(self):
        os.remove('test.db')

    def test_create_category(self):
        """Create a category"""
        category = self.create_category("issues", "test.db")

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, 'issues')

    def test_create_tally_item(self):
        """Creates a tally item under a category"""

        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")
        tally = th.create_tally("bugs", "stuck deployments")

        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, 'stuck deployments')
        self.assertEqual(tally.count, 1)

    def test_get_tally(self):
        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")
        th.create_tally("bugs", "stuck deployments")

        tally = th.get_tally("stuck deployments")
        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, 1)
        self.assertEqual(tally.count, 1)

    def test_update_tally(self):
        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")
        th.create_tally("bugs", "stuck deployments")

        tally = th.get_tally("stuck deployments")
        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, 1)
        self.assertEqual(tally.count, 1)

        tally = th.update_tally("stuck deployments", 1)
        self.assertEqual(tally.count, 2)

        tally = th.update_tally("stuck deployments", -2)
        self.assertEqual(tally.count, 0)

    def test_delete_tally(self):
        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")
        tally = th.create_tally("bugs", "stuck deployments")

        th.delete_tally("bugs", "stuck deployments")
        tally = th.get_tally("stuck deplloyments")
        self.assertEqual(tally, '')
