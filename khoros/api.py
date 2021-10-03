# -*- coding: utf-8 -*-
"""
:Module:            khoros.api
:Synopsis:          This module handles interactions with the Khoros Community REST APIs
:Usage:             ``import khoros.api``
:Example:           ``json_response = khoros.api.get_request_with_retries(url, auth_dict=khoros.auth)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Oct 2021
"""

import json
import os.path
import warnings
import importlib

import urllib3
import requests

from . import errors
from .utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

# Define global variable to determine if SSL verification has been disabled
ssl_verify_disabled = None

# Define global variable to determine if suppressed message warning has been displayed
ssl_warning_shown = False


def define_headers(khoros_object=None, auth_dict=None, params=None, accept=None, content_type=None, multipart=False,
                   default_content_type=False, proxy_user_object=None):
    """This function defines the headers to use in an API call.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionchanged:: 3.5.0
       An unnecessary ``else`` statement after the :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
       exception is raised has been removed.

    .. versionchanged:: 2.7.5
       Added the ``default_content_type`` argument which is defined as ``False`` by default.

    .. versionchanged:: 2.7.4
       The HTTP headers were changed to be all lowercase in order to be standardized across the library.
       A function call for :py:func:`khoros.api._normalize_headers` was also introduced.

    .. versionchanged:: 2.3.0
       Added the ``multipart`` Boolean argument to remove the ``content-type`` key value pair when appropriate.

    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param params: Header parameters in a dictionary format
    :type params: dict, None
    :param accept: The ``accept`` header value (e.g. ``application/json``)
    :type accept: str, None
    :param content_type: The ``content-type`` header value (e.g. ``application/json``)
    :type content_type: str, None
    :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
    :type multipart: bool
    :param default_content_type: Determines if ``application/json`` should be used as the default ``content-type``
                                 value if the key does not exist (``False`` by default)
    :type default_content_type: bool
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: A dictionary with the header fields and associated values
    :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
    """
    if not khoros_object and not auth_dict and not proxy_user_object:
        raise errors.exceptions.MissingAuthDataError()
    if proxy_user_object:
        headers = proxy_user_object.session_header
    elif auth_dict:
        headers = auth_dict['header']
    else:
        headers = khoros_object.auth['header']
    if 'content-type' not in headers and default_content_type:
        headers['content-type'] = 'application/json'
    if params:
        headers.update(params)
    if accept:
        headers['accept'] = accept
    if content_type:
        headers['content-type'] = content_type
    if multipart and 'content-type' in headers:
        del headers['content-type']
    headers = _normalize_headers(headers)
    return headers


def _normalize_headers(_headers):
    """This function normalizes the HTTP headers to ensure that the keys and values are all lowercase.

    .. versionchanged:: 2.7.5
       The function was updated to ensure that authentication/authorization tokens would not be altered.

    .. versionadded:: 2.7.4

    :param _headers: The headers dictionary
    :type  _headers: dict
    :returns: The normalized headers dictionary
    """
    _normalized_headers = {}
    _auth_keys = ['li-api-session-key', 'authorization']
    for _header_key, _header_value in _headers.items():
        if _header_key.lower() in _auth_keys:
            _normalized_headers[_header_key] = _header_value
        elif isinstance(_header_value, str):
            _normalized_headers[_header_key.lower()] = _header_value.lower()
        elif any((isinstance(_header_value, list), isinstance(_header_value, tuple))):
            _new_iterable = []
            for _inner_value in _header_value:
                _inner_value = _inner_value.lower() if isinstance(_inner_value, str) else _inner_value
                _new_iterable.append(_inner_value)
            _new_iterable = tuple(_new_iterable) if isinstance(_header_value, tuple) else _new_iterable
            _normalized_headers[_header_key.lower()] = _new_iterable
        else:
            _header_key = _header_key.lower() if isinstance(_header_key, str) else _header_key
            _normalized_headers[_header_key] = _header_value
    return _normalized_headers


def _get_json_query_string(_return_json, _include_ampersand_prefix=True):
    """This function constructs a query string for a Community API v1 query that should return JSON responses.

    :param _return_json: Indicates whether or not API responses should be in JSON format
    :type _return_json: bool
    :param _include_ampersand_prefix: Determines if an ampersand (``&``) prefix should be included in the string
    :type _include_ampersand_prefix: bool
    :returns: The formatted query string
    """
    _query_strings = {True: 'restapi.response_format=json', False: ''}
    _prefixes = {True: '&', False: ''}
    _query_string = ''
    if _return_json:
        _query_string = f"{_prefixes.get(_include_ampersand_prefix)}{_query_strings.get(_return_json)}"
    return _query_string


def _add_json_query_to_uri(_uri, _return_json=True):
    """This function appends the v1 query parameter to return a JSON response when appropriate.

    .. versionadded:: 4.0.0

    .. note:: No action will be taken if the URI is not recognized as a Community API v1 URI.

    :param _uri: The current URI against which the REST API call will be made
    :type _uri: str
    :param _return_json: Indicates whether or not the response should be in JSON format (``True`` by default)
    :type _return_json: bool
    :returns: The URI either untouched or with the added query parameter string where appropriate
    :raises: :py:exc:`TypeError`
    """
    if 'restapi/vc' in _uri and 'restapi.response_format' not in _uri and _return_json:
        _has_queries = True if '?' in _uri else False
        _uri = f"{_uri}?" if '?' not in _uri else _uri
        _uri = f"{_uri}{_get_json_query_string(_return_json, _has_queries)}"
    return _uri


def _display_ssl_verify_warning():
    """This function displays a warning if SSL verification has been disabled.

    .. versionadded:: 4.3.0

    :returns: None
    """
    global ssl_warning_shown
    if ssl_warning_shown is False:
        # Warn that SSL warnings are being suppressed
        warnings.warn('SSL certificate verification has been explicitly disabled and warnings '
                      'will be suppressed')
        ssl_warning_shown = True

        # Suppress warnings when performing API calls without verifying SSL certificates
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return


