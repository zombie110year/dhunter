from .database import FILEINFO
import colorama as c
import platform as p

if p.platform() == "Windows":
    c.init()

def showStatus():
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
