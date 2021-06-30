# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_settings
:Synopsis:       This module is used by pytest to verify the :py:mod:`khoros.objects.settings` functionality.
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  28 Jun 2021
"""

import os
import sys

import pytest

from . import resources
from ...errors import exceptions

# Define a global variable to define when the package path has been set
package_path_defined = False


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionadded:: 4.1.0
    """
    global package_path_defined
    if not package_path_defined:
        sys.path.insert(0, os.path.abspath('../..'))
        package_path_defined = True
    return


def test_node_setting_retrieval():
    """This function tests the retrieval of API v1 and v2 node settings.

    .. versionadded:: 4.1.0
    """
    if not resources.local_test_config_exists() or not resources.local_helper_exists():
        pytest.skip("skipping local-only tests")

    # Instantiate the Khoros object
    set_package_path()
    khoros_object = resources.instantiate_with_local_helper()

    # Define the elements to query
    test_config = resources.get_testing_config()
    v1_setting = test_config.get('test_data').get('settings').get('node_v1_setting')
    v2_setting = test_config.get('test_data').get('settings').get('node_v2_setting')
    node_id = test_config.get('test_data').get('settings').get('node_id')
    node_type = test_config.get('test_data').get('settings').get('node_type')

    # Retrieve and verify the v1 setting
    setting = khoros_object.settings.get_node_setting(v1_setting, node_id, node_type, convert_json=False)
    assert isinstance(setting, str) or setting is None          # nosec

    # Retrieve and verify the v2 setting
    setting = khoros_object.settings.get_node_setting(v2_setting, node_id, node_type, convert_json=True)
    assert isinstance(setting, dict) or setting is None         # nosec


def test_invalid_node_type_exception():
    """This function tests to confirm that invalid nodes will raise the
    :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError` exception.

    .. versionadded:: 4.1.0
    """
    # Instantiate the Khoros object
    set_package_path()
    khoros_object = resources.initialize_khoros_object()

    # Test most common invalid node types
    for invalid_type in ['boards', 'categories', 'group hubs', 'grouphubs']:
        with pytest.raises(exceptions.InvalidNodeTypeError):
            khoros_object.settings.get_node_setting('custom.pretend_setting', 'fake-node', invalid_type)

    # Test that converting a node to plural also results in the exception
    node_type = resources.get_structure_collection('board')
    with pytest.raises(exceptions.InvalidNodeTypeError):
        khoros_object.settings.get_node_setting('custom.pretend_setting', 'fake-node', node_type)