def should_verify_tls(khoros_object=None):
    """This function determines whether or not to verify the server's TLS certificate. (``True`` by default)

    .. versionchanged:: 4.3.0
       Introduced the ``ssl_verify_disabled`` global variable to allow this check to be performed even when the
       core object is not passed to the function.

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros], None
    :returns: Boolean value indicating if the verification should occur
    """
    global ssl_warning_shown, ssl_verify_disabled
    verify = None
    if khoros_object is not None and 'ssl_verify' in khoros_object.core_settings:
        verify = khoros_object.core_settings.get('ssl_verify')
        if verify is False:
            _display_ssl_verify_warning()
    elif ssl_verify_disabled is True:
        verify = False
        _display_ssl_verify_warning()
    verify = True if verify is None else verify
    if ssl_verify_disabled is None:
        ssl_verify_disabled = True if verify is False else False
    return verify


def get_request_with_retries(query_url, return_json=True, khoros_object=None, auth_dict=None, headers=None,
                             verify=None, proxy_user_object=None):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.
       A function call was also introduced to ensure that v1 requests that should return JSON responses are formatted
       correctly.

    .. versionchanged:: 3.4.0
       Removed an unnecessary ``pass`` statement and initially defined the ``response`` variable with a ``NoneType``
       value to prevent a linting error from being reported. Also leveraged the ``ssl_verify`` core setting.

    .. versionchanged:: 2.5.0
       Leverages new private functions and has improved error handling of JSON conversion attempts.

    :param query_url: The URI to be queried
    :type query_url: str
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response from the GET request (optionally in JSON format)
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers,
                             proxy_user_object=proxy_user_object)
    verify = should_verify_tls(khoros_object) if verify is None else verify
    query_url = _add_json_query_to_uri(query_url, return_json)
    retries, response = 0, None
    while retries <= 5:
        try:
            response = requests.get(query_url, headers=headers, verify=verify)
            break
        except Exception as exc_msg:
            _report_failed_attempt(exc_msg, 'get', retries)
            retries += 1
    if retries == 6:
        _raise_exception_for_repeated_timeouts()
    return _attempt_json_conversion(response, return_json)


def _is_plaintext_payload(_headers, _payload=None):
    """This function checks to determine whether or not the payload for an API is in JSON or plaintext format.

    .. versionadded:: 3.1.0

    :param _headers: The headers associated with the API call
    :type _headers: dict
    :param _payload: The payload to be delivered in the API call
    :type _payload: dict, str
    :returns: Boolean value indicating whether or not the payload is plaintext
    :raises: :py:exc:`ValueError`
    """
    _is_plaintext = False
    if ('content-type' in _headers and _headers.get('content-type') == 'text/plain') or isinstance(_payload, str):
        _is_plaintext = True
    return _is_plaintext


def _api_request_with_payload(_url, _payload=None, _request_type='post', _headers=None, _multipart=False, _verify=None,
                              _khoros_object=None):
    """This function performs an API request while supplying a JSON payload.

    .. versionchanged:: 4.3.0
       An issue has been fixed that prevented SSL verification from being disabled by the helper file setting.

    .. versionchanged:: 3.5.0
       Removed the unnecessary ``pass`` statement.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``verify`` parameter to determine if SSL certificate verification is needed.

    .. versionchanged:: 3.1.0
       The function now supports plaintext payloads.

    .. versionchanged:: 2.5.0
       The function can now be called without supplying a JSON payload.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param _url: The URI to be queried
    :type _url: str
    :param _payload: The payload that accompanies the API call
    :type _payload: dict, str, None
    :param _request_type: Define the type of API call (e.g. ``get``, ``post`` or ``put``)
    :type _request_type: str
    :param _headers: Any predefined headers to be passed with the API call (optional)
    :type _headers: dict
    :param _multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
    :type _multipart: bool
    :param _verify: Determines whether or not to verify the server's TLS certificate (``None`` by default)
    :type _verify: bool
    :param _khoros_object: The core Khoros object
    :type _khoros_object: class[khoros.Khoros], None
    :returns: The API response
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    _headers = {} if not _headers else _headers
    _verify = should_verify_tls(_khoros_object) if _verify is None else _verify
    _retries, _response = 0, None
    if not _payload:
        _response = _api_request_without_payload(_url, _request_type, _headers)
    else:
        _is_plaintext = _is_plaintext_payload(_headers, _payload)
        while _retries <= 5:
            try:
                if _request_type.lower() == "put":
                    if _multipart:
                        _response = requests.put(_url, files=_payload, headers=_headers, verify=_verify)
                    else:
                        _payload = json.dumps(_payload, default=str) if not _is_plaintext else _payload
                        _response = requests.put(_url, data=_payload, headers=_headers, verify=_verify)
                elif _request_type.lower() == "post":
                    if _multipart:
                        _response = requests.post(_url, files=_payload, headers=_headers, verify=_verify)
                    else:
                        _payload = json.dumps(_payload, default=str) if not _is_plaintext else _payload
                        _response = requests.post(_url, data=_payload, headers=_headers, verify=_verify)
                else:
                    raise errors.exceptions.InvalidRequestTypeError()
                break
            except Exception as _exc_msg:
                _report_failed_attempt(_exc_msg, _request_type, _retries)
                _retries += 1
        if _retries == 6:
            _raise_exception_for_repeated_timeouts()
    return _response


def _api_request_without_payload(_url, _request_type, _headers, _verify=None, _khoros_object=None):
    """This function performs a ``POST`` or ``PUT`` request without an accompanying JSON payload.

    .. versionchanged:: 4.3.0
       An issue has been fixed that prevented SSL verification from being disabled by the helper file setting.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``_verify`` parameter to determine if SSL certificate verification is needed.

    :param _url: The URL for the API request
    :type _url: str
    :param _request_type: The request type (e.g. ``post`` or ``put``)
    :type _request_type: str
    :param _headers: The headers associated with the API request
    :type _headers: dict
    :param _verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type _verify: bool
    :param _khoros_object: The core Khoros object
    :type _khoros_object: class[khoros.Khoros], None
    :returns: The API response
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    _verify = should_verify_tls(_khoros_object) if _verify is None else _verify
    _retries, _response = 0, None
    while _retries <= 5:
        try:
            if _request_type.lower() == "post":
                _response = requests.post(_url, headers=_headers, verify=_verify)
            elif _request_type.lower() == "put":
                _response = requests.put(_url, headers=_headers, verify=_verify)
            else:
                raise errors.exceptions.InvalidRequestTypeError()
            break
        except Exception as _exc_msg:
            _report_failed_attempt(_exc_msg, _request_type, _retries)
            _retries += 1
    if _retries == 6:
        _raise_exception_for_repeated_timeouts()
    return _response


