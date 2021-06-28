# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_settings
:Synopsis:       This module is used by pytest to verify the :py:mod:`khoros.objects.settings` functionality.
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  27 Jun 2021
"""

import os
import sys

import pytest

from . import resources

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


def test_v1_node_setting_retrieval():
    """This function tests the retrieval of an API v1 node.

    .. versionadded:: 4.1.0
    """
    if not resources.local_test_config_exists():
        pytest.skip("skipping local-only tests")
    test_config = resources.get_testing_config()
    node_id = test_config.get('test_data').get('settings').get('node_id')
    # TODO: Finish the function

