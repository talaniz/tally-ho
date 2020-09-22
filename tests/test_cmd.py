#!/usr/bin/env python

"""Tests for processing the cli."""
import os
import unittest

from tally_ho import cmd, tally_ho




class TestCLICmds(unittest.TestCase):

    def setUp(self):
        self.th = tally_ho.TallyHo('test.db')

    def tearDown(self):
        os.remove('test.db')

    def create_category(self, name):
        """Create a category."""
        create_cat_cmd = cmd.Command(
            "category", "create", None, name, None, self.th)
        category = cmd.process_cli_cmds(create_cat_cmd)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, name)
        

    def test_cli_gets_all_categories(self):
        self.create_category("bugs")

        get_cat_cmd = cmd.Command("category", None, None, None, None, self.th)
        cat_list = cmd.process_cli_cmds(get_cat_cmd)
        first_cat = cat_list[0]

        self.assertEqual(len(cat_list), 1)
        self.assertEqual(first_cat.name, "bugs")

        create_cat_issues = cmd.Command("category",
                                        "create",
                                        None,
                                        "issues",
                                        None,
                                        self.th
                                        )
        category = cmd.process_cli_cmds(create_cat_issues)

        self.assertEqual(category.id, 2)
        self.assertEqual(category.name, "issues")

        get_cat_cmd = cmd.Command("category", None, None, None, None, self.th)
        cat_list = cmd.process_cli_cmds(get_cat_cmd)
        second_cat = cat_list[1]

        self.assertEqual(len(cat_list), 2)
        self.assertEqual(second_cat.name, "issues")

    def test_cli_deletes_category(self):
        self.create_category("bugs")
        delete_cat_cmd = cmd.Command("category",
                                     "delete",
                                     None,
                                     "bugs",
                                     None,
                                     self.th
                                     )
        cat_list = cmd.process_cli_cmds(delete_cat_cmd)

        self.assertEqual(len(cat_list), 0)

    def test_cli_creates_tally(self):
        create_cat_cmd = cmd.Command("category",
                                     "create",
                                     None,
                                     "bugs",
                                     None,
                                     self.th
                                     )
        category = cmd.process_cli_cmds(create_cat_cmd)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

        create_tally_cmd = cmd.Command("tally",
                                       "create",
                                       "stuck deployments",
                                       "bugs",
                                       None,
                                       self.th
                                       )
        tally = cmd.process_cli_cmds(create_tally_cmd)

        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, category.id)
        self.assertEqual(tally.count, 1)

    def test_cli_gets_single_tally(self):
        self.create_category("bugs")

        create_tally_cmd = cmd.Command(
            "tally", "create", "stuck deployments", "bugs", None, self.th)
        tally = cmd.process_cli_cmds(create_tally_cmd)

        get_tally_cmd = cmd.Command("tally",
                                    "get",
                                    "stuck deployments",
                                    "bugs",
                                    None,
                                    self.th
                                    )
        tally_result = cmd.process_cli_cmds(get_tally_cmd)

        self.assertEqual(tally_result.id, tally.id)
        self.assertEqual(tally_result.name, tally.name)
        self.assertEqual(tally_result.category, tally.category)
        self.assertEqual(tally_result.count, tally.count)

    def test_cli_gets_all_tallies(self):
        self.create_category("bugs")

        create_tally_cmd = cmd.Command(
            "tally", "create", "stuck deployments", "bugs", None, self.th)
        cmd.process_cli_cmds(create_tally_cmd)

        create_tally2_cmd = cmd.Command(
            "tally", "create", "old database", "bugs", None, self.th)
        cmd.process_cli_cmds(create_tally2_cmd)
        get_tallies_cmd = cmd.Command(
            "tally", "list", None, None, None, self.th)
        tally2_result = cmd.process_cli_cmds(get_tallies_cmd)

        self.assertEqual(len(tally2_result), 2)

    def test_cli_deletes_tally(self):
        self.create_category("bugs")

        create_tally_cmd = cmd.Command(
            "tally", "create", "stuck deployments", "bugs", None, self.th)
        cmd.process_cli_cmds(create_tally_cmd)

        tallies = self.th.get_tallies()
        self.assertEqual(len(tallies), 1)

        delete_tally_cmd = cmd.Command("tally",
                                       "delete",
                                       "stuck deployments",
                                       "bugs",
                                       None,
                                       self.th
                                       )
        cmd.process_cli_cmds(delete_tally_cmd)

        tallies = self.th.get_tallies()
        self.assertEqual(len(tallies), 0)

    def test_create_cat_fmt_ouput(self):
        create_cat_cmd = cmd.Command("category",
                                     "create",
                                     None,
                                     "bugs",
                                     None,
                                     self.th
                                     )
        category = cmd.process_cli_cmds(create_cat_cmd)
        category = cmd.fmt_output(category)

        self.assertIsInstance(category, list)
        self.assertEqual(len(category), 1)
        self.assertEqual(category[0][0], 1)
        self.assertEqual(category[0][1], "bugs")
