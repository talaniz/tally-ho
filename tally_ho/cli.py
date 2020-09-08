"""Console script for tally_ho."""
import argparse
import sys


def main():
    """Console script for tally_ho.
    ***Next steps: Create the command line implementation
    ex. `tally-ho category create ${cat}`
    ex. `tally-ho tally create ${tally}`
    ex. `tally-ho tally update ${tally} --amount $amt}`
    ex. `tally-ho category delete ${cat}`
    ex. `tally-ho tally delete ${tally}`
    1. Check for correct arguments
    2. Check for correct configs
    3. Process request
    """
    parser = argparse.ArgumentParser(description="A python based cli for creating tallies.")
    parser.add_argument('item', nargs='?', choices=['category', 'tally'], help='Interact with categories')
    parser.add_argument('action', nargs='?', choices=[
                        'create', 'update', 'delete'], help='Interact with tallies')
    parser.add_argument('--name', nargs='?', help='Name of category or tally')
    parser.add_argument('--quantity', nargs='?', type=int, help='Amount to increase or decrease. Negative or positive integer')
    
    args = parser.parse_args()


    print("Results:\n")
    print("item: " + str(args.item))
    print("action: " + str(args.action))
    print("name: " + str(args.name))
    print("quantity: " + str(args.quantity))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
