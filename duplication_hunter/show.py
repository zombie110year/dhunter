import platform as p
from pathlib import Path

import colorama as c

from .database import FILEINFO

if p.platform() == "Windows":
    c.init()


def simpleShow():
    _total = FILEINFO.item_count()
    print("---")
    print(f"total: {_total}")
    print("---")
    _count = 0
    for key in FILEINFO.keys():
        _count += 1
        paths = FILEINFO.get(key)
        print(c.Fore.GREEN, f"{_count} ++++ ", paths[0], c.Style.RESET_ALL)
        for path in paths[1:]:
            print(c.Fore.RED, "| ", path, c.Style.RESET_ALL)
        print()
