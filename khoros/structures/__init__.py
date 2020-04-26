# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures
:Synopsis:          This module contains sub-modules that are specific to the various Community structures.
:Usage:             ``from khoros import structures``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Apr 2020
"""

__all__ = ['base', 'categories', 'communities', 'nodes']

# Import all submodules by default
from . import categories
from . import communities
from . import nodes
