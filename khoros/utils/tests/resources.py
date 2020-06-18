# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.resources
:Synopsis:          Frequently used resources for performing unit testing
:Usage:             ``from khoros.utils.tests import resources``
:Example:           ``exceptions = resources.import_exceptions_module()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     18 Jun 2020
:Version:           1.0.0
"""

import os
import sys
import importlib


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionadded:: 2.7.4

    :returns: None
    """
    sys.path.insert(0, os.path.abspath('../..'))
    return


def import_modules(*modules):
    """This function imports and returns one or more modules to utilize in a unit test.

    .. versionadded:: 2.7.4

    :param modules: One or more module paths (absolute) in string format
    :returns: The imported module(s) as an individual object or a tuple of objects
    """
    imported_modules = []
    for module in modules:
        imported_modules.append(importlib.import_module(module))
    tuple(imported_modules)
    return imported_modules if len(imported_modules) > 1 else imported_modules[0]


def initialize_khoros_object():
    """This function imports the :py:class:`khoros.core.Khoros` class and initializes an object.

    .. versionadded:: 2.7.4

    :returns: The initialized :py:class:`khoros.core.Khoros` object
    """
    set_package_path()
    core_module = importlib.import_module('khoros.core')
    return core_module.Khoros(community_url='https://example.community.com', auto_connect=False,
                              tenant_id='example', auth_type='session_auth',
                              session_auth={'username': 'testuser', 'password': 'fakePassword123'})
