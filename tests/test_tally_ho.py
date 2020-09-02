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
        tally = th.get_tally("stuck deployments")
        self.assertEqual(tally, '')

    def test_get_category(self):
        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")

        category = th.get_category("bugs")
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

    def test_delete_category(self):
        self.create_category("bugs", "test.db")
        th = tally_ho.TallyHo("test.db")

        category = th.get_category("bugs")
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

        th.delete_category("bugs")

        category = th.get_category("bugs")
        self.assertEqual(category, '')

    def test_get_multiple_categories(self):
        categories = ["bugs", "issues"]
        for category in categories:
            self.create_category(category, "test.db")

        th = tally_ho.TallyHo("test.db")
        all_cats = th.get_categories()

        for cat in all_cats:
            self.assertIsInstance(cat, tuple)
            self.assertIn(cat.name, categories)

    def test_get_all_tallies(self):
        tally_names = ["stuck deployments", "missing button"]
        self.create_category("bugs", "test.db")
        self.create_category("issues", "test.db")
        
        th = tally_ho.TallyHo("test.db")
        th.create_tally("bugs", "stuck deployments")
        th.create_tally("issues", "missing button")

        tallies = th.get_tallies()

        for tally in tallies:
            self.assertIsInstance(tally, tuple)
            self.assertIn(tally.name, tally_names)
            self.assertEqual(len(tallies), 2)
