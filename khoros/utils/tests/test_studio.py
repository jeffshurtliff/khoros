# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_studio
:Synopsis:          This module is used by pytest to verify that the ``studio`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

from . import resources


def test_studio_functions():
    """This function tests the various Studio-related functions.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Test if SDK is installed
    sdk_installed = khoros_object.studio.sdk_installed()
    assert isinstance(sdk_installed, bool)

    # Test if Node.js is installed
    node_installed = khoros_object.studio.node_installed()
    assert isinstance(node_installed, bool)

    # Tset if npm is installed
    npm_installed = khoros_object.studio.npm_installed()
    assert isinstance(npm_installed, bool)

    # Test retrieving the Node.js version
    node_version = khoros_object.studio.get_node_version()
    assert node_version is None or isinstance(node_version, str)

    # Test retrieving the npm version
    npm_version = khoros_object.studio.get_npm_version()
    assert npm_version is None or isinstance(npm_version, str)

    # Test retrieving the SDK version
    sdk_version = khoros_object.studio.get_sdk_version()
    assert sdk_version is None or isinstance(sdk_version, str)
