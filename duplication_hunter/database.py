r"""包装数据库:

1. 如果本机已安装 SQLite3, 则使用它
2. 如果未安装 SQLite3, 则使用 Python 字典与
"""

import pickle
import sys
from pathlib import Path
from queue import Queue

from .setting import FILEINFO_DB_PATH


class MemoryDict:
    def __init__(self, db_path):
        self._datum = dict()
        self._db_path = db_path
        self._load()

    def put(self, key, value):
        if key not in self._datum:
            self._datum[key] = [value, ]
        else:
            self._datum[key].append(value)

    def get(self, key):
        return self._datum[key]

    def keys(self):
        for key in self._datum:
            if len(self._datum[key]) > 1:
                yield key

    def item_count(self):
        """重复条目的数量, 多个重复条目归为一条
        """
        count = 0
        for key in self._datum:
            item = self._datum[key]
            if len(item) > 1:
                count += 1

        return count

    def _load(self):
        _db_path = Path(self._db_path)
        if _db_path.exists():
            _db = _db_path.open("rb")
            self._datum = pickle.load(_db)
            _db.close()

    def _dump(self):
        _db_path = Path(self._db_path)
        if not _db_path.exists():
            _db_path.touch()
        else:
            print(
                "{}: file exists, overwrite? [y/n]".format(self._db_path), file=sys.stderr, end=" ")
            _ = input()
            _overwrite = True if _ == "y" else False
            if not _overwrite:
                return

        _db = _db_path.open("wb")
        pickle.dump(self._datum, _db)
        _db.close()


class SQLiteDB:
    def __init__(self, path):
        pass

    def _init_db(self):
        pass

    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def keys(self):
        pass

    def _load(self, path):
        pass

    def _dump(self, path):
        pass


class SimpleDatabaseFactory(type):
    def __new__(self, path):
        if installed("sqlite3"):
            type_ = SQLiteDB
        else:
            type_ = MemoryDict

        return type_(path)


def installed(cmd):
    return False


FILEINFO = SimpleDatabaseFactory(FILEINFO_DB_PATH)
CAUGHT_FILES = Queue()
