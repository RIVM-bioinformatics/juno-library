from __future__ import print_function

import sys, os
from typing import List

if sys.version_info < (3, 9):
    print(
        "At least Python 3.10 is required for the Juno pipelines to work.\n",
        file=sys.stderr,
    )
    exit(1)


try:
    from setuptools import setup, find_packages
except ImportError:
    print(
        "Please install setuptools before installing juno_library.\n",
        file=sys.stderr,
    )
    exit(1)

# read metadata, replacing the breaking """from juno_library.version import ( .... )"""
meta = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "juno_library", "version.py"), "r", encoding="utf-8") as f:
    exec(f.read(), meta)

def parse_requirements(filename:str="requirements.txt") -> List[str]:
    """ parse the/a requirements.txt file into a list for setup(install_requires=[]) """
    with open(filename, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

setup(
    name=meta["__package_name__"],
    version=meta["__version__"],
    author=meta["__authors__"],
    author_email=meta["__email__"],
    description=meta["__description__"],
    license=meta["__license__"],
    zip_safe=False,
    packages=find_packages(),
    scripts=["juno_library/run.py"],
    package_data={"juno_library": ["envs/*", "py.typed"]},
    install_requires=parse_requirements(os.path.join(here, "requirements.txt")),
    entry_points={"console_scripts": ["juno_pipeline = juno_library.run:main"]},
    include_package_data=True,
)
