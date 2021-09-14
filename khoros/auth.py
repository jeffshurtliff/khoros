# -*- coding: utf-8 -*-
"""
:Module:            khoros.auth
:Synopsis:          This module handles authentication-related tasks and operations for the Khoros Community APIs
:Usage:             ``import khoros.auth``
:Example:           ``session_key = khoros.auth(KhorosObject)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Aug 2021
"""

import requests
from defusedxml import ElementTree

from . import api, errors
from .utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_session_key(khoros_object, username=None, password=None):
    """This function retrieves the session key for an authentication session.

    .. versionchanged:: 4.2.0
       The URI is now generated utilizing the :py:func:`khoros.auth._get_khoros_login_url` function.

    .. versionchanged:: 3.5.0
       This function can now be used to authenticate secondary users with either a username and password or with
       only a username if calling the function with a previously authenticated user with Administrator privileges.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    .. versionchanged:: 3.3.0
       Updated ``khoros_object._settings`` to be ``khoros_object.core_settings``.

    .. versionchanged:: 2.7.4
       The HTTP headers were changed to be all lowercase in order to be standardized across the library.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param username: The username (i.e. login) of a secondary user to authenticate *(optional)*
    :type username:  str, None
    :param password: The password of a secondary user to authentication *(optional)*
    :returns: The session key in string format
    :raises: :py:exc:`khoros.errors.exceptions.SessionAuthenticationError`
    """
    # Prepare the API call
    password = khoros_object.core_settings['session_auth']['password'] if not username else password
    username = khoros_object.core_settings['session_auth']['username'] if not username else username
    payload = _get_session_key_payload(username, password)
    query_string = core_utils.encode_query_string(payload)

    # Determine if TLS certificates should be verified during API calls
    verify = api.should_verify_tls(khoros_object)

    # Perform the API call to authorize the session
    uri = f'{_get_khoros_login_url(khoros_object)}/?{query_string}'
    secondary_user = False if password else True
    header = _get_session_key_header(khoros_object, secondary_user)
    response = requests.post(uri, headers=header, verify=verify)
    if response.status_code != 200:
        if type(response.text) == str and response.text.startswith('<html>'):
            api_error = errors.handlers.get_error_from_html(response.text)
            error_msg = f"The authentication attempt failed with the following error:\n\t{api_error}"
            raise errors.exceptions.SessionAuthenticationError(error_msg)
        raise errors.exceptions.SessionAuthenticationError()
    else:
        response = response.json()
        try:
            session_key = response['response']['value']['$']
        except KeyError:
            raise errors.exceptions.SessionAuthenticationError(f"Failed to retrieve a session key for '{username}'")
    return session_key


def get_sso_key(khoros_object):
    """This function retrieves the session key for a LithiumSSO session.

    .. versionadded:: 4.2.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The session key in string format
    :raises: :py:exc:`khoros.errors.exceptions.SsoAuthenticationError`
    """
    khoros_login_url = _get_khoros_login_url(khoros_object)
    headers = _get_session_key_header(khoros_object)

    response = requests.post(
        khoros_login_url,
        headers=headers,
        data=khoros_object.core_settings.get('sso')
    )
    tree = ElementTree.fromstring(response.text)
    if 'status' in tree.attrib:
        if tree.attrib['status'] == 'success':
            return tree.findtext('value')
    raise errors.exceptions.SsoAuthenticationError('Failed to retrieve a session key with the LithiumSSO token.')


def _get_khoros_login_url(khoros_object):
    """This function returns the URL for the Khoros login endpoint.

    .. versionadded:: 4.2.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The URL string
    """
    community_url = khoros_object.core_settings.get('community_url')
    return f'{community_url}/restapi/vc/authentication/sessions/login'


def _get_session_key_payload(_username, _password=None, _return_json=True):
    """This function constructs the payload used to request a session key.

    .. versionadded:: 3.5.0

    :param _username: The username (i.e. login) for the user being authenticated
    :type _username: str
    :param _password: The password for the user being authenticated

                      .. note:: A password is not required if authenticating a secondary user with a previously
                                authenticated Administrator account.

    :type _password: str, None
    :param _return_json: Determines if the session key should be returned in JSON format (``True`` by default)
    :type _return_json: bool
    :returns: A dictionary with the authentication request payload
    """
    _auth_payload = {'user.login': _username}
    if _password:
        _auth_payload.update({'user.password': _password})
    if _return_json:
        _auth_payload.update({'restapi.response_format': 'json'})
    return _auth_payload


def _get_session_key_header(_khoros_object, _secondary=False):
    """This function retrieves the header for an API call to retrieve a session key.

    .. versionadded:: 3.5.0

    :param _khoros_object: The core Khoros object
    :type _khoros_object: class[khoros.Khoros]
    :param _secondary: Indicates that the authentication request is for a secondary user (``False`` by default)
    :returns: A dictionary with the header information
    :raises: :py:exc:`khoros.errors.exceptions.SessionAuthenticationError`
    """
    _header = {"content-type": "application/x-www-form-urlencoded"}
    if _secondary:
        if _khoros_object.auth.get('header'):
            _header.update(_khoros_object.auth.get('header'))
        else:
            _error_msg = "Unable to retrieve a session key for secondary users without an existing session key"
            raise errors.exceptions.SessionAuthenticationError(_error_msg)
    return _header


def get_session_header(session_key):
    """This function constructs and returns a proper API header containing the session key for authorization.

    :param session_key: The session key for the authorization session
    :type session_key: str
    :returns: The API in dictionary format
    """
    return {'li-api-session-key': session_key}


def invalidate_session(khoros_object, user_id=None, sso_id=None):
    """This function invalidates an active authentication session.

    .. versionchanged:: 3.3.0
       Updated ``khoros_object._settings`` to be ``khoros_object.core_settings``.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID of the service account (Lithium Registration)
    :type user_id: str, int, None
    :param sso_id: The SSO ID of the service account (Single Sign-On)
    :type sso_id: str, int, None
    :returns: Boolean value defining if the session was invalidated successfully
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    session_terminated = False
    payload = {}
    if sso_id:
        payload['sso_id'] = sso_id
    elif user_id:
        payload['id'] = user_id
    else:
        username = khoros_object.core_settings['session_auth']['username']
        user_id = khoros_object.search('id', 'users', f'login = "{username}"')
        user_id = user_id['data']['items'][0]['id']
        payload['id'] = user_id
    query_url = f"{khoros_object.core_settings['v2_base']}/auth/signout"
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

    .. versionchanged:: 3.3.0
       Updated ``khoros_object._settings`` to be ``khoros_object.core_settings``.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The properly encoded authorization URL in string format
    """
    community_url = khoros_object.core_settings['community_url']
    query_string = core_utils.encode_query_string({
        'client_id': khoros_object.core_settings['oauth2']['client_id'],
        'redirect_uri': khoros_object.core_settings['oauth2']['redirect_url'],
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
