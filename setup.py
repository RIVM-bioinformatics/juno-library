from __future__ import print_function

from juno_library.version import (
    __package_name__,
    __version__,
    __email__,
    __description__,
    __authors__,
    __license__,
)
import sys

if sys.version_info < (3, 10):
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


setup(
    name=__package_name__,
    version=__version__,
    author=__authors__,
    author_email=__email__,
    description=__description__,
    zip_safe=False,
    license=__license__,
    packages=find_packages(),
    scripts=["juno_library/run.py"],
    package_data={"juno_library": ["envs/*", "py.typed"]},
    install_requires=[
        "pandas>=1.5",
        "pandas-stubs>=1.5",
        "drmaa>=0.7.9",
        "snakemake>=7.24",
        "xlrd>=2.0",
        "pyyaml>=6.0",
        "types-PyYAML>=6.0",
        "black>=23",
        "snakefmt>=0.8",
        "mypy>=1.1",
        "pip>=23",
    ],
    entry_points={"console_scripts": ["juno_pipeline = juno_library.run:main"]},
    include_package_data=True,
)
