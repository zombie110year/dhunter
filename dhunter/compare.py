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

        _stored = FILEINFO.select(path)
        if _stored is None:
            # 新增此条目
            _hash = md5()
            _hash.update(_file_obj.read_bytes())
            _hash = _hash.hexdigest()
            FILEINFO.insert(path, _hash, _mtime)
        else: # 判断是否需要更新
            if _stored.mtime < _mtime:
                # 现存文件更新
                print(f"newfile: {path}")
                _hash = md5()
                _hash.update(_file_obj.read_bytes())
                _hash = _hash.hexdigest()
                FILEINFO.update(path, _hash, _mtime)
