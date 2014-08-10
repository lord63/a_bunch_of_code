#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

try:
    from pypandoc import convert
    readme_md = lambda f: convert(f, 'rst')
except ImportError:
    sys.exit("Please install pypandoc first.")
except OSError:
    sys.exit("You probably do not have pandoc installed.")

setup(
    name='v2ex_daily_mission',
    version='0.1.0',
    description='complete mission, get money, from v2ex',
    long_description=readme_md('README.md'),
    url='https://github.com/lord63/a_bunch_of_code/tree/master/v2ex',
    author='lord63',
    author_email='lord63.j@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
    keywords='v2ex daily money sign',
    packages=['v2ex_daily_mission'],
    install_requires=['terminal','requests', 'lxml'],
    package_data={
        'v2ex_daily_mission': ['README.md', 'LICENSE'],
    },
    entry_points={
        'console_scripts':[
            'v2ex_daily_mission=v2ex_daily_mission.v2ex:main']
    }
)
