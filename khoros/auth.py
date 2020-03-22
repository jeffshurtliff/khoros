# -*- coding: utf-8 -*-
"""
:Module:            khoros.auth
:Synopsis:          This module handles authentication-related tasks and operations for the Khoros Community APIs
:Usage:             ``import khoros.auth``
:Example:           ``session_key = khoros.auth(KhorosObject)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Mar 2020
"""

import requests

from . import api, errors
from .utils import core_utils


def get_session_key(khoros_object):
    """This function retrieves the session key for an authentication session.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The session key in string format
    """
    community_url = khoros_object._settings['community_url']
    username = khoros_object._settings['session_auth']['username']
    password = khoros_object._settings['session_auth']['password']
    query_string = core_utils.encode_query_string({
        'user.login': username,
        'user.password': password,
        'restapi.response_format': 'json'
    })
    uri = f"{community_url}/restapi/vc/authentication/sessions/login/?{query_string}"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(uri, headers=header)
    if response.status_code != 200:
        if type(response.text) == str and response.text.startswith('<html>'):
            api_error = errors.handlers.get_error_from_html(response.text)
            error_msg = f"The authentication attempt failed with the following error:\n\t{api_error}"
            raise errors.exceptions.SessionAuthenticationError(error_msg)
        raise errors.exceptions.SessionAuthenticationError
    else:
        response = response.json()
        session_key = response['response']['value']['$']
    return session_key


def get_session_header(session_key):
    """This function constructs and returns a proper API header containing the session key for authorization.

    :param session_key: The session key for the authorization session
    :type session_key: str
    :returns: The API in dictionary format
    """
    return {'li-api-session-key': session_key}


def invalidate_session(khoros_object, user_id=None, sso_id=None):
    """This function invalidates an active authentication session.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID of the service account (Lithium Registration)
    :type user_id: str, int, NoneType
    :param sso_id: The SSO ID of the service account (Single Sign-On)
    :type sso_id: str, int, NoneType
    :returns: Boolean value defining if the session was invalidated successfully
    """
    session_terminated = False
    payload = {}
    if sso_id:
        payload['sso_id'] = sso_id
    elif user_id:
        payload['id'] = user_id
    else:
        username = khoros_object._settings['session_auth']['username']
        user_id = khoros_object.search('id', 'users', f'login = "{username}"')
        user_id = user_id['data']['items'][0]['id']
        payload['id'] = user_id
    query_url = f"{khoros_object._settings['v2_base']}/auth/signout"
    headers = {'content-type': 'application/json'}
    response = api.post_request_with_retries(query_url, payload, return_json=True,
                                             auth_dict=khoros_object.auth, headers=headers)
    if response['status'] == "success":
        if response['data']['signed_off_all_sessions'] is True:
            session_terminated = True
            print("The authentication session has been terminated.\n")
    return session_terminated


def get_oauth_authorization_url(khoros_object):
    """This function constructs the authorization URL needed for the OAuth 2.0 Web Application Flow.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The properly encoded authorization URL in string format
    """
    community_url = khoros_object._settings['community_url']
    query_string = core_utils.encode_query_string({
        'client_id': khoros_object._settings['oauth2']['client_id'],
        'redirect_uri': khoros_object._settings['oauth2']['redirect_url'],
        'response_type': 'code',
        'state': core_utils.get_random_string()
    }, no_encode='redirect_uri')
    authorization_url = f"{community_url}/auth/oauth2/authorize?{query_string}"
    return authorization_url


def get_oauth_callback_url_from_user(khoros_object):
    """This function instructs the end-user to visit the authorization URL and provide the full callback URL.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The callback URL supplied by the end-user
    """
    authorization_url = get_oauth_authorization_url(khoros_object)
    print("Please visit this URL to authorize access: ", authorization_url)
    callback_url = input("Enter the full URL in the address bar after visiting the URL above: ")
    if not callback_url.startswith('http'):
        raise errors.exceptions.InvalidCallbackURLError(val=callback_url)
    return callback_url
