from __future__ import print_function

from juno_library import juno_info
import sys

if sys.version_info < (3, 7):
    print(
        "At least Python 3.7 is required for the Juno pipelines to work.\n",
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
    name=juno_info.__package_name__,
    version=juno_info.__version__,
    author=juno_info.__authors__,
    author_email=juno_info.__email__,
    description=juno_info.__description__,
    zip_safe=False,
    license=juno_info.__license__,
    packages=find_packages(include=["juno_library", "juno_library.*"]),
    scripts=["juno_library/juno_library.py"],
    package_data={"juno_library": ["envs/*"]},
    install_requires=[
        "pandas>=1.5",
        "drmaa>=0.7.9",
        "snakemake>=7.18",
        "xlrd>=2.0",
        "unittest2",
        "pip>=22.3",
        "pyyaml>=6.0",
        "numpy>=1.23",
        "dask",
        "unittest2",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "juno_pipeline = juno_library:main"
        ]
    },
    include_package_data=True,
)
