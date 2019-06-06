from pathlib import Path

from .database import CAUGHT_FILES


class FileSearcher:

    def __init__(self, root: "path-like, dir", ignore_rule: "callable" = lambda obj: False):
        """生成器, 从 root 开始递归, 将得到的文件保存到 chan 中,
        如果文件满足 ignore_rule 规则, 则被排除.

        :param root: 起点目录
        :param ignore_rule: 返回 Bool 值的实现了 :func:`obj.__call__ 方法的对象.
            当 返回 True 时, 所找到的文件将被忽略.
        """
        if isinstance(root, str):
            self._root = Path(root)
        elif isinstance(root, Path):
            self._root = root
        else:
            raise TypeError("root is not a path-like object")

        self._files = CAUGHT_FILES
        self._ignore_rule = ignore_rule

    def __call__(self):
        _FileSearch(self._root, self._files, self._ignore_rule)


def _FileSearch(root: Path, chan, ignore):
    """见 :func:`FileSearcher`
    """
    assert isinstance(root, Path) and root.is_dir()

    for i in root.iterdir():
        if i.is_file():
            if not ignore(i):
                # 输出
                chan.put(i.absolute())
        elif i.is_dir():
            _FileSearch(i, chan, ignore)


def simpleScan(path, ignore):
    searcher = FileSearcher(path, ignore)
    searcher()
