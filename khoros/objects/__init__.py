# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects
:Synopsis:          This module contains sub-modules that are specific to the various Community API objects.
:Usage:             ``from khoros import objects``
:Example:           ``objects.archives.archive(khoros_obj, '123', suggested_url, return_status=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Sep 2021
"""

__all__ = ['albums', 'archives', 'attachments', 'base', 'labels', 'messages', 'roles', 'settings', 'subscriptions',
           'tags', 'users']

# Import all submodules by default
from . import albums
from . import archives
from . import attachments
from . import base
from . import labels
from . import messages
from . import roles
from . import settings
from . import subscriptions
from . import tags
from . import users
