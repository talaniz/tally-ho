"""Console script for tally_ho."""
import argparse
import sys

from tabulate import tabulate

from tally_ho import tally_ho
from tally_ho.cmd import Command, process_cli_cmds, fmt_output, parse_args
from tally_ho.config import ConfigHandler


def main():
    """Console script for tally_ho.
    ***Next steps: Create the command line implementation
    Print tables
    Functionalize and test argparse setup
    Create homebrew formula
    Test, check coverage, tag release
    """
    
    cfg_handler = ConfigHandler()
    cfg_handler.load_config()
    db = cfg_handler.db
    cmd = parse_args(sys.argv, db)
    res = process_cli_cmds(cmd)
    res = fmt_output(res)

    if cmd.item == "category":
        print("========== Categories ==========")
        print(tabulate(res, headers=['id', 'name'], tablefmt='fancy_grid'))
    elif cmd.item == "tally":
        print("========== Tallies ==========")
        print(tabulate(res, headers=['id', 'name', 'category', 'count'], tablefmt='fancy_grid'))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
