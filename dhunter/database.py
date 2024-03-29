r"""包装数据库:

1. 如果本机已安装 SQLite3, 则使用它
2. 如果未安装 SQLite3, 则使用 Python 字典

在任何数据存储对象中, 存储都是 Python 原生对象
"""

import pickle
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


class VersionError(Exception):
    # 数据库中的文件格式不同, 导致当前版本无法解析
    pass


class MemoryDict:
    """存储 path, md5, mtime 元组, 以 path 为键:

    .. code::
        :caption: self._datum

        {
            path: FileItem(path: str, hash: str, mtime: float)
        }
    """

    DB_VERSION = 1

    def __init__(self, db_path):
        self._old_datum = dict()    # 旧的数据库, 从 .fileinfo.db 中读取而来
        self._old_index = dict()    # 旧的索引, 从 .fileinfo.db 中读取而来
        self._datum = dict()    # 以 path-FileItem 为键值对的数据库, 每次 scan 都会新建
        self._index = dict()    # 以 hash-{path, } 为键值对的索引, 每次 scan 都会新建
        self._db_path = db_path
        self._load()

    def select(self, path: str) -> float:
        """从旧数据库或索引中以绝对路径为键查询一个值
        如果存在, 则返回对应的 mtime, 否则, 返回 None
        """
        _item = self._old_datum.get(path, None)
        if _item is not None:
            return _item.mtime
        else:
            return None

    def insert(self, path: str, hash: str, mtime: float):
        """向新数据库新增一个条目

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

    def update(self, path: str):
        """原件相同, 不需要重新计算 hash 值,
        从旧数据库中向新数据库直接复制数据

        :param str path: 绝对路径
        """
        # 查找旧记录
        _old_item = self._old_datum[path]
        self.insert(_old_item.path, _old_item.hash, _old_item.mtime)

    def query(self, hash):
        """从旧记录中获取具有相同 hash 值的 FileItem 集合,
        按照 mtime 的顺序排序
        """
        _item_list = list(self._old_index[hash])
        _item_list.sort(key=lambda x: self._old_datum[x].mtime)
        return _item_list

    def hashs(self):
        """获取数据库中已存储的所有 hash 值
        """

        return self._old_index.keys()

    def duped_hashs(self):
        """获取数据库中重复条目的 hash 值
        """

        result = []
        for hash in self._old_index.keys():
            if len(self._old_index[hash]) >= 2:
                result.append(hash)

        return result

    def _load(self):
        """从 cwd 中读取 .fileinfo.db 内容
        将其设为 self._old_datum 和 self._old_index
        """
        _db_path = Path(self._db_path)
        if _db_path.exists():
            _db = _db_path.open("rb")
            _wrap = pickle.load(_db)
            if _wrap["version"] == self.DB_VERSION:
                self._old_datum, self._old_index = _wrap["datum"], _wrap["index"]
            else:
                raise VersionError("database dump file version error, delete .fileinfo.db and scan again\n"
                                   f"current: {self.DB_VERSION}, dumped: {_wrap['version']}")
            _db.close()

    def _dump(self):
        """保存本次 scan 的结果
        """
        _wrap = {}
        _wrap["version"] = self.DB_VERSION
        _wrap["datum"] = self._datum
        _wrap["index"] = self._index

        _db_path = Path(self._db_path)
        if not _db_path.exists():
            _db_path.touch()

        _db = _db_path.open("wb")
        pickle.dump(_wrap, _db)
        _db.close()


FILEINFO = MemoryDict(FILEINFO_DB_PATH)
CAUGHT_FILES = Queue()


def dumpDB():
    """本次运行结束后调用
    """
    FILEINFO._dump()
