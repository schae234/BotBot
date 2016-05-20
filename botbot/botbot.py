import argparse
from . import checks, schecks, checker

def main():
    parser = argparse.ArgumentParser(description="Manage lab computational resources.")

    # Verbosity options
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose',
                           help='Print issues and fixes for all files',
                           action='store_true')

    # Directory options
    parser.add_argument('path',
                        help='Path to check')
    parser.add_argument('-s', '--shared',
                        help='Use the shared folder ruleset',
                        action='store_true')

    parser.add_argument('-l', '--follow-symlinks',
                        help='Follow symlinks',
                        action='store_true')
    # Initialize the checker
    args = parser.parse_args()

    c = checker.Checker()
    clist = [checks.file_exists,
             checks.is_fastq,
             checks.sam_should_compress]

    if args.shared:
        clist += [schecks.file_groupreadable,
                  schecks.file_group_executable,
                  schecks.dir_group_readable]
    c.register(clist)

    # Check the given directory
    c.check_all(args.path, link=args.follow_symlinks, verbose=args.verbose)

    # Print the list of issues
    c.pretty_print_issues(args.verbose)
