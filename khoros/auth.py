# -*- coding: utf-8 -*-
"""
:Module:            khoros.auth
:Synopsis:          This module handles authentication-related tasks and operations for the Khoros Community APIs
:Usage:             ``import khoros.auth``
:Example:           ``session_key = khoros.auth(KhorosObject)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Feb 2020
"""

import requests

from . import errors
from .utils import core_utils


def get_session_key(khoros_object):
    """This function retrieves the session key for an authentication session.

    :param khoros_object: The core Khoros object
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
