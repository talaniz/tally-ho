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

        get_cat_cmd = cmd.Command("category", 'None', None, None, None, self.th)
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

        get_cat_cmd = cmd.Command("category", 'None', None, None, None, self.th)
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

    def test_cat_fmt_ouput(self):
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

        create_cat_cmd = cmd.Command("category",
                                     "create",
                                     None,
                                     "issues",
                                     None,
                                     self.th
                                     )
        category = cmd.process_cli_cmds(create_cat_cmd)
        category = cmd.fmt_output(category)

        self.assertIsInstance(category, list)
        self.assertEqual(len(category), 1)
        self.assertEqual(category[0][0], 2)
        self.assertEqual(category[0][1], "issues")

        get_cat_cmd = cmd.Command("category", 'None', None, None, None, self.th)
        cat_list = cmd.process_cli_cmds(get_cat_cmd)

        self.assertIsInstance(cat_list, list)
        self.assertEqual(len(cat_list), 2)
        self.assertEqual(cat_list[0][0], 1)
        self.assertEqual(cat_list[0][1], "bugs")
        self.assertEqual(cat_list[1][0], 2)
        self.assertEqual(cat_list[1][1], "issues")


    def test_tally_fmt_ouput(self):
        self.create_category("bugs")
        create_tally_cmd = cmd.Command("tally",
                                       "create",
                                       "stuck deployments",
                                       "bugs",
                                       None,
                                       self.th
                                       )
        cmd.process_cli_cmds(create_tally_cmd)
        get_tally_cmd = cmd.Command("tally",
                                    "get",
                                    "stuck deployments",
                                    "bugs",
                                    None,
                                    self.th
                                    )
        tally = cmd.process_cli_cmds(get_tally_cmd)
        tally = cmd.fmt_output(tally)

        self.assertIsInstance(tally, list)
        self.assertEqual(len(tally), 1)
        self.assertEqual(tally[0][0], 1)
        self.assertEqual(tally[0][1], "stuck deployments")
        self.assertEqual(tally[0][2], 1)
        self.assertEqual(tally[0][3], 1)

        create_tally_cmd2 = cmd.Command("tally",
                                       "create",
                                       "slow page load",
                                       "bugs",
                                       None,
                                       self.th
                                       )
        tally2 = cmd.process_cli_cmds(create_tally_cmd2)
        tally2 = cmd.fmt_output(tally2)

        self.assertIsInstance(tally2, list)
        self.assertEqual(len(tally2), 1)
        self.assertEqual(tally2[0][0], 2)
        self.assertEqual(tally2[0][1], "slow page load")
        self.assertEqual(tally2[0][2], 1)

        get_tallies_cmd = cmd.Command(
            "tally", "list", None, None, None, self.th)
        tally_list = cmd.process_cli_cmds(get_tallies_cmd)
    
        self.assertIsInstance(tally_list, list)
        self.assertEqual(len(tally_list), 2)
        self.assertEqual(tally_list[0][0], 1)
        self.assertEqual(tally_list[0][1], "stuck deployments")
        self.assertEqual(tally_list[0][2], 1)
        self.assertEqual(tally_list[1][0], 2)
        self.assertEqual(tally_list[1][1], "slow page load")
        self.assertEqual(tally_list[1][2], 1)


class TestArgHandling(unittest.TestCase):


    def setUp(self):
        self.th = tally_ho.TallyHo('test.db')
        self.create_cat_cmd = cmd.Command("category", "create", None, "bugs", None, self.th)
        self.get_cat_cmd = cmd.Command("category", 'None', None, None, None, self.th)
        self.delete_cat_cmd = cmd.Command("category", "delete", None, "bugs", None, self.th)
        self.create_tally_cmd = cmd.Command("tally", "create", "stuck deployments", "bugs", None, self.th)
        self.get_tally_cmd = cmd.Command("tally", "get", "stuck deployments", "bugs", None, self.th)
        self.get_tallies_cmd = cmd.Command("tally", "list", None, None, None, self.th)
        self.delete_tally_cmd = cmd.Command("tally", "delete", "stuck deployments", "bugs", None,self.th)

    def tearDown(self):
        os.remove('test.db')

    def test_parse_args_creates_cat_cmd(self):
        db = 'test.db'
        create_cat_args = ['category', 'create', '--category', 'bugs']
        create_cat_args2 = ['category', 'create', '--category', 'issues']
        create_cat_args3 = ['category', 'create', '--category', 'db backup']
        test_create_cat_cmd = cmd.parse_args(create_cat_args, db)

        self.assertIsInstance(test_create_cat_cmd, cmd.Command)
        self.assertIsInstance(test_create_cat_cmd.tally_ho, tally_ho.TallyHo)
        self.assertEqual(test_create_cat_cmd.item, self.create_cat_cmd.item)
        self.assertEqual(test_create_cat_cmd.action, self.create_cat_cmd.action)
        self.assertEqual(test_create_cat_cmd.category, self.create_cat_cmd.category)
        self.assertEqual(test_create_cat_cmd.quantity, self.create_cat_cmd.quantity)

        category = cmd.process_cli_cmds(test_create_cat_cmd)
        get_cat_args = ['category', '--category', 'bugs']
        test_get_cat_cmd = cmd.parse_args(get_cat_args, db)

        test_cat = cmd.process_cli_cmds(test_get_cat_cmd)[0]
        self.assertEqual(test_cat.id, category.id)
        self.assertEqual(test_cat.name, category.name)

        create_cat_cmd2 = cmd.parse_args(create_cat_args2, db)
        cmd.process_cli_cmds(create_cat_cmd2)
        get_all_cat_args = ['category']
        test_get_all_cat_cmd = cmd.parse_args(get_all_cat_args, db)
        cat_list = cmd.process_cli_cmds(test_get_all_cat_cmd)
        test_cat2 = cat_list[1]

        self.assertEqual(len(cat_list), 2)
        self.assertEqual(test_cat2.id, 2)
        self.assertEqual(test_cat2.name, 'issues')

        create_cat_cmd3 = cmd.parse_args(create_cat_args3, db)
        cmd.process_cli_cmds(create_cat_cmd3)
        cat_list2 = cmd.process_cli_cmds(test_get_all_cat_cmd)
        test_cat3 = cat_list2[2]

        self.assertEqual(len(cat_list2), 3)
        self.assertEqual(test_cat3.id, 3)