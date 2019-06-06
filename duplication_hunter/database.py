r"""包装数据库:

1. 如果本机已安装 SQLite3, 则使用它
2. 如果未安装 SQLite3, 则使用 Python 字典与
"""

import pickle
import sys
from collections import namedtuple
from pathlib import Path
from queue import Queue

from .setting import FILEINFO_DB_PATH

FileItem = namedtuple(
    "FileItem", [
        "path",     # 绝对路径
        "mtime",    # 最近修改时间
    ])


class MemoryDict:
    """存储 hash-path 对
    """

    def __init__(self, db_path):
        self._datum = dict()
        self._db_path = db_path
        self._load()
        self._index = dict()    # 以 path-mtime 为键值对的索引

    def put(self, key, value):
        """保存一个条目

        :param str key: hash 值的 字符串表示
        :param str value: 文件的绝对路径
        """
        if key not in self._datum:
            self._datum[key] = set()

        # 构建条目: 路径, 最近修改时间
        _path = Path(value)
        _mtime = _path.stat().st_mtime
        _path_str = str(_path.absolute())
        _item = FileItem(_path_str, _mtime)

        self._index[_path_str] = _mtime
        self._datum[key].add(_item)

    def get(self, key):
        "获取具有相同 hash 值的 FileItem 集合"
        return list(map(lambda x: x.path, self._datum[key]))

    def keys(self):
        "获取所有的 Hash 值"
        for key in self._datum:
            if len(self._datum[key]) > 1:
                yield key

    def is_new(self, path):
        """检查 path 条目的 mtime. 若当前读取的文件较新则更新

        :param str path: 文件的绝对路径
        """

        if path in self._index:
            if self._index[path].mtime < Path(path).stat().st_mtime:
                return True
            else:
                return False
        else:
            return True

    def item_count(self):
        """条目群组的数量, 多个重复条目归为一个群组
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


def dumpDB():
    """本次运行结束后调用
    """
    FILEINFO._dump()
