from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pandoc-glosses',
    version='0.1.0',
    description='A pandoc filter for interlinear glosses',
    long_description=long_description,
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
    )
