"""比较文件

.. graphviz:: img/process.gv
"""
from hashlib import md5
from pathlib import Path
import sys

from .database import CAUGHT_FILES, FILEINFO



def compareFile():
    """对比 CAUGHT_FILES 与数据库中的文件

    1. 对比是否已保存
    2. 对比是否需更新
    """
    while not CAUGHT_FILES.empty():
        path = CAUGHT_FILES.get()
        _file_obj   = Path(path)
        _mtime = _file_obj.stat().st_mtime

        _stored_mtime = FILEINFO.select(path)
        if _stored_mtime is None or _stored_mtime < _mtime:
            # 新增此条目
            print(f"newfile: {path}")
            _hash = md5()
            _hash.update(_file_obj.read_bytes())
            _hash = _hash.hexdigest()
            FILEINFO.insert(path, _hash, _mtime)
        else:
            # 现存文件不需要更新, 直接复制前面的记录即可
            _hash = md5()
            _hash.update(_file_obj.read_bytes())
            _hash = _hash.hexdigest()
            FILEINFO.update(path)
