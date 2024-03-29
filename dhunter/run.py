from argparse import ArgumentParser

from .compare import compareFile
from .database import dumpDB
from .search import simpleScan
from .show import simpleShow


def getParser():
    parser = ArgumentParser(
        prog="duplication hunter",
        description="Find duplicated files in a folder",
    )

    cmd = parser.add_subparsers(dest="cmd")
    scan = cmd.add_parser(name="scan", description="scan folder")
    scan.add_argument("root", nargs="?", const=".",
                      default=".", help="Searching starting point")
    # parser.add_argument("--fuzzy", action="store_true", default=False, required=False,
    #                     help="[unsupported now] Use fuzzy matching, similar but not equal files will be place in one item")

    show = cmd.add_parser(
        name="show", description="show status from ./.fileinfo.db")

    return parser


def main():
    args = getParser().parse_args()
    if args.cmd == "scan":
        simpleScan(args.root)
        compareFile()
        dumpDB()
    elif args.cmd == "show":
        simpleShow()
