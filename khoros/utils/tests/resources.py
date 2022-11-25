# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.resources
:Synopsis:          Frequently used resources for performing unit testing
:Usage:             ``from khoros.utils.tests import resources``
:Example:           ``exceptions = resources.import_exceptions_module()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     25 Nov 2022
"""

import os
import sys
import json
import importlib

import yaml
import pytest

# Define global variable to store the YAML test settings
test_config = {}

# Define constants
SKIP_LOCAL_TEST_MSG = 'skipping local-only tests'


class MockResponse:
    """This class simulates an API response for testing purposes.

    .. versionchanged:: 5.2.0
       The ``status_code`` attribute has been added to the object.

    .. versionadded:: 5.1.2
    """
    def __init__(self, json_body, status_code=200):
        self.json_body = json_body
        self.status_code = status_code

    def json(self):
        return self.json_body


def mock_success_post(*args, **kwargs):
    """This function works with the `MockedResponse` class to simulate a successful API response.

    .. versionadded:: 5.1.2
    """
    return MockResponse({
        "status": "success"
    })


def mock_error_post(*args, **kwargs):
    """This function works with the `MockedResponse` class to simulate a failed API response.

    .. versionadded:: 5.1.2
    """
    return MockResponse({
        "status": "error",
        "message": "There was an error",
        "data": {
            "code": "500",
            "type": "error"
        }
    })


def mock_bulk_data_json(*args, **kwargs):
    """This function works with the `MockedResponse` class to simulate a Bulk Data API JSON response.

    .. versionadded:: 5.2.0
    """
    return MockResponse({
        "records": []
    })


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.

    .. versionadded:: 2.7.4
    """
    sys.path.insert(0, os.path.abspath('../..'))


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


def _get_control_dataset_file(_dataset_name):
    """This function returns the file name associated with a particular dataset.

    .. versionadded:: 5.1.0

    :param _dataset_name: The name of the dataset
    :type _dataset_name: str
    :returns: The file name if found or a blank string
    """
    # Define the dataset file mapping
    _datasets = {
        'categories': 'categories_control_data.json',
        'communities': 'communities_control_data.json',
    }
    try:
        _dataset_file = _datasets[_dataset_name]
    except KeyError:
        _dataset_file = ''
    return _dataset_file


def import_control_data(dataset_name):
    """This function imports a local control data file as a dictionary.

    .. versionchanged:: 5.1.1
       The function has been updated to support GitHub Workflows control data.

    .. versionadded:: 5.1.0

    :param dataset_name: The name of the dataset
    :type dataset_name: str
    :returns: The JSON data as a dictionary
    :raises: :py:exc:`FileNotFoundError`
    """
    data = None
    dataset_file = _get_control_dataset_file(dataset_name)
    file_paths = [
        f'{os.environ.get("HOME")}/secrets/{dataset_file}',
        f'local/tests/{dataset_file}',
    ]
    for path in file_paths:
        if os.path.isfile(path):
            with open(path, 'r') as file:
                data = json.load(file)
                break
    if data is None:
        raise FileNotFoundError(f'The {dataset_name} control data cannot be found.')
    return data


def control_data_exists(dataset_name):
    """This function checks to see if a local control data file exists.

    .. versionchanged:: 5.1.1
       The function has been updated to support GitHub Workflow control data.

    .. versionadded:: 5.1.0

    :param dataset_name: The name of the dataset
    :type dataset_name: str
    :returns: Boolean value indicating whether the file was found
    """
    data_exists = False
    dataset_file = _get_control_dataset_file(dataset_name)
    if dataset_file and (os.path.isfile(f'{os.environ.get("HOME")}/secrets/{dataset_file}') or
                         os.path.isfile(f'local/tests/{dataset_file}')):
        data_exists = True
    return data_exists


