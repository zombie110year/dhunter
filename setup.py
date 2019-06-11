from setuptools import setup

setup(
    name="dhunter",
    version="0.1.0",
    author="Zombie110year",
    author_email="zombie110year@outlook.com",
    license="MIT",
    description="search all duplicated files in a folder",
    url="https://github.com/zombie110year/duplication_hunter",
    packages=["dhunter"],
    entry_points={
        "console_scripts": [
            "dhunt = dhunter.run:main"
        ]
    },
    require=["colorama", "sqlite3"],
)