def combine_json_and_avatar_payload(json_payload, avatar_image_path):
    """This function combines JSON payload with an uploaded avatar image (binary file) for a multipart API request.

    .. versionadded:: 2.6.0

    :param json_payload: The JSON payload for the API request
    :type json_payload: dict
    :param avatar_image_path: The full path to the avatar image to use
    :type avatar_image_path: str
    :returns: The full multipart payload for the API request
    :raises: :py:exc:`FileNotFoundError`
    """
    files_payload = format_avatar_payload(avatar_image_path)
    full_payload = {'api.request': (None, json.dumps(json_payload, default=str), 'application/json')}
    full_payload.update(files_payload)
    return full_payload


def format_avatar_payload(avatar_image_path):
    """This function structures and formats the avatar payload to be used in a multipart API request.

    .. versionadded:: 2.6.0

    :param avatar_image_path: The file path to the avatar image to use
    :type avatar_image_path: str
    :returns: The payload dictionary containing the binary file
    :raises: :py:exc:`FileNotFoundError`
    """
    return {'avatar': (f'{os.path.basename(avatar_image_path)}', open(avatar_image_path, 'rb'))}


def _report_failed_attempt(_exc_msg, _request_type, _retries):
    """This function reports a failed API call that will be retried.

    :param _exc_msg: The exception that was raised can captured within a try/except clause
    :param _request_type: The type of API request (e.g. ``post``, ``put`` or ``get``)
    :type _request_type: str
    :param _retries: The attempt number for the API request
    :type _retries: int
    :returns: None
    """
    _exc_name = type(_exc_msg).__name__
    if 'connect' not in _exc_name.lower():
        raise Exception(f"{_exc_name}: {_exc_msg}")
    _current_attempt = f"(Attempt {_retries} of 5)"
    _error_msg = f"The {_request_type.upper()} request has failed with the following exception: " + \
                 f"{_exc_name}: {_exc_msg} {_current_attempt}"
    errors.handlers.eprint(f"{_error_msg}\n{_exc_name}: {_exc_msg}\n")
    return


def _raise_exception_for_repeated_timeouts():
    """This function raises an exception when all API attempts (including) retries resulted in a timeout.

    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    _failure_msg = "The script was unable to complete successfully after five consecutive API timeouts. " + \
                   "Please run the script again or contact Khoros Support for further assistance."
    raise errors.exceptions.APIConnectionError(_failure_msg)


def payload_request_with_retries(url, request_type, json_payload=None, plaintext_payload=None, url_encoded_payload=None,
                                 return_json=True, khoros_object=None, auth_dict=None, headers=None, multipart=False,
                                 content_type=None, verify=None, proxy_user_object=None):
    """This function performs an API request that includes a payload with up to three reties as necessary.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    .. versionchanged:: 3.2.0
       Support has been introduced for URL-encoded string payloads in POST and PUT requests.

    :param url: The URI to be queried
    :type url: str
    :param request_type: Defines the API call as a ``POST`` or ``PUT`` request
    :type request_type: str
    :param json_payload: The payload for the POST or PUT request in JSON format
    :type json_payload: dict, None
    :param plaintext_payload: The payload for the POST or PUT request in plaintext (i.e. ``text/plain``) format
    :type plaintext_payload: str, None
    :param url_encoded_payload: The payload for the POST or PUT request as a URL-encoded string
    :type url_encoded_payload: str, None
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, None
    :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
    :type multipart: bool
    :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                         .. note:: If this parameter is not defined then the content type will be identified based
                                   on the payload format and/or type of request.

    :type content_type: str, None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response from the API request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    # Ensure that the request type is valid
    valid_request_types = ['post', 'put']
    request_type = request_type.lower()
    if request_type not in valid_request_types:
        raise errors.exceptions.InvalidRequestTypeError()

    # Determine if TLS certificates should be verified during API calls
    verify = should_verify_tls(khoros_object) if verify is None else verify

    # Construct the appropriate headers for the POST call
    if content_type:
        headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers, multipart=multipart,
                                 content_type=content_type.lower(), proxy_user_object=proxy_user_object)
    elif plaintext_payload and not json_payload:
        multipart = False
        headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers, multipart=multipart,
                                 content_type='text/plain', proxy_user_object=proxy_user_object)
    else:
        headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers, multipart=multipart,
                                 proxy_user_object=proxy_user_object)

    # Perform the API call and retrieve the response
    if any((plaintext_payload, url_encoded_payload, json_payload)):
        if any((plaintext_payload, url_encoded_payload)) and not json_payload:
            if plaintext_payload and not url_encoded_payload:
                payload = plaintext_payload
            elif url_encoded_payload and not plaintext_payload:
                payload = url_encoded_payload
            else:
                raise errors.exceptions.PayloadMismatchError(request_type=request_type.upper())
        elif json_payload and not any((plaintext_payload, url_encoded_payload)):
            payload = json_payload
        else:
            raise errors.exceptions.PayloadMismatchError(request_type=request_type.upper())
    else:
        payload = None
    response = _api_request_with_payload(url, payload, request_type, headers, multipart, verify)
    return _attempt_json_conversion(response, return_json)


