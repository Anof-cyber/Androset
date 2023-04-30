#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

setup(
    name='androset',
    version=__import__('androset').__version__,
    description='Auto setup android for pentest with auto push burp certificate and redirect traffic to burp with IP Table',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='Sourav Kalal',
    author_email='kalalsourav20@gmail.com',
    license='MIT license',
    url='https://github.com/Anof-cyber/androset',
    download_url='https://github.com/Anof-cyber/androset/archive/v1.1.zip',
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'pyOpenSSL==23.1.1',
        'termcolor==2.3.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'License :: MIT license',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'androset = androset:main'
        ]
    },
    keywords=['androset', 'bug bounty', 'android', 'pentesting', 'security'],
)
