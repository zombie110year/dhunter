# 重复猎人

找出指定目录下所有相同的文件.

默认情况下将 md5 值相同的文件归为一组.

# 使用方法

1. 先使用子命令 scan 扫描目标文件夹
2. 再使用子命令 show 显示重复的文件

## scan 参数: `root`

第一个参数, 指定搜索起点, 默认为当前工作目录.

```sh
# 搜索当前目录
dhunt scan

# 搜索 D:/xiaoshipin 目录
dhunt scan D:/xiaoshipin
```

## scan 参数: `--ignore`

可选参数, 指定文件排除规则, 使用 Python 的 lambda 表达式, 如果文件对象满足此条件, 则不被包含在重复列表中, 传入的参数是名为 `o` 的 `pathlib.Path` 对象. 支持使用正则模块(re).

示例:

```python
o.name != '.fileinfo.db'
```

<!-- ## `--fuzzy`

启用模糊搜索, 将判据 "相同" 更改为 "相似".

(暂不支持, 等我学明白聚类算法再来搞) -->

## show:

```sh
# 展示当前目录下 .fileinfo.db 中存储的重复项
dunt show
```