def post_request_with_retries(url, json_payload=None, plaintext_payload=None, url_encoded_payload=None,
                              return_json=True, khoros_object=None, auth_dict=None, headers=None, multipart=False,
                              content_type=None, verify=None, proxy_user_object=None):
    """This function performs a POST request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.
       A function call was also introduced to ensure that v1 requests that should return JSON responses are formatted
       correctly.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    .. versionchanged:: 3.2.0
       Support has been introduced for URL-encoded string payloads in POST requests.

    .. versionchanged:: 3.1.1
       The ``content_type`` parameter now gets defined as an empty string prior to calling the sub-function.

    .. versionchanged:: 3.1.0
       The function can now accept plaintext payloads and now leverages the `:py:func:payload_request_with_retries`
       function. The ``content_type`` parameter has also been introduced.

    .. versionchanged:: 2.5.0
       The function can now be called without supplying a JSON payload.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the POST request in JSON format
    :type json_payload: dict, None
    :param plaintext_payload: The payload for the POST request in plaintext (i.e. ``text/plain``) format
    :type plaintext_payload: str, None
    :param url_encoded_payload: The payload for the POST request as a URL-encoded string
    :type url_encoded_payload: str, None
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, None
    :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
    :type multipart: bool
    :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                         .. note:: If this parameter is not defined then the content type will be identified based
                                   on the payload format and/or type of request.

    :type content_type: str, None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response from the POST request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    # Determine if TLS certificates should be verified during API calls
    verify = should_verify_tls(khoros_object) if verify is None else verify

    # Ensure the v1 URIs are formatted properly if the response must be in JSON format
    url = _add_json_query_to_uri(url, return_json)

    # Define the content type as necessary and perform the API call
    content_type = '' if not content_type else content_type
    return payload_request_with_retries(url, 'post', json_payload=json_payload, plaintext_payload=plaintext_payload,
                                        url_encoded_payload=url_encoded_payload, return_json=return_json,
                                        khoros_object=khoros_object, auth_dict=auth_dict, headers=headers,
                                        multipart=multipart, content_type=content_type.lower(), verify=verify,
                                        proxy_user_object=proxy_user_object)


def put_request_with_retries(url, json_payload=None, plaintext_payload=None, return_json=True, url_encoded_payload=None,
                             khoros_object=None, auth_dict=None, headers=None, multipart=False, content_type=None,
                             verify=None, proxy_user_object=None):
    """This function performs a PUT request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.
       A function call was also introduced to ensure that v1 requests that should return JSON responses are formatted
       correctly.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    .. versionchanged:: 3.2.0
       Support has been introduced for URL-encoded string payloads in PUT requests.

    .. versionchanged:: 3.1.1
       The ``content_type`` parameter now gets defined as an empty string prior to calling the sub-function.

    .. versionchanged:: 3.1.0
       The function can now accept plaintext payloads and now leverages the `:py:func:payload_request_with_retries`
       function. The ``content_type`` parameter has also been introduced.

    .. versionchanged:: 2.5.0
       The function can now be called without supplying a JSON payload.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the PUT request in JSON format
    :type json_payload: dict, None
    :param plaintext_payload: The payload for the POST request in plaintext (i.e. ``text/plain``) format
    :type plaintext_payload: str, None
    :param url_encoded_payload: The payload for the POST request as a URL-encoded string
    :type url_encoded_payload: str, None
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, None
    :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
    :type multipart: bool
    :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                         .. note:: If this parameter is not defined then the content type will be identified based
                                   on the payload format and/or type of request.

    :type content_type: str, None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response from the PUT request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    url = _add_json_query_to_uri(url, return_json)
    content_type = '' if not content_type else content_type
    return payload_request_with_retries(url, 'put', json_payload=json_payload, plaintext_payload=plaintext_payload,
                                        url_encoded_payload=url_encoded_payload, return_json=return_json,
                                        khoros_object=khoros_object, auth_dict=auth_dict, headers=headers,
                                        multipart=multipart, content_type=content_type.lower(), verify=verify,
                                        proxy_user_object=proxy_user_object)


def _attempt_json_conversion(_response, _return_json):
    """This function attempts to convert an API response to JSON if requested.

    .. versionadded:: 2.5.0

    :param _response: The API response to be converted
    :param _return_json: Indicates whether or not the API response should be converted
    :type _return_json: bool
    :returns: The API response that has been converted to JSON or in its original format if unable to convert
    """
    if _return_json and not isinstance(_response, dict):
        try:
            _response = _response.json()
        except Exception as _exc_msg:
            _exc_name = type(_exc_msg).__name__
            errors.handlers.eprint(f"Failed to convert to JSON due to the following exception: {_exc_name}: {_exc_msg}")
    return _response


def query_successful(api_response):
    """This function reviews the API response from the Community API to verify whether or not the call was successful.

    :param api_response: The response from the API in JSON format
    :type api_response: dict
    :returns: Boolean indicating whether or not the API call was successful
    """
    try:
        success_values = ['successful', 'success']
        successful = True if api_response['status'] in success_values else False
    except (KeyError, IndexError, ValueError, TypeError):
        successful = False
    return successful


def get_results_count(api_response):
    """This function returns the number of results within a response from the Community API.

    :param api_response: The response to an API query in JSON format
    :type api_response: dict
    :returns: The number of results in the API response as an integer
    """
    return api_response['data']['size']


def get_items_list(api_response):
    """This function returns the list of ``items`` dictionaries within a response from the Community API.

    :param api_response: The response to an API query in JSON format
    :type api_response: dict
    :returns: List of ``items`` dictionaries from the API response
    """
    return api_response['data']['items']


def delete(url, return_json=False, khoros_object=None, auth_dict=None, headers=None, proxy_user_object=None,
           verify=None):
    """This function performs a DELETE request against the Core API.

    .. versionchanged:: 4.3.0
       An issue has been fixed that prevented SSL verification from being disabled by the helper file setting.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    :param url: The URI against which the DELETE request will be issued
    :type url: str
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``False``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :returns: The API response from the DELETE request (optionally in JSON format)
    """
    # Determine if TLS certificates should be verified during API calls
    verify = should_verify_tls(khoros_object) if verify is None else verify

    # Perform the API call to delete the asset
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers,
                             proxy_user_object=proxy_user_object)
    response = requests.delete(url, headers=headers, verify=verify)
    if return_json:
        response = response.json()
    return response


