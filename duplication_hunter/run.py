import re
from argparse import ArgumentParser

from .compare import compareFile
from .database import dumpDB
from .search import FileSearcher
from .show import showStatus


def simpleHandle(path, ignore):

    searcher = FileSearcher(path, ignore)
    searcher()
    compareFile()
    dumpDB()
    showStatus()


def getParser():
    parser = ArgumentParser(
        prog="duplication hunter",
        description="Find duplicated files in a folder",
    )

    parser.add_argument("root", nargs="?", const=".",
                        default=".", help="Searching starting point")
    parser.add_argument("--ignore", required=False,
                        help="[danger] Ignore rule, use Python lambda expression, 'o' is the input argument")
    # parser.add_argument("--fuzzy", action="store_true", default=False, required=False,
    #                     help="[unsupported now] Use fuzzy matching, similar but not equal files will be place in one item")

    return parser


def main():
    args = getParser().parse_args()
    def _expr(o): return False
    _code = compile(f"_expr = lambda o: {args.ignore}", '', "exec")
    exec(_code, locals())
    simpleHandle(args.root, _expr)
