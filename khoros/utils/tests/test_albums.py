# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_albums
:Synopsis:          This module is used by pytest to verify that the ``albums`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     30 Sep 2022
"""

import os
import sys

import requests

from . import resources

# Define a global variable to define when the package path has been set
package_path_defined = False


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionadded:: 5.1.2
    """
    global package_path_defined
    if not package_path_defined:
        sys.path.insert(0, os.path.abspath('../..'))
        package_path_defined = True


def test_create_album(monkeypatch):
    """This function tests the ability to create an album.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_success_post)

    # Perform and assess the mock API call
    response = khoros_object.albums.create('My New Album', 'The description', full_response=False)
    assert response is True


def test_failed_create_album(monkeypatch):
    """This function tests the response of the ``create`` method when the API returns an error.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_error_post)

    # Perform and assess the mock API call
    response = khoros_object.albums.create('My New Album', 'The description', full_response=False)
    assert response is False