def get_control_data(dataset_name):
    """This function retrieves the control data used in various tests.

    .. versionadded:: 5.1.1
    """
    if not control_data_exists(dataset_name):
        pytest.skip('skipping tests where control data is unavailable')

    # Import the control data
    control_data = import_control_data(dataset_name)

    # Return the control data and the core object
    return control_data


def get_core_object():
    """This function instantiates and returns the core object using a local helper file.

    .. versionadded:: 5.1.1
    """
    set_package_path()
    if secrets_helper_exists():
        khoros_object = instantiate_with_secrets_helper()
    else:
        if not local_test_config_exists() or not local_helper_exists():
            pytest.skip('skipping tests where a valid helper file is needed')
        khoros_object = instantiate_with_local_helper(production=False)
    return khoros_object


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
    :returns: The appropriate collection
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

    :param _production: Defines whether the helper file is associated with a Production environment
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

    :param production: Defines whether the helper file is associated with a Production environment
    :type production: bool, None
    :returns: Boolean value indicating whether the local helper file was found
    """
    file_name = _get_local_helper_file_name(production)
    return os.path.exists(f'local/{file_name}')


def local_test_config_exists():
    """This function checks to see if the *khorostest.yml* file is present in the ``local/`` directory.

    .. versionadded:: 4.1.0

    :returns: Boolean value indicating whether the file was found
    """
    return os.path.exists('local/khorostest.yml')


def parse_testing_config_file():
    """This function parses the ``local/khorostest.yml`` file when present.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.

    .. versionadded:: 4.1.0
    """
    global test_config
    if local_test_config_exists():
        with open('local/khorostest.yml', 'r') as file:
            test_config = yaml.safe_load(file)


def get_testing_config():
    """This function returns the test config data from the ``local/khorostest.yml`` file when present.

    .. versionadded:: 4.1.0
    """
    if not test_config and local_test_config_exists():
        parse_testing_config_file()
    return test_config


def secrets_helper_exists():
    """This function checks to see if the unencrypted helper file exists for GitHub Workflows.

    .. versionadded:: 5.1.1
    """
    helper_path = f'{os.environ.get("HOME")}/secrets/khoros_helper.yml'
    return os.path.isfile(helper_path)


def instantiate_with_local_helper(production=False):
    """This function instantiates a Khoros object using a local helper file for unit testing.

    .. versionchanged:: 5.1.0
       The function has been updated to raise the :py:exc:`FileNotFoundError` exception if the file is not found.

    .. versionadded:: 4.1.0

    :param production: Defines whether the helper file is associated with a Production environment
    :type production: bool, None
    :returns: The instantiated :py:class:`khoros.core.Khoros` object
    :raises: :py:exc:`FileNotFoundError`
    """
    file_name = _get_local_helper_file_name(production)
    if not local_helper_exists():
        raise FileNotFoundError('The local helper file cannot be found.')
    set_package_path()
    core_module = importlib.import_module('khoros.core')
    return core_module.Khoros(helper=f"local/{file_name}")


def instantiate_with_secrets_helper():
    """This function instantiates a Khoros object using the unencrypted helper file intended for GitHub Workflows.

    .. versionadded:: 5.1.1

    :returns: The instantiated :py:class:`khoros.core.Khoros` object
    :raises: :py:exc:`FileNotFoundError`
    """
    if not secrets_helper_exists():
        raise FileNotFoundError('The unencrypted GitHub Workflows helper file cannot be found.')
    file_name = f'{os.environ.get("HOME")}/secrets/khoros_helper.yml'
    set_package_path()
    core_module = importlib.import_module('khoros.core')
    return core_module.Khoros(helper=file_name)


def instantiate_with_placeholder():
    """This function instantiates a Khoros object with placeholder data.

    .. versionadded:: 5.0.0

    :returns: The instantiated :py:class:`khoros.core.Khoros` object
    """
    set_package_path()
    core_module = importlib.import_module('khoros.core')
    return core_module.Khoros(placeholder=True)
