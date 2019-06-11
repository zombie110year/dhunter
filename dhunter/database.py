r"""包装数据库:

1. 如果本机已安装 SQLite3, 则使用它
2. 如果未安装 SQLite3, 则使用 Python 字典

在任何数据存储对象中, 存储都是 Python 原生对象
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
        "hash",      # Hash 值
        "mtime",    # 最近修改时间
    ])


class MemoryDict:
    """存储 path, md5, mtime 元组, 以 path 为键:

    .. code::
        :caption: self._datum

        {
            path: FileItem(path: str, hash: str, mtime: float)
        }
    """

    def __init__(self, db_path):
        self._datum = dict()    # 以 path-FileItem 为键值对的数据库
        self._index = dict()    # 以 hash-{path, } 为键值对的索引
        self._db_path = db_path
        self._load()

    def select(self, path: str) -> float:
        """从数据库或索引中以绝对路径为键查询一个值
        如果存在, 则返回对应的 mtime, 否则, 返回 None
        """
        _item = self._datum.get(path, None)
        if not _item is None:
            return _item.mtime
        else:
            return None

    def insert(self, path: str, hash: str, mtime: float):
        """新增一个条目

        :param str key: hash 值的 字符串表示
        :param str value: 文件的绝对路径
        :param float mtime: 文件的最后修改时间
        """
        # 保存数据
        _item = FileItem(path, hash, mtime)
        self._datum[path] = _item

        # 更新索引
        if hash not in self._index:
            self._index[hash] = set()
        self._index[hash].add(path)

    def update(self, path: str, hash: str, mtime: float):
        """更新一个条目, 有可能在索引中移动此条目

        :param str key: hash 值的 字符串表示
        :param str value: 文件的绝对路径
        :param float mtime: 文件的最后修改时间
        """
        # 查找旧记录
        _old_item = self._datum[path]
        # 插入新记录
        _item = FileItem(path, hash, mtime)
        self._datum[path] = _item
        # 更新索引
        self._index[_old_item.hash].remove(_old_item.path)
        self._index[hash].add(path)

    def query(self, hash):
        """获取具有相同 hash 值的 FileItem 集合,
        按照 mtime 的顺序排序
        """
        _item_list = list(self._index[hash])
        _item_list.sort(key=lambda x: self._datum[x].mtime)
        return _item_list

    def hashs(self):
        """获取数据库中已存储的所有 hash 值
        """

        return self._index.keys()

    def duped_hashs(self):
        """获取数据库中重复条目的 hash 值
        """

        result = []
        for hash in self._index.keys():
            if len(self._index[hash]) >= 2:
                result.append(hash)

        return result

    def _load(self):
        """从 cwd 中读取 .fileinfo.db 内容
        将其设为 self._datum 和 self._index
        """
        _db_path = Path(self._db_path)
        if _db_path.exists():
            _db = _db_path.open("rb")
            self._datum, self._index = pickle.load(_db)
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
        pickle.dump((self._datum, self._index), _db)
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
