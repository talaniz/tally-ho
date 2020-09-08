#!/usr/bin/env python

"""Tests for processing the cli."""
import os
import unittest

from tally_ho import cmd, tally_ho


class TestCLI(unittest.TestCase):

    def tearDown(self):
        os.remove('test.db')

    def test_cli_creates_category(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command("category", "create", "bugs", None, th)
        category = cmd.process_cli_cmds(create_cat_cmd)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

