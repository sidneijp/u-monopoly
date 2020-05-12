#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup


setup(
    name='u-monopoly-web',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
)
