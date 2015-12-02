# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.1.0'

PACKAGE_DEPS = [
    'click',
    'matplotlib',
]

setup(
    name='gitfame',
    version=VERSION,
    description='',
    author='Eemil V\xc3\xa4is\xc3\xa4nen',
    author_email='eemil.vaisanen@iki.fi',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=PACKAGE_DEPS,
    entry_points={
        'console_scripts': [
            'git-fame = gitfame.app:main',
        ]
    },
    zip_safe=False
)
