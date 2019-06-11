import platform as p

import colorama as c

from .database import FILEINFO


def simpleShow():
    if p.platform() == "Windows":
        c.init()

    _hashs = FILEINFO.duped_hashs()
    _total = len(_hashs)
    print("---")
    print(f"total: {_total}")
    print("---")
    _count = 0
    for hash in _hashs:
        _count += 1
        paths = FILEINFO.query(hash)
        print(c.Fore.GREEN, f"{_count} ++++ ", paths[0], c.Style.RESET_ALL)
        for path in paths[1:]:
            print(c.Fore.RED, "| ", path, c.Style.RESET_ALL)
        print()
