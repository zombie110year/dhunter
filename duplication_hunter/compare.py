from hashlib import md5
from pathlib import Path

from .database import CAUGHT_FILES, FILEINFO


def compareFile():
    while not CAUGHT_FILES.empty():
        file = CAUGHT_FILES.get()
        if FILEINFO.is_new(file):
            _md5 = md5()
            _md5.update(Path(file).read_bytes())
            _hash = _md5.hexdigest()
            FILEINFO.put(_hash, str(file))
