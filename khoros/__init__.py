# -*- coding: utf-8 -*-
"""
:Package:           khoros
:Synopsis:          This is the ``__init__`` module for the khoros package
:Usage:             ``from khoros import Khoros``
:Example:           ``khoros = Khoros(community_url='https://community.example.com', helper='path/to/helper_file.yml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     18 Mar 2020
"""

from . import errors
from .core import Khoros
from .utils import version

__all__ = ['core', 'auth', 'liql', 'errors']

# Define the package version by pulling from the khoros.utils.version module
__version__ = version.get_full_version()

# Display a warning if the running version is not the latest stable version found on PyPI
version.warn_when_not_latest()
