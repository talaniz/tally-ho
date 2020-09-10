#!/usr/bin/env python

"""Tests for processing the cli."""
import os
import unittest

from tally_ho import cmd, tally_ho


class TestCategoryCLICmds(unittest.TestCase):

    def tearDown(self):
        os.remove('test.db')

    def test_cli_creates_category(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command(
            "category", "create", None, "bugs", None, th)
        category = cmd.process_cli_cmds(create_cat_cmd)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

    def test_cli_gets_all_categories(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_bugs = cmd.Command("category", "create", None, "bugs", None, th)
        category = cmd.process_cli_cmds(create_cat_bugs)
        

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

        
        get_cat_cmd = cmd.Command("category", None, None, None, None, th)
        cat_list = cmd.process_cli_cmds(get_cat_cmd)
        first_cat = cat_list[0]

        self.assertEqual(len(cat_list), 1)
        self.assertEqual(first_cat.name, "bugs")

        create_cat_issues = cmd.Command("category", "create", None, "issues", None, th)
        category = cmd.process_cli_cmds(create_cat_issues)

        self.assertEqual(category.id, 2)
        self.assertEqual(category.name, "issues")

        get_cat_cmd = cmd.Command("category", None, None, None, None, th)
        cat_list = cmd.process_cli_cmds(get_cat_cmd)
        second_cat = cat_list[1]

        self.assertEqual(len(cat_list), 2)
        self.assertEqual(second_cat.name, "issues")

    def test_cli_deletes_category(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command("category", "create", None, "bugs", None, th)
        category = cmd.process_cli_cmds(create_cat_cmd)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

        delete_cat_cmd = cmd.Command("category", "delete", None, "bugs", None, th)
        cat_list = cmd.process_cli_cmds(delete_cat_cmd)

        self.assertEqual(len(cat_list), 0)


class TestTallyCLICmds(unittest.TestCase):

    def tearDown(self):
        os.remove('test.db')

    def test_cli_creates_tally(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command("category", "create", None, "bugs", None, th)
        category = cmd.process_cli_cmds(create_cat_cmd)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "bugs")

        create_tally_cmd = cmd.Command("tally", "create", "stuck deployments", "bugs", None, th)
        tally = cmd.process_cli_cmds(create_tally_cmd)

        self.assertEqual(tally.id, 1)
        self.assertEqual(tally.name, "stuck deployments")
        self.assertEqual(tally.category, category.id)
        self.assertEqual(tally.count, 1)

    def test_cli_gets_single_tally(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command("category", "create", None, "bugs", None, th)
        cmd.process_cli_cmds(create_cat_cmd)

        create_tally_cmd = cmd.Command(
            "tally", "create", "stuck deployments", "bugs", None, th)
        tally = cmd.process_cli_cmds(create_tally_cmd)

        get_tally_cmd = cmd.Command("tally", "get", "stuck deployments", "bugs", None, th)
        tally_result = cmd.process_cli_cmds(get_tally_cmd)

        self.assertEqual(tally_result.id, tally.id)
        self.assertEqual(tally_result.name, tally.name)
        self.assertEqual(tally_result.category, tally.category)
        self.assertEqual(tally_result.count, tally.count)

    def test_cli_gets_all_tallies(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command(
            "category", "create", None, "bugs", None, th)
        cmd.process_cli_cmds(create_cat_cmd)

        create_tally_cmd = cmd.Command(
            "tally", "create", "stuck deployments", "bugs", None, th)
        cmd.process_cli_cmds(create_tally_cmd)


        create_tally2_cmd = cmd.Command(
            "tally", "create", "old database", "bugs", None, th)
        cmd.process_cli_cmds(create_tally2_cmd)
        get_tallies_cmd = cmd.Command(
            "tally", "list", None, None, None, th)
        tally2_result = cmd.process_cli_cmds(get_tallies_cmd)

        self.assertEqual(len(tally2_result), 2)

    def test_cli_deletes_tally(self):
        th = tally_ho.TallyHo('test.db')
        create_cat_cmd = cmd.Command(
            "category", "create", None, "bugs", None, th)
        cmd.process_cli_cmds(create_cat_cmd)

        create_tally_cmd = cmd.Command(
            "tally", "create", "stuck deployments", "bugs", None, th)
        cmd.process_cli_cmds(create_tally_cmd)

        tallies = th.get_tallies()
        self.assertEqual(len(tallies), 1)

        delete_tally_cmd = cmd.Command("tally", "delete", "stuck deployments", "bugs", None, th)
        cmd.process_cli_cmds(delete_tally_cmd)

        tallies = th.get_tallies()
        self.assertEqual(len(tallies), 0)
