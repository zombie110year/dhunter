from setuptools import setup

setup(
    name="duplication_hunter",
    version="0.1.0",
    author="Zombie110year",
    author_email="zombie110year@outlook.com",
    license="MIT",
    description="search all duplicated files in a folder",
    url="https://github.com/zombie110year/duplication_hunter",
    packages=["duplication_hunter"],
    entry_points={
        "console_scripts": [
            "dhunt = duplication_hunter.run:main"
        ]
    },
    require=["colorama"],
)
