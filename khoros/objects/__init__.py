# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects
:Synopsis:          This module contains sub-modules that are specific to the various Community API objects.
:Usage:             ``from khoros.objects import base``
:Example:           ``node_id = base.get_node_id('https://community.khoros.com/t5/Khoros-Blog/bg-p/relnote', 'blog')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     11 May 2020
"""

__all__ = ['albums', 'messages', 'roles', 'users']

# Import all submodules by default
from . import albums
from . import messages
from . import roles
from . import users
