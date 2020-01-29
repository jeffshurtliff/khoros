# -*- coding: utf-8 -*-
"""
:Package:        khoros
:Synopsis:       This is the ``__init__`` module for the khoros package
:Usage:          ``import khoros``
:Example:        TBD
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  28 Jan 2020
"""

from .utils import version

# Define the package version by pulling from the khoros.utils.version module
__version__ = version.get_full_version()
