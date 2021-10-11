# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.resources
:Synopsis:          Frequently used resources for performing unit testing
:Usage:             ``from khoros.utils.tests import resources``
:Example:           ``exceptions = resources.import_exceptions_module()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Jun 2021
"""

import os
import sys
import importlib

import yaml

# Define global variable to store the YAML test ettings
test_config = {}


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


def initialize_khoros_object(use_defined_settings=False, defined_settings=None, append_to_default=False):
    """This function imports the :py:class:`khoros.core.Khoros` class and initializes an object.

    .. versionchanged:: 4.3.0
       Added support for utilizing the ``defined_settings`` parameter.

    .. versionadded:: 2.7.4

    :returns: The initialized :py:class:`khoros.core.Khoros` object
    """
    set_package_path()
    default_defined_settings = {
        'community_url': 'https://community.example.com',
        'auto_connect': False,
        'tenant_id': 'example',
        'auth_type': 'session_auth',
        'session_auth': {
            'username': 'testuser',
            'password': 'fakePassword123',
        },
    }
    core_module = importlib.import_module('khoros.core')
    if use_defined_settings:
        settings = default_defined_settings if defined_settings is None else defined_settings
        if defined_settings and append_to_default:
            settings = default_defined_settings
            settings.update(defined_settings)
        instantiated_object = core_module.Khoros(defined_settings=settings)
    else:
        instantiated_object = core_module.Khoros(community_url='https://community.example.com', auto_connect=False,
                                                 tenant_id='example', auth_type='session_auth',
                                                 session_auth={'username': 'testuser', 'password': 'fakePassword123'})
    return instantiated_object


def get_structure_collection(structure_type):
    """This function identifies the API collection for a given structure type.

    .. versionadded:: 4.1.0

    :param structure_type: The structure type for which to return the corresponding collection.
    :return:
    """
    structure_map = {
        'board': 'boards',
        'category': 'categories',
        'community': 'community',
        'grouphub': 'grouphubs',
    }
    if structure_type in structure_map.values():
        collection = structure_type
    else:
        collection = structure_map.get(structure_type)
    return collection


def _get_local_helper_file_name(_production=False):
    """This function defines the file name of the local helper file to be used with unit testing.

    .. versionadded:: 4.1.0

    :param _production: Defines whether or not the helper file is associated with a Production environment
    :type _production: bool, None
    :returns: The file name for the local helper file
    """
    if _production is None:
        _file_name = 'helper.yml'
    else:
        _file_name = 'prod_helper.yml' if _production else 'stage_helper.yml'
    return _file_name


def local_helper_exists(production=False):
    """This function checks to see if a helper file is present in the ``local/`` directory.

    .. versionadded:: 4.1.0

    :param production: Defines whether or not the helper file is associated with a Production environment
    :type production: bool, None
    :returns: Boolean value indicating whether or not the local helper file was found
    """
    file_name = _get_local_helper_file_name(production)
    return os.path.exists(f'local/{file_name}')


def local_test_config_exists():
    """This function checks to see if the *khorostest.yml* file is present in the ``local/`` directory.

    .. versionadded:: 4.1.0

    :returns: Boolean value indicating whether or not the file was found
    """
    return os.path.exists('local/khorostest.yml')


def parse_testing_config_file():
    """This function parses the ``local/khorostest.yml`` file when present.

    .. versionadded:: 4.1.0

    :returns: None
    """
    global test_config
    if local_test_config_exists():
        with open('local/khorostest.yml', 'r') as file:
            test_config = yaml.safe_load(file)
    return


def get_testing_config():
    """This function returns the test config data from the ``local/khorostest.yml`` file when present.

    .. versionadded:: 4.1.0
    """
    if not test_config and local_test_config_exists():
        parse_testing_config_file()
    return test_config


def instantiate_with_local_helper(production=False):
    """This function instantiates a Khoros object using a local helper file for unit testing.

    .. versionadded:: 4.1.0

    :param production: Defines whether or not the helper file is associated with a Production environment
    :type production: bool, None
    :returns: The instantiated :py:class:`khoros.core.Khoros` object
    """
    file_name = _get_local_helper_file_name(production)
    if local_helper_exists():
        set_package_path()
        core_module = importlib.import_module('khoros.core')
        return core_module.Khoros(helper=f"local/{file_name}")
