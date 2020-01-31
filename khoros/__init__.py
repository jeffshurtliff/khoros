# -*- coding: utf-8 -*-
"""
:Package:        khoros
:Synopsis:       This is the ``__init__`` module for the khoros package
:Usage:          ``import khoros``
:Example:        ``khoros.initialize(base_url='community.example.com', community='mycommunity')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  31 Jan 2020
"""

from . import core, errors
from .utils import version

__all__ = ['core', 'auth', 'errors']

# Define the package version by pulling from the khoros.utils.version module
__version__ = version.get_full_version()