def get_v1_node_collection(node_type):
    """This function retrieves the appropriate API v1 collection name for a given node type.

    .. versionchanged:: 4.0.0
       Group Hubs are now supported by the function by passing the ``grouphub`` or ``group hub`` string.

    .. versionadded:: 3.5.0

    :param node_type: The node type for which to retrieve the collection (e.g. ``board``, ``category``)
    :type node_type: str
    :returns: The associated API v2 collection for the node type
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    node_collections = {
        'board': 'boards',
        'category': 'categories',
        'grouphub': 'nodes/type/key/grouphub',
        'group hub': 'nodes/type/key/grouphub',
    }
    node_collection = node_type if node_type in node_collections.values() else ''
    if node_type not in node_collections:
        raise errors.exceptions.InvalidNodeTypeError(val=node_type)
    return node_collections.get(node_type) if not node_collection else node_collection


def get_v1_user_path(user_id=None, user_email=None, user_login=None, user_sso_id=None, user_and_type=None,
                     trailing_slash=False):
    """This function returns the segment of an API v1 endpoint that is the path to define a user.

    .. versionadded:: 4.0.0
       Introduced the ``user_and_type`` parameter that can be passed instead of a parameter for a specific type.

    .. versionadded:: 3.5.0

    :param user_id: The numeric User ID associated with a user
    :type user_id: str, int, None
    :param user_email: The email address associated with a user
    :type user_email: str, None
    :param user_login: The username (i.e. login) associated with a user
    :type user_login: str, None
    :param user_sso_id: The Single Sign-On (SSO) ID associated with a user
    :type user_sso_id: str, None
    :param user_and_type: A tuple with the first value being the user value and the second being the user type.
                          (Accepted types: ``id``, ``email``, ``login`` and ``sso_id``)
    :type user_and_type: tuple, None
    :param trailing_slash: Determines if the returned path should end with a slash (``False`` by default)
    :type trailing_slash: bool
    :returns: The API user path (e.g. ``/users/id/1234``)
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    # Parse the user_and_type parameter when present
    user_id = user_and_type[0] if user_and_type[1] == 'id' else user_id
    user_email = user_and_type[0] if user_and_type[1] == 'email' else user_email
    user_login = user_and_type[0] if user_and_type[1] == 'login' else user_login
    user_sso_id = user_and_type[0] if user_and_type[1] == 'sso_id' else user_sso_id

    # Validate the data and return the path
    if not any((user_id, user_email, user_login, user_sso_id)):
        raise errors.exceptions.MissingRequiredDataError("A user identifier must be provided")
    slash = '/' if trailing_slash else ''
    if user_email:
        user_path = f"/users/email/{user_email}{slash}"
    elif user_login:
        user_path = f"/users/login/{user_login}{slash}"
    elif user_sso_id:
        user_path = f"/users/sso_id/{user_sso_id}{slash}"
    else:
        user_path = f"/users/id/{user_id}{slash}"
    return user_path


