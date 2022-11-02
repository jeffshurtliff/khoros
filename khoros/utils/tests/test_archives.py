# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_archives
:Synopsis:          This module is used by pytest to verify that the ``archives`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Nov 2022
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


def test_archive_content(monkeypatch):
    """This function tests the ability to archive content.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_success_post)

    # Perform and assess the mock API call using a message ID
    response = khoros_object.archives.archive('12345')
    assert response.get('status') == 'success'

    # Perform and assess the mock API call using a message URL
    response = khoros_object.archives.archive(message_url='https://community.example.com/t5/-/-/ta-p/12345')
    assert response.get('status') == 'success'


def test_unarchive_content(monkeypatch):
    """This function tests the ability to unarchive content.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_success_post)

    # Perform and assess the mock API call using a message ID
    response = khoros_object.archives.unarchive('12345')
    assert response.get('status') == 'success'

    # Perform and assess the mock API call using a message URL
    response = khoros_object.archives.unarchive(message_url='https://community.example.com/t5/-/-/ta-p/12345')
    assert response.get('status') == 'success'


def test_archive_check():
    """This function tests the ability to check whether a message is archived.

    .. versionadded:: 5.2.0
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Define message IDs to test
    archived_content = '30127'
    online_content = '58909'

    # Perform and assess the methods
    assert khoros_object.archives.is_archived(archived_content) is True
    assert khoros_object.archives.is_archived(online_content) is False


