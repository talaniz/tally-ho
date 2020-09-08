#!/usr/bin/env python

"""Module for processing user based requests."""
from collections import namedtuple

from tally_ho import tally_ho

Command = namedtuple("Command", "item action name quantity tally_ho")

def execute_category_action(cmd):
    """Execute a category based method."""
    if cmd.action == "create":
        return cmd.tally_ho.create_category(cmd.name)
    elif cmd.action == None and cmd.name == None and cmd.quantity == None:
        return cmd.tally_ho.get_categories()


def process_cli_cmds(cmd):
    """Execute a category or tally method based on user input."""
    if cmd.item == "category":
        return execute_category_action(cmd)
