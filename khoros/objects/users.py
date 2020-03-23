# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.users
:Synopsis:          This module includes functions that handle user-related operations.
:Usage:             ``from khoros.objects import users``
:Example:           ``users.create(khoros_object, username='john_doe', email='john.doe@example.com')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Mar 2020
"""

from .. import api, errors


def create(khoros_object, params=None, username=None, email=None, password=None, first_name=None, last_name=None,
           biography=None, sso_id=None, web_page_url=None, cover_image=None):
    """This function creates a new user in the Khoros Community environment.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param params: Allows all parameters to be passed to the function within a single dictionary
    :type params: dict, NoneType
    :param username: The username (i.e. ``login``) for the user (**required**)
    :type username: str, NoneType
    :param email: The email address for the user (**required**)
    :type email: str, NoneType
    :param password: The password for the user
    :type password: str, NoneType
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, NoneType
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, NoneType
    :param biography: The user's biography for their profile
    :type biography: str, NoneType
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, NoneType
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, NoneType
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, NoneType
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.UserCreationError`
    """
    # TODO: Add functionality for followers, following, rank, roles, user_avatar and user_badges
    payload = structure_payload(params, username, email, password, first_name, last_name, biography, sso_id,
                                web_page_url, cover_image)
    query_url = f"{khoros_object._settings['v2_base']}/users"
    headers = {'Content-Type': 'application/json'}
    response = api.post_request_with_retries(query_url, payload, auth_dict=khoros_object.auth, headers=headers)
    if not api.query_successful(response):
        raise errors.exceptions.UserCreationError(user=payload['login'], exc_msg=response['message'])
    return


def structure_payload(params=None, username=None, email=None, password=None, first_name=None, last_name=None,
                      biography=None, sso_id=None, web_page_url=None, cover_image=None):
    """This function properly structures the payload to be passed when creating or manipulating users via the API.

    :param params: Allows all parameters to be passed to the function within a single dictionary
    :type params: dict, NoneType
    :param username: The username (i.e. ``login``) for the user (**required**)
    :type username: str, NoneType
    :param email: The email address for the user (**required**)
    :type email: str, NoneType
    :param password: The password for the user
    :type password: str, NoneType
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, NoneType
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, NoneType
    :param biography: The user's biography for their profile
    :type biography: str, NoneType
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, NoneType
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, NoneType
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, NoneType
    :returns: The properly formatted payload within a dictionary
    """
    payload_mapping = {
        'biography': biography,
        'cover_image': cover_image,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'login': username,
        'password': password,
        'sso_id': sso_id,
        'web_page_url': web_page_url
    }
    payload = {}
    if params:
        payload.update(params)
    for field_name, field_value in payload_mapping.items():
        if payload_mapping[field_name]:
            payload[field_name] = field_value
    payload = {'data': payload}
    return payload


def delete(khoros_object, user_id, return_json=False):
    """This function deletes a user from the Khoros Community environment.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID of the user to be deleted
    :type user_id: str, int
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response (optionally in JSON format)
    """
    query_url = f"{khoros_object._settings['v2_base']}/users/{user_id}"
    return api.delete(query_url, return_json, auth_dict=khoros_object.auth)
