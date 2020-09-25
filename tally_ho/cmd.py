#!/usr/bin/env python

"""Module for processing user based requests."""
import argparse
from collections import namedtuple

from tally_ho import tally_ho

class Command(namedtuple("Command", ["item", "action", "tally", "category", "quantity" , "tally_ho"])):
    """A cli command."""

    # To make the conditional in `execute_tally_action` more clear
    @property
    def has_valid_params(self):
        """Return True if the cmd has the necessary args to execute."""
        if self.item == "tally":
            return self.tally is not None and self.category is not None

def execute_tally_action(cmd):
    """Execute a tally based action."""
    if cmd.action == "create" and cmd.has_valid_params:
        return cmd.tally_ho.create_tally(cmd.category, cmd.tally)
    elif cmd.action == "get" and cmd.has_valid_params:
        return cmd.tally_ho.get_tally(cmd.tally, cmd.category)
    elif cmd.action == "list":
        return cmd.tally_ho.get_tallies()
    elif cmd.action == "delete" and cmd.has_valid_params:
        return cmd.tally_ho.delete_tally(cmd.category, cmd.tally)

def execute_category_action(cmd):
    """Execute a category based method."""
    if cmd.action == "create":
        return cmd.tally_ho.create_category(cmd.category) 
    elif cmd.action == 'None':
        return cmd.tally_ho.get_categories()
    elif cmd.action == "delete" and cmd.category != None:
        return cmd.tally_ho.delete_category(cmd.category)

def process_cli_cmds(cmd):
    """Execute a category or tally method based on user input."""
    if cmd.item == "category":
        return execute_category_action(cmd)
    elif cmd.item == "tally":
        return execute_tally_action(cmd)

def fmt_output(item):
    if isinstance(item, tally_ho.Category):
        return [[item.id, item.name]]
    elif isinstance(item, list) and isinstance(item[0], tally_ho.Category):
        cat_list = [[cat.id, cat.name] for cat in item]
        return cat_list
    elif isinstance(item, tally_ho.Tally):
        return [[item.id, item.name, item.category, item.count]]
    elif isinstance(item, list) and isinstance(item[0], tally_ho.Tally):
        tally_list = [[tally.id, tally.name, tally.category, tally.count] for tally in item]
        return tally_list

def _args_or_none(arg):
    """Return None if the arg is 'None' or the arg."""
    if arg == 'None':
        return None
    return arg

def parse_args(args_list, db):
    th = tally_ho.TallyHo(db)
    parser = argparse.ArgumentParser(description="A python based cli for creating tallies.")
    item_group = parser.add_argument_group('item', description="Interact with tallies and categories")
    item_group.add_argument('item', nargs='?', choices=[
                            'category', 'tally'], help='Interact with categories')
    item_group.add_argument('action', nargs='?', choices=[
                        'create', 'get', 'list', 'update', 'delete'], help='Interact with tallies')
    item_group.add_argument('--tally', nargs='?',
                            help='Name of category or tally')
    item_group.add_argument('--category', nargs='?',
                            help='Name of a category to associate with a tally')
    item_group.add_argument('--quantity', nargs='?', type=int,
                            help='Amount to increase or decrease. Negative or positive integer')

    args = parser.parse_args(args_list)
    item = str(args.item)
    action = str(args.action)
    tally = _args_or_none(str(args.tally))
    category = _args_or_none(str(args.category))
    quantity = _args_or_none(str(args.quantity))

    cmd = Command(item, action, tally, category, quantity, th)
    return cmd