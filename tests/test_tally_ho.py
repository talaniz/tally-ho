#!/usr/bin/env python

"""Tests for `tally_ho` package."""
import os
import sqlite3
import unittest

from tally_ho import tally_ho
from tally_ho.exceptions import DuplicateCategoryException, DuplicateTallyException


class TestTally_ho(unittest.TestCase):
    """Tests for `tally_ho` package."""

    def tearDown(self):
        os.remove('test.db')

    def create_category(self, category, db_name):
        th = tally_ho.TallyHo(db_name)
        return th.create_category(category)

    def create_tally(self, category, name, db_name):
        th = tally_ho.TallyHo(db_name)
        return th.create_tally(category, name)

    def test_create_category(self):
        """Create a category"""
        category = self.create_category("issues", "test.db")

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, 'issues')

    def test_create_tally_item(self):
        """Creates a tally item under a category"""

        self.create_category("bugs", "test.db")
        tally = self.create_tally("bugs", "stuck deployments", "test.db")

        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, 'stuck deployments')
        self.assertEqual(tally.count, 1)

    def test_get_tally(self):
        self.create_category("bugs", "test.db")
        self.create_tally("bugs", "stuck deployments", "test.db")

        th = tally_ho.TallyHo("test.db")
        tally = th.get_tally("stuck deployments", "bugs")
        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, 1)
        self.assertEqual(tally.count, 1)

    def test_update_tally(self):
        self.create_category("bugs", "test.db")
        self.create_tally("bugs", "stuck deployments", "test.db")

        th = tally_ho.TallyHo("test.db")
        tally = th.get_tally("stuck deployments", "bugs")
        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, 1)
        self.assertEqual(tally.count, 1)

        tally = th.update_tally("stuck deployments", "bugs", 1)
        self.assertEqual(tally.count, 2)

        tally = th.update_tally("stuck deployments", "bugs", -2)
        self.assertEqual(tally.count, 0)

    def test_delete_tally(self):
        self.create_category("bugs", "test.db")
        self.create_tally("bugs", "stuck deployments", "test.db")


        th = tally_ho.TallyHo("test.db")
        th.delete_tally("bugs", "stuck deployments")
        tally = th.get_tally("stuck deployments", "bugs")
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
        # TODO: Make this more simple
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

    def test_raises_duplicate_category_exception(self):
        self.create_category("bugs", "test.db")

        with self.assertRaises(DuplicateCategoryException):
            self.create_category("bugs", "test.db")

    def test_raises_duplicate_tally_exception(self):
        c1 = self.create_category("bugs", "test.db")
        c2 = self.create_category("issues", "test.db")

        self.assertEqual(c1.id, 1)
        self.assertEqual(c1.name, "bugs")
        
        self.assertEqual(c2.id, 2)
        self.assertEqual(c2.name, "issues")
        
        t1 = self.create_tally("bugs", "stuck deployments", "test.db")
        t2 = self.create_tally("issues", "stuck deployments", "test.db")

        self.assertEqual(t1.name, "stuck deployments")
        self.assertEqual(t1.count, 1)
        self.assertEqual(t1.category, 1)

        self.assertEqual(t2.name, "stuck deployments")
        self.assertEqual(t2.count, 1)
        self.assertEqual(t2.category, 2)

        with self.assertRaises(DuplicateTallyException):
            self.create_tally("issues", "stuck deployments", "test.db")
