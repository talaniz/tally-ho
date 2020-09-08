#!/usr/bin/env python

"""Module for processing user based requests."""
from collections import namedtuple

from tally_ho import tally_ho

Command = namedtuple("Command", "item action name category quantity tally_ho")

def execute_tally_action(cmd):
    """Execute a tally based action."""
    if cmd.action == "create" and cmd.name is not None and cmd.category is not None:
        return cmd.tally_ho.create_tally(cmd.category, cmd.name)
    elif cmd.action == "get" and cmd.name is not None and cmd.category is not None:
        return cmd.tally_ho.get_tally(cmd.name, cmd.category)
    elif cmd.action == "list":
        return cmd.tally_ho.get_tallies()

def execute_category_action(cmd):
    """Execute a category based method."""
    if cmd.action == "create":
        return cmd.tally_ho.create_category(cmd.name)
    elif cmd.action == None and cmd.name == None and cmd.quantity == None:
        return cmd.tally_ho.get_categories()
    elif cmd.action == "delete" and cmd.name != None:
        return cmd.tally_ho.delete_category(cmd.name)

def process_cli_cmds(cmd):
    """Execute a category or tally method based on user input."""
    if cmd.item == "category":
        return execute_category_action(cmd)
    elif cmd.item == "tally":
        return execute_tally_action(cmd)
