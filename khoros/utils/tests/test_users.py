# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_users
:Synopsis:          This module is used by pytest to verify that the ``users`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

import os
import sys

import pytest
import requests

from . import resources

# Define a global variable to define when the package path has been set
package_path_defined = False

# Define constants
USER_ID = 216
USERNAME = 'joeCustomer'


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
        khoros_object.users.update_sso_id('abcdEFGH', user_login=USERNAME)


def test_get_user_identifiers():
    """This function tests the ability to retrieve the identifiers for a user.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Retrieve the User ID and assert the response was expected
    user_id = khoros_object.users.get_user_id(login=USERNAME)
    assert isinstance(user_id, int) and user_id > 0
    # TODO: Troubleshoot why the test below fails with a LiQL invalid query syntax error
    # user_id = khoros_object.users.get_user_id(first_name='Joe', last_name='Customer')
    # assert isinstance(user_id, int) and user_id > 0

    # Retrieve the email address through various methods and assert the response was expected
    email = khoros_object.users.get_email(user_id=user_id)
    assert isinstance(email, str) and '@' in email
    email = khoros_object.users.get_email(login=USERNAME)
    assert isinstance(email, str) and '@' in email

    # Retrieve the User ID using email and assert the response was expected
    user_id = khoros_object.users.get_user_id(email=email)
    assert isinstance(user_id, int) and user_id > 0

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

    response = khoros_object.users.query_users_table_by_id('login', USER_ID)
    assert response.get('status') == 'success'
    response = khoros_object.users.query_users_table_by_id(['login', 'email'], USER_ID)
    assert response.get('status') == 'success'


def test_get_counts():
    """This function tests the various functions that involve retrieving user-related counts.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Test retrieving the album count and verifying the response
    album_count = khoros_object.users.get_album_count(user_id=USER_ID)
    assert isinstance(album_count, int) and album_count >= 0

    # Test retrieving the follower count and verifying the response
    followers_count = khoros_object.users.get_followers_count(user_id=USER_ID)
    assert isinstance(followers_count, int) and followers_count >= 0

    # Test retrieving the following count and verifying the response
    following_count = khoros_object.users.get_following_count(user_id=USER_ID)
    assert isinstance(following_count, int) and following_count >= 0

    # Test retrieving the images count and verifying the response
    image_count = khoros_object.users.get_images_count(user_id=USER_ID)
    assert isinstance(image_count, int) and image_count >= 0
    image_count = khoros_object.users.get_public_images_count(user_id=USER_ID)
    assert isinstance(image_count, int) and image_count >= 0

    # Test retrieving the messages count and verifying the response
    msg_count = khoros_object.users.get_messages_count(user_id=USER_ID)
    assert isinstance(msg_count, int) and msg_count >= 0

    # Test retrieving the roles count and verifying the response
    roles_count = khoros_object.users.get_roles_count(user_id=USER_ID)
    assert isinstance(roles_count, int) and roles_count >= 0

    # Test retrieving the authored solutions count and verifying the response
    solutions_count = khoros_object.users.get_solutions_authored_count(user_id=USER_ID)
    assert isinstance(solutions_count, int) and solutions_count >= 0

    # Test retrieving the posted topics count and verifying the response
    topics_count = khoros_object.users.get_topics_count(user_id=USER_ID)
    assert isinstance(topics_count, int) and topics_count >= 0

    # Test retrieving the posted replies count and verifying the response
    # TODO: Troubleshoot why the response below returns TypeError: list indices must be integers or slices, not str
    # replies_count = khoros_object.users.get_replies_count(user_id=USER_ID)
    # assert isinstance(replies_count, int) and replies_count >= 0

    # Test retrieving the posted videos count and verifying the response
    videos_count = khoros_object.users.get_videos_count(user_id=USER_ID)
    assert isinstance(videos_count, int) and videos_count >= 0

    # Test retrieving the kudos given count and verifying the response
    kudos_given_count = khoros_object.users.get_kudos_given_count(user_id=USER_ID)
    assert isinstance(kudos_given_count, int) and kudos_given_count >= 0

    # Test retrieving the kudos given count and verifying the response
    kudos_received_count = khoros_object.users.get_kudos_received_count(user_id=USER_ID)
    assert isinstance(kudos_received_count, int) and kudos_received_count >= 0

    # Test retrieving the online users count
    online_users_count = khoros_object.users.get_online_user_count()
    assert isinstance(online_users_count, int)


# Import the exceptions modules
exceptions = resources.import_modules('khoros.errors.exceptions')