def perform_v1_search(khoros_object, endpoint, filter_field, filter_value, return_json=False, fail_on_no_results=False,
                      proxy_user_object=None, verify=None):
    """This function performs a search for a particular field value using a Community API v1 call.

    .. versionchanged:: 4.3.0
       An issue has been fixed that prevented SSL verification from being disabled by the helper file setting.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionchanged:: 3.5.0
       The typecheck was updated to utilize ``isinstance()`` instead of ``type()``.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param endpoint: The API v1 endpoint against which to perform the search query
    :type endpoint: str
    :param filter_field: The name of the field being queried within the API v1 endpoint
    :type filter_field: str
    :param filter_value: The value associated with the field being queried
    :type filter_value: str, int
    :param return_json: Determines if the response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :param fail_on_no_results: Raises an exception if no results are returned (``False`` by default)
    :type fail_on_no_results: bool
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :returns: The API response (optionally in JSON format)
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    # Determine if TLS certificates should be verified during API calls
    verify = should_verify_tls(khoros_object) if verify is None else verify

    # Prepare the API call
    headers = define_headers(khoros_object, content_type='application/x-www-form-urlencoded',
                             proxy_user_object=proxy_user_object)
    if isinstance(filter_value, str):
        filter_value = core_utils.url_encode(filter_value)
    uri = f"{khoros_object.core['v1_base']}/search/{endpoint}?q={filter_field}:{filter_value}"
    uri = f"{uri}{_get_json_query_string(return_json)}"

    # Perform the API call
    response = requests.get(uri, headers=headers, verify=verify)
    if return_json:
        response = response.json()
        response = response['response'] if 'response' in response else response
    errors.handlers.verify_v1_response(response, 'get', 'users', fail_on_no_results)
    return response


def encode_multipart_data(data_fields):
    """This function uses the Streaming Multipart Data Encoder to encode the payload for a multipart/form-data API call.

    .. versionchanged:: 3.5.0
       This function now import the ``requests_toolbelt`` module locally to avoid dependency errors during installation.

    .. versionadded:: 2.3.0

    .. seealso:: This function follows the `requests_toolbelt <https://rsa.im/3dg7QiZ>`_ documentation.

    :param data_fields: A dictionary with the data to be encoded
    :type data_fields: dict
    :returns: The encoded data for use by the :py:mod:`requests` library
    """
    try:
        toolbelt_encoder = importlib.import_module('requests_toolbelt.multipart.encoder')
        multipart_data = toolbelt_encoder.MultipartEncoder(fields=data_fields)
    except ModuleNotFoundError:
        error_msg = "The 'requests_toolbelt' module is required to encode multipart data. " \
                    "Install with pip and try again."
        logger.error(error_msg)
        raise ModuleNotFoundError(error_msg)
    return multipart_data


def encode_payload_values(payload_dict):
    """This function URL-encoded any string-formatted payload values.

    .. versionadded:: 3.2.0

    :param payload_dict: The JSON payload for an API call in dictionary format
    :type payload_dict: dict
    :returns: The JSON payload with URL-encoded string values
    """
    encoded_payload = {}
    for field, value in payload_dict.items():
        if isinstance(value, str):
            encoded_payload[field] = core_utils.url_encode(value)
        else:
            encoded_payload[field] = value
    return encoded_payload


def encode_v1_query_string(query_dict, return_json=True, json_payload=False):
    """This function formats and URL-encodes a Community API v1 query string.

    .. versionchanged:: 3.2.0
       Introduced the ability to pass the query parameters as JSON payload to avoid URI length limits.

    .. versionadded:: 2.5.0

    :param query_dict: A dictionary with the query fields and associated values
    :type query_dict: dict
    :param return_json: Determines if JSON should be returned rather than XML (default: ``True``)
    :type return_json: bool
    :param json_payload: Determines if query parameters should be passed as JSON payload rather than in the URI
                         (``False`` by default)
    :type json_payload: bool
    :returns: The properly formatted and encoded query string
    """
    if return_json:
        query_dict['restapi.response_format'] = 'json'
    return core_utils.encode_query_string(query_dict, json_payload=json_payload)


def make_v1_request(khoros_object, endpoint, query_params=None, request_type='GET', return_json=True,
                    params_in_uri=False, json_payload=False, proxy_user_object=None, verify=None):
    """This function makes a Community API v1 request.

    .. versionchanged:: 4.3.0
       An issue has been fixed that prevented SSL verification from being disabled by the helper file setting.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionchanged:: 3.2.0
       Introduced the new default ability to pass the query parameters as payload to avoid URI length limits,
       and fixed an issue with GET requests not returning JSON responses even when requested.

    .. versionchanged:: 3.0.0
       The ``query_params`` argument has been updated to be optional and a full query string can now
       be passed within the ``endpoint`` argument.

    .. versionchanged:: 2.7.4
       The HTTP headers were changed to be all lowercase in order to be standardized across the library.

    .. versionchanged:: 2.7.1
       Fixed a syntax error in raising the the :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`
       exception class and removed unnecessary print debugging.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param endpoint: The API endpoint to be queried
    :type endpoint: str
    :param query_params: The field and associated values to be leveraged in the query string
    :type query_params: dict, None
    :param request_type: Determines which type of API request to perform (e.g. ``GET`` or ``POST``)

                         .. caution:: While ``PUT`` requests are technically supported in this library, at this time
                                      they are not yet supported by the Khoros Community API v1 endpoints.

    :type request_type: str
    :param return_json: Determines if the response should be returned in JSON format rather than the default
    :type return_json: bool
    :param params_in_uri: Determines if query parameters should be passed in the URI rather than in the request body
                         (``False`` by default)
    :type params_in_uri: bool
    :param json_payload: Determines if query parameters should be passed as JSON payload rather than in the URI
                         (``False`` by default)

                         .. caution:: This is not yet fully supported and therefore should not be used at this time.

    :type json_payload: bool
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :returns: The API response
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
             :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    # Determine if TLS certificates should be verified during API calls
    verify = should_verify_tls(khoros_object) if verify is None else verify

    # Construct the API request
    currently_unsupported_types = ['UPDATE', 'PATCH', 'DELETE']
    query_params = {} if not query_params else query_params
    query_string = encode_v1_query_string(query_params, return_json, params_in_uri)
    header = {"content-type": "application/x-www-form-urlencoded"}
    endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
    url = f"{khoros_object.core['v1_base']}/{endpoint}"

    # Only add the query parameters to the URI when explicitly requested
    if params_in_uri:
        query_string_delimiter = '&' if '?' in url else '?'
        url = f"{url}{query_string_delimiter}{query_string}"

    # Add query string to GET request URIs when a JSON response has been requested
    if request_type.upper() == 'GET' and return_json:
        json_query_string = 'restapi.response_format=json'
        query_string_delimiter = '&' if '?' in url else '?'
        url = f"{url}{query_string_delimiter}{json_query_string}"

    # Determine the request type and perform the appropriate call
    if request_type.upper() == 'GET':
        response = get_request_with_retries(url, return_json, khoros_object, headers=header,
                                            proxy_user_object=proxy_user_object, verify=verify)
    elif request_type.upper() == 'POST':
        if params_in_uri:
            response = post_request_with_retries(url, return_json=return_json, khoros_object=khoros_object,
                                                 headers=header, proxy_user_object=proxy_user_object, verify=verify)
        elif json_payload:
            # TODO: Finish testing and adding support for this type of payload (may just need different header)
            response = post_request_with_retries(url, json_payload=query_params, return_json=return_json,
                                                 khoros_object=khoros_object, headers=header,
                                                 proxy_user_object=proxy_user_object, verify=verify)
        else:
            response = post_request_with_retries(url, url_encoded_payload=query_string, return_json=return_json,
                                                 khoros_object=khoros_object, headers=header,
                                                 proxy_user_object=proxy_user_object, verify=verify)
    elif request_type.upper() == 'PUT':
        if params_in_uri:
            response = put_request_with_retries(url, return_json=return_json, khoros_object=khoros_object,
                                                headers=header, proxy_user_object=proxy_user_object, verify=verify)
        elif json_payload:
            # TODO: Finish testing and adding support for this type of payload (may just need different header)
            response = put_request_with_retries(url, json_payload=query_params, return_json=return_json,
                                                khoros_object=khoros_object, headers=header,
                                                proxy_user_object=proxy_user_object, verify=verify)
        else:
            response = put_request_with_retries(url, url_encoded_payload=query_string, return_json=return_json,
                                                khoros_object=khoros_object, headers=header,
                                                proxy_user_object=proxy_user_object, verify=verify)
    elif request_type.upper() in currently_unsupported_types:
        # TODO: Pass the request type into the exception to provide a more specific error
        raise errors.exceptions.CurrentlyUnsupportedError()
    else:
        # TODO: Pass the request type into the exception to provide a more specific error
        raise errors.exceptions.InvalidRequestTypeError()
    return response


def deliver_v2_results(response, full_response=None, return_id=None, return_url=None, return_api_url=None,
                       return_http_code=None, return_status=None, return_error_messages=None, split_errors=False,
                       khoros_object=None):
    """This function parses a Community API v2 response and returned specific data based on the function arguments.

    .. versionchanged:: 2.8.0
       Introduced the ability for error messages to be translated where possible to be more relevant, and added
       the optional ``khoros_object`` argument to facilitate this.

    .. versionchanged:: 2.5.2
       Replaced the ``return_developer_message`` argument with ``return_error_messages``.

    .. versionadded:: 2.5.0
       The code for this function was extracted from the :py:func:`khoros.objects.messages.create` function.

    :param response: The API response to be parsed
    :param full_response: Determines if the full raw API response should be returned
    :type full_response: bool, None
    :param return_id: Determines if the ``id`` field value should be returned
    :type return_id: bool, None
    :param return_url: Determines if the ``view_href`` field value should be returned
    :type return_url: bool, None
    :param return_api_url: Determines if the ``href`` field value should be returned
    :type return_api_url: bool, None
    :param return_http_code: Determines if the ``http_code`` field value should be returned
    :type return_http_code: bool, None
    :param return_status: Determines if the ``http_code`` field value should be returned
    :type return_status: bool, None
    :param return_error_messages: Determines if error messages should be returned when applicable
    :type return_error_messages: bool, None
    :param split_errors: Determines if error messages should be split into separate values or merged when applicable
    :type split_errors: bool
    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None

                         .. note:: The core object is only leveraged to check whether or not the ``translate_errors``
                                   setting is configured and to retrieve its value where possible.

    :returns: Boolean value indicating a successful outcome (default), the full API response or one or more specific
              fields defined by function arguments
    """
    outcome = query_successful(response)
    if any((return_id, return_url, return_api_url, return_http_code, return_status, return_error_messages)):
        data_to_return = []
        return_booleans = {
            'return_id': return_id,
            'return_url': return_url,
            'return_http_code': return_http_code,
            'return_api_url': return_api_url,
            'return_status': return_status,
            'return_error_messages': return_error_messages,
        }
        return_values = _get_v2_return_values(return_booleans, response, split_errors, khoros_object)
        for return_key, return_value in return_booleans.items():
            if return_value:
                data_to_return.append(return_values.get(return_key))
        outcome = tuple(data_to_return)
        if len(data_to_return) == 1:
            outcome = outcome[0]
    return response if full_response else outcome


def parse_v2_response(json_response, return_dict=False, status=False, error_msg=False, dev_msg=False,
                      split_errors=False, http_code=False, data_id=False, data_url=False,
                      data_api_uri=False, v2_base='', khoros_object=None):
    """This function parses an API response for a Community API v2 operation and returns parsed data.

    .. versionchanged:: 2.8.0
       Introduced the ability for error messages to be translated where possible to be more relevant, and added
       the optional ``khoros_object`` argument to facilitate this.

    .. versionchanged:: 2.5.2
       Replaced the ``developer_msg`` argument with ``error_msg`` and added the ``dev_msg`` and ``split_error``
       arguments with their accompanying functionality. (See :doc:`changelog` for more details.)

    .. versionchanged:: 2.5.0
       Moved from the :py:mod:`khoros.objects.messages` module to :py:mod:`khoros.api` and expanded the scope to
       apply to most Community API v2 API responses.

    .. versionadded:: 2.3.0

    :param json_response: The API response in JSON format
    :type json_response: dict
    :param return_dict: Defines if the parsed data should be returned within a dictionary
    :type return_dict: bool
    :param status: Defines if the **status** value should be returned
    :type status: bool
    :param error_msg: Defines if any **error messages** should be returned when applicable
    :type error_msg: bool
    :param dev_msg: Defines if the **developer message** should be returned when applicable
    :type dev_msg: bool
    :param split_errors: Defines if error messages should be returned as separate values when applicable
    :type split_errors: bool
    :param http_code: Defines if the **HTTP status code** should be returned
    :type http_code: bool
    :param data_id: Defines if the **ID** should be returned
    :type data_id: bool
    :param data_url: Defines if the **URL** should be returned
    :type data_url: bool
    :param data_api_uri: Defines if the **API URI** should be returned
    :type data_api_uri: bool
    :param v2_base: The base URL for the API v2
    :type v2_base: str, None
    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None

                         .. note:: The core object is only leveraged to check whether or not the ``translate_errors``
                                   setting is configured and to retrieve its value where possible.

    :returns: A string, tuple or dictionary with the parsed data
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    parsed_data = {}
    dev_msg = True if error_msg or dev_msg else False
    fields = {
        'status': (status, ('status',)),
        'error_msg': (error_msg, ('message',)),
        'dev_msg': (dev_msg, ('data', 'developer_message')),
        'http_code': (http_code, ('http_code',)),
        'data_id': (data_id, ('data', 'id')),
        'data_url': (data_url, ('data', 'view_href')),
        'data_api_uri': (data_api_uri, ('data', 'href')),
    }
    _confirm_field_supplied(fields)
    for field, info in fields.items():
        requested, json_path = info[0], info[1]
        if requested:
            if len(json_path) == 1:
                value = json_response[json_path[0]]
            else:
                value = json_response[json_path[0]][json_path[1]]
            parsed_data[field] = value
    if 'data_api_uri' in parsed_data and v2_base != '':
        parsed_data['data_api_uri'] = f"{v2_base}/{parsed_data.get('data_api_uri')}"
    if 'http_code' in parsed_data:
        try:
            parsed_data['http_code'] = int(parsed_data.get('http_code'))
        except (TypeError, ValueError):
            pass
    if 'error_msg' in parsed_data:
        translated_error_msg = errors.translations.translate_error(parsed_data.get('error_msg'), khoros_object)
        translated_dev_msg = errors.translations.translate_error(parsed_data.get('dev_msg'), khoros_object)
        if split_errors:
            parsed_data['error_msg'] = (translated_error_msg, translated_dev_msg)
        else:
            if len(parsed_data.get('dev_msg')) > 0 and parsed_data.get('error_msg') != parsed_data.get('dev_msg'):
                parsed_data['error_msg'] = f"{translated_error_msg} - {translated_dev_msg}"
            else:
                parsed_data['error_msg'] = translated_error_msg
        del parsed_data['dev_msg']
    if not return_dict:
        parsed_data = tuple(list(parsed_data.values()))
        if len(parsed_data) == 1:
            parsed_data = parsed_data[0]
    return parsed_data


def _get_v2_return_values(_return_booleans, _api_response, _split_errors, _khoros_object=None):
    """This function collects the relevant return values to be delivered for certain functions.

    .. versionchanged:: 2.8.0
       Introduced the ability for error messages to be translated where possible to be more relevant, and added
       the optional ``_khoros_object`` argument to facilitate this.

    .. versionadded:: 2.5.2

    :param _return_booleans: Dictionary of the return types with their associated Boolean value
    :type _return_booleans: dict
    :param _api_response: The Khoros Community API v2 response
    :type _api_response: dict
    :param _split_errors: Defines whether or not error messages should be merged when applicable
    :type _split_errors: bool
    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros], None

                          .. note:: The core object is only leveraged to check whether or not the ``translate_errors``
                                    setting is configured and to retrieve its value where possible.

    :returns: A dictionary of the parsed return values for return types whose Boolean values are ``True``
    """
    _return_values = {}
    for _return_type, _return_boolean in _return_booleans.items():
        if _return_boolean:
            try:
                if _return_type == 'return_id':
                    _return_values[_return_type] = parse_v2_response(_api_response, data_id=True,
                                                                     khoros_object=_khoros_object)
                elif _return_type == 'return_url':
                    _return_values[_return_type] = parse_v2_response(_api_response, data_url=True,
                                                                     khoros_object=_khoros_object)
                elif _return_type == 'return_api_url':
                    _return_values[_return_type] = parse_v2_response(_api_response, data_api_uri=True,
                                                                     khoros_object=_khoros_object)
                elif _return_type == 'return_http_code':
                    _return_values[_return_type] = parse_v2_response(_api_response, http_code=True,
                                                                     khoros_object=_khoros_object)
                elif _return_type == 'return_status':
                    _return_values[_return_type] = parse_v2_response(_api_response, status=True,
                                                                     khoros_object=_khoros_object)
                else:
                    _return_values[_return_type] = parse_v2_response(_api_response, error_msg=True,
                                                                     split_errors=_split_errors,
                                                                     khoros_object=_khoros_object)
            except KeyError:
                pass
    return _return_values


def _confirm_field_supplied(_fields_dict):
    """This function checks to ensure that at least one field has been enabled to retrieve.

    .. versionchanged:: 2.5.0
       Moved from the :py:mod:`khoros.objects.messages` module to :py:mod:`khoros.api`.

    .. versionadded:: 2.3.0

    :param _fields_dict: A dictionary made up of API fields and corresponding values
    :type _fields_dict: dict
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    _field_supplied = False
    for _field_value in _fields_dict.values():
        if _field_value[0]:
            _field_supplied = True
            break
    if not _field_supplied:
        raise errors.exceptions.MissingRequiredDataError("At least one field must be enabled to retrieve a response.")
    return


def _normalize_base_url(_base_url):
    """This function normalizes the base URL (i.e. top-level domain) for use in other functions.

    .. versionadded:: 3.0.0

    :param _base_url: The base URL of a Khoros Community environment
    :type _base_url: str
    :returns: The normalized base URL
    """
    _base_url = _base_url[:-1] if _base_url.endswith('/') else _base_url
    _base_url = f"https://{_base_url}" if not _base_url.startswith('http') else _base_url
    return _base_url


def get_platform_version(base_url, full_release=False, simple=False, commit_id=False, timestamp=False,
                         khoros_object=None, verify=None):
    """This function retrieves the Khoros Community platform version information for a given environment.

    .. versionchanged:: 4.3.0
       An issue has been fixed that prevented SSL verification from being disabled by the helper file setting.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object.

    .. versionadded:: 3.0.0

    :param base_url: The base URL (i.e. top-level domain) of the Khoros Community environment
    :type base_url: str
    :param full_release: Defines if the full platform release version should be returned

                         .. note:: If none of the options are enabled then the ``full_release`` option will be
                                   enabled by default.

    :type full_release: bool
    :param simple: Defines if the simple X.Y version (e.g. 20.6) should be returned
    :type simple: bool
    :param commit_id: Defines if the Commit ID (i.e. hash) for the release should be returned
    :type commit_id: bool
    :param timestamp: Defines if the timestamp of the release (e.g. 2007092156) should be returned
    :type timestamp: bool
    :param khoros_object: The core Khoros object (Optional unless needing to determine SSL certificate verification)
    :type khoros_object: class[khoros.Khoros], None
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :returns: One or more string with version information
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    # Determine if TLS certificates should be verified during API calls
    verify = should_verify_tls(khoros_object) if verify is None else verify

    # Perform and parse the
    full_release = True if not any((full_release, simple, commit_id, timestamp)) else full_release
    base_url = _normalize_base_url(base_url)
    version_info = requests.get(f'{base_url}/status/version', verify=verify)
    if version_info.status_code != 200:
        fail_msg = f'The attempt to get the platform version failed with a {version_info.status_code} status code.'
        logger.error(fail_msg)
        raise errors.exceptions.GETRequestError(fail_msg)
    versions = []
    parsed_info = {
        version_info.text.split('(')[1].split(')')[0]: full_release,
        version_info.text.split('Revision: ')[1].split(' (')[0]: simple,
        version_info.text.split('Commit Id: ')[1].split(' <br>')[0]: commit_id,
        version_info.text.split('Timestamp: ')[1].split('<')[0]: timestamp
    }
    for parsed_value, enabled in parsed_info.items():
        if enabled:
            versions.append(parsed_value)
    return versions[0] if len(versions) == 1 else tuple(versions)
