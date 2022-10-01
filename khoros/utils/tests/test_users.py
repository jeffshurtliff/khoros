# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_users
:Synopsis:          This module is used by pytest to verify that the ``users`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Oct 2022
"""

import os
import sys

import pytest
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


def test_impersonate_user():
    """This function tests the ability to impersonate a user.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Perform the API call to impersonate a user
    khoros_object.users.impersonate_user('joeCustomer')


def test_create_user(monkeypatch):
    """This function tests the ability to create a user.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_success_post)

    # Perform the API call and assert that it was successful
    response = khoros_object.users.create(
        login='testUser',
        email='test@test.com',
        first_name='Test',
        last_name='User')
    assert response.get('status') == 'success'


def test_failed_create_user(monkeypatch):
    """This function verifies that the appropriate exception is raised if the user creation process fails.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_error_post)

    # Perform the API call and assert that it was successful
    with pytest.raises(exceptions.UserCreationError):
        khoros_object.users.create(
            login='testUser',
            email='test@test.com',
            first_name='Test',
            last_name='User')


# Import the exceptions modules
exceptions = resources.import_modules('khoros.errors.exceptions')
