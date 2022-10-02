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


def test_unsupported_update_sso_id():
    """This function tests to ensure the ``CurrentlyUnsupportedError`` exception is raised when trying to update the
    SSO ID of a user.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Perform the API call and assert that the exception is raised
    with pytest.raises(exceptions.CurrentlyUnsupportedError):
        khoros_object.users.update_sso_id('abcdEFGH', user_login='joeCustomer')


def test_get_user_identifiers():
    """This function tests the ability to retrieve the identifiers for a user.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Retrieve the User ID and assert the response was expected
    user_id = khoros_object.users.get_user_id(login='joeCustomer')
    assert isinstance(user_id, int) and user_id > 0
    # TODO: Troubleshoot why the test below fails with a LiQL invalid query syntax error
    # user_id = khoros_object.users.get_user_id(first_name='Joe', last_name='Customer')
    # assert isinstance(user_id, int) and user_id > 0

    # Retrieve the email address through various methods and assert the response was expected
    email = khoros_object.users.get_email(user_id=user_id)
    assert isinstance(email, str) and '@' in email
    email = khoros_object.users.get_email(login='joeCustomer')
    assert isinstance(email, str) and '@' in email

    # Retrieve the username through various methods and assert the responses
    username = khoros_object.users.get_username(user_id=user_id)
    assert username == 'joeCustomer'
    username = khoros_object.users.get_login(user_id=user_id)
    assert username == 'joeCustomer'
    username = khoros_object.users.get_username(email=email)
    assert username == 'joeCustomer'


def test_users_table_query(monkeypatch):
    """This function tests the ability to query the users table.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'get', resources.mock_success_post)

    response = khoros_object.users.query_users_table_by_id('login', 216)
    assert response.get('status') == 'success'


# Import the exceptions modules
exceptions = resources.import_modules('khoros.errors.exceptions')
