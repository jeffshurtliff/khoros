#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Synopsis:          This script is the primary configuration file for the khoros project
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Oct 2021
"""

import setuptools
import codecs
import os.path


def read(rel_path):
    """This function reads the ``version.py`` script in order to retrieve the version.

    .. versionadded:: 4.0.0
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    """This function retrieves the current version of the package without needing to import the
       :py:mod:`khoros.utils.version` module in order to avoid dependency issues.

    .. versionadded:: 4.0.0
    """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    raise RuntimeError("Unable to find the version string")


with open("README.md", "r") as fh:
    long_description = fh.read()

version = get_version("khoros/utils/version.py")

setuptools.setup(
    name="khoros",
    version=version,
    author="Jeff Shurtliff",
    author_email="jeff.shurtliff@rsa.com",
    description="Useful tools and utilities to assist in managing a Khoros Community (formerly Lithium) environment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffshurtliff/khoros",
    project_urls={
        'Changelog': 'https://khoros.readthedocs.io/en/latest/changelog.html',
        'Documentation': 'https://khoros.readthedocs.io/',
        'Issue Tracker': 'https://github.com/jeffshurtliff/khoros/issues',
        'Khoros Dev Docs': 'https://developer.khoros.com/khoroscommunitydevdocs',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYAML>=5.3.1",
        "urllib3>=1.26.2",
        "requests>=2.23.0",
        "setuptools~=52.0.0",
        "defusedxml>=0.7.1"
    ],
    extras_require={
        'sphinx': [
            'Sphinx>=3.4.0',
            'sphinxcontrib-applehelp>=1.0.2',
            'sphinxcontrib-devhelp>=1.0.2',
            'sphinxcontrib-htmlhelp>=1.0.3',
            'sphinxcontrib-jsmath>=1.0.1',
            'sphinxcontrib-qthelp>=1.0.3',
            'sphinxcontrib-serializinghtml>=1.1.4'
        ],
    }
)
