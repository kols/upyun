#!/usr/bin/env python

import os
import sys

import upyun

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='requests',
    version=upyun.__version__,
    description='Feature complete upyun REST client',
    author='Kane Dou',
    author_email='douqilong@gmail.com',
    url='https://github.com/kols/upyun',
    packages=['upyun'],
    package_data={'': ['LICENSE']},
    package_dir={'upyun': 'upyun'},
    include_package_data=True,
    install_requires=['requests'],
    setup_requires=['sphinx'],
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
