from pathlib import Path

from .database import CAUGHT_FILES


class FileSearcher:

    def __init__(self, root: "path-like, dir"):
        """生成器, 从 root 开始递归, 将得到的文件保存到 self._files 中

        :param root: 起点目录
        """
        if isinstance(root, str):
            self._root = Path(root)
        elif isinstance(root, Path):
            self._root = root
        else:
            raise TypeError("root is not a path-like object")

        self._files = CAUGHT_FILES

    def __call__(self):
        _FileSearch(self._root, self._files)


def _FileSearch(root: Path, chan):
    """见 :func:`FileSearcher`
    """
    assert isinstance(root, Path) and root.is_dir()

    for i in root.iterdir():
        if i.is_file():
            chan.put(i.absolute())
        elif i.is_dir():
            _FileSearch(i, chan)


def simpleScan(path):
    searcher = FileSearcher(path)
    searcher()
