"""Console script for tally_ho."""
import argparse
import sys

from tabulate import tabulate

from tally_ho import tally_ho
from tally_ho.cmd import Command, process_cli_cmds, fmt_output
from tally_ho.config import ConfigHandler


def main():
    """Console script for tally_ho.
    ***Next steps: Create the command line implementation
    Print tables
    Functionalize and test argparse setup
    Create homebrew formula
    Test, check coverage, tag release
    """
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

    args = parser.parse_args()
    item = str(args.item)
    action = str(args.action)
    tally = str(args.tally)
    category = str(args.category)
    quantity = str(args.quantity)
    
    cfg_handler = ConfigHandler()
    cfg_handler.load_config()

    db = cfg_handler.db
    th = tally_ho.TallyHo(db)

    cmd = Command(item, action, tally, category, quantity, th)
    print(cmd)
    res = process_cli_cmds(cmd)
    res = fmt_output(res)
    # TODO: add tabulate and print here, then clean up this file

    if cmd.item == "category":
        print("========== Categories ==========")
        print(tabulate(res, headers=['id', 'name'], tablefmt='fancy_grid'))
    elif cmd.item == "tally":
        print("========== Tallies ==========")
        print(tabulate(res, headers=['id', 'name', 'category', 'count'], tablefmt='fancy_grid'))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
