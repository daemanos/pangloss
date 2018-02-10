from setuptools import setup, find_packages
from codecs import open
from os import path

from pangloss import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pangloss',
    version=__version__,
    description='A pandoc filter for interlinear glosses',
    long_description=long_description,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'pangloss = pangloss.pangloss:main'
            ]
        }
    )
