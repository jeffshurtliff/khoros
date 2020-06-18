# -*- coding: utf-8 -*-
"""
:Module:            khoros.api
:Synopsis:          This module handles interactions with the Khoros Community REST APIs
:Usage:             ``import khoros.api``
:Example:           ``json_response = khoros.api.get_request_with_retries(url, auth_dict=khoros.auth)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     18 Jun 2020
"""

import json
import os.path

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from . import errors
from .utils import core_utils


def define_headers(khoros_object=None, auth_dict=None, params=None, accept=None, content_type=None, multipart=False,
                   default_content_type=False):
    """This function defines the headers to use in an API call.

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
    :returns: A dictionary with the header fields and associated values
    """
    if not khoros_object and not auth_dict:
        raise errors.exceptions.MissingAuthDataError()
    else:
        if auth_dict:
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


def get_request_with_retries(query_url, return_json=True, khoros_object=None, auth_dict=None, headers=None):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

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
    :returns: The API response from the GET request (optionally in JSON format)
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers)
    retries = 0
    while retries <= 5:
        try:
            response = requests.get(query_url, headers=headers)
            break
        except Exception as exc_msg:
            _report_failed_attempt(exc_msg, 'get', retries)
            retries += 1
            pass
    if retries == 6:
        _raise_exception_for_repeated_timeouts()
    return _attempt_json_conversion(response, return_json)


def _api_request_with_payload(_url, _payload=None, _request_type='post', _headers=None, _multipart=False):
    """This function performs an API request while supplying a JSON payload.

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
    :returns: The API response
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    _headers = {} if not _headers else _headers
    _retries = 0
    if not _payload:
        _response = _api_request_without_payload(_url, _request_type, _headers)
    else:
        while _retries <= 5:
            try:
                if _request_type.lower() == "put":
                    if _multipart:
                        _response = requests.put(_url, files=_payload, headers=_headers)
                    else:
                        _response = requests.put(_url, data=json.dumps(_payload, default=str), headers=_headers)
                elif _request_type.lower() == "post":
                    if _multipart:
                        _response = requests.post(_url, files=_payload, headers=_headers)
                    else:
                        _response = requests.post(_url, data=json.dumps(_payload, default=str), headers=_headers)
                else:
                    raise errors.exceptions.InvalidRequestTypeError()
                break
            except Exception as _exc_msg:
                _report_failed_attempt(_exc_msg, _request_type, _retries)
                _retries += 1
                pass
        if _retries == 6:
            _raise_exception_for_repeated_timeouts()
    return _response


def _api_request_without_payload(_url, _request_type, _headers):
    """This function performs a ``POST`` or ``PUT`` request without an accompanying JSON payload.

    :param _url: The URL for the API request
    :type _url: str
    :param _request_type: The request type (e.g. ``post`` or ``put``)
    :type _request_type: str
    :param _headers: The headers associated with the API request
    :type _headers: dict
    :returns: The API response
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    _retries = 0
    while _retries <= 5:
        try:
            if _request_type.lower() == "post":
                _response = requests.post(_url, headers=_headers)
            elif _request_type.lower() == "put":
                _response = requests.put(_url, headers=_headers)
            else:
                raise errors.exceptions.InvalidRequestTypeError()
            break
        except Exception as _exc_msg:
            _report_failed_attempt(_exc_msg, _request_type, _retries)
            _retries += 1
            pass
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


def post_request_with_retries(url, json_payload=None, return_json=True, khoros_object=None, auth_dict=None,
                              headers=None, multipart=False):
    """This function performs a POST request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 2.5.0
       The function can now be called without supplying a JSON payload.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the POST request in JSON format
    :type json_payload: dict, None
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
    :returns: The API response from the POST request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers, multipart=multipart)
    response = _api_request_with_payload(url, json_payload, 'post', headers, multipart)
    return _attempt_json_conversion(response, return_json)


def put_request_with_retries(url, json_payload=None, return_json=True, khoros_object=None, auth_dict=None,
                             headers=None, multipart=False):
    """This function performs a PUT request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 2.5.0
       The function can now be called without supplying a JSON payload.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the PUT request in JSON format
    :type json_payload: dict, None
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
    :returns: The API response from the PUT request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers, multipart=multipart)
    response = _api_request_with_payload(url, json_payload, 'put', headers, multipart)
    return _attempt_json_conversion(response, return_json)


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


def delete(url, return_json=False, khoros_object=None, auth_dict=None, headers=None):
    """This function performs a DELETE request against the Core API.

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
    :returns: The API response from the DELETE request (optionally in JSON format)
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers)
    response = requests.delete(url, headers=headers)
    if return_json:
        response = response.json()
    return response


def perform_v1_search(khoros_object, endpoint, filter_field, filter_value, return_json=False, fail_on_no_results=False):
    """This function performs a search for a particular field value using a Community API v1 call.

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
    :returns: The API response (optionally in JSON format)
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    headers = define_headers(khoros_object, content_type='application/x-www-form-urlencoded')
    if type(filter_value) == str:
        filter_value = core_utils.url_encode(filter_value)
    uri = f"{khoros_object.core['v1_base']}/search/{endpoint}?q={filter_field}:{filter_value}"
    uri = f"{uri}{_get_json_query_string(return_json)}"
    response = requests.get(uri, headers=headers)
    if return_json:
        response = response.json()
        response = response['response'] if 'response' in response else response
    errors.handlers.verify_v1_response(response, 'get', 'users', fail_on_no_results)
    return response


def encode_multipart_data(data_fields):
    """This function uses the Streaming Multipart Data Encoder to encode the payload for a multipart/form-data API call.

    .. versionadded:: 2.3.0

    .. seealso:: This function follows the `requests_toolbelt <https://rsa.im/3dg7QiZ>`_ documentation.

    :param data_fields: A dictionary with the data to be encoded
    :type data_fields: dict
    :returns: The encoded data for use by the :py:mod:`requests` library
    """
    return MultipartEncoder(fields=data_fields)


def encode_v1_query_string(query_dict, return_json=True):
    """This function formats and URL-encodes a Community API v1 quey string.

    .. versionadded:: 2.5.0

    :param query_dict: A dictionary with the query fields and associated values
    :type query_dict: dict
    :param return_json: Determines if JSON should be returned rather than XML (default: ``True``)
    :type return_json: bool
    :returns: The properly formatted and encoded query string
    """
    if return_json:
        query_dict['restapi.response_format'] = 'json'
    return core_utils.encode_query_string(query_dict)


def make_v1_request(khoros_object, endpoint, query_params, request_type='GET', return_json=True):
    """This function makes a Community API v1 request.

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
    :type query_params: dict
    :param request_type: Determines which type of API request to perform (e.g. ``GET``, ``POST``, ``PUT``, etc.)
    :type request_type: str
    :param return_json: Determines if the response should be returned in JSON format rather than the default
    :type return_json: bool
    :returns: The API response
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
             :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`
    """
    currently_unsupported_types = ['UPDATE', 'PATCH', 'DELETE']
    query_string = encode_v1_query_string(query_params, return_json)
    header = {"content-type": "application/x-www-form-urlencoded"}
    url = f"{khoros_object.core['v1_base']}/{endpoint}?{query_string}"
    if request_type.upper() == 'GET':
        response = get_request_with_retries(url, return_json, khoros_object, headers=header)
    elif request_type.upper() == 'POST':
        response = post_request_with_retries(url, return_json=return_json, khoros_object=khoros_object, headers=header)
    elif request_type.upper() == 'PUT':
        response = put_request_with_retries(url, return_json=return_json, khoros_object=khoros_object, headers=header)
    elif request_type.upper() in currently_unsupported_types:
        raise errors.exceptions.CurrentlyUnsupportedError()
    else:
        raise errors.exceptions.InvalidRequestTypeError()
    # TODO: Verify successful response
    return response


def deliver_v2_results(response, full_response=None, return_id=None, return_url=None, return_api_url=None,
                       return_http_code=None, return_status=None, return_error_messages=None, split_errors=False):
    """This function parses a Community API v2 response and returned specific data based on the function arguments.

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
        return_values = _get_v2_return_values(return_booleans, response, split_errors)
        for return_key, return_value in return_booleans.items():
            if return_value:
                data_to_return.append(return_values.get(return_key))
        outcome = tuple(data_to_return)
        if len(data_to_return) == 1:
            outcome = outcome[0]
    return response if full_response else outcome


def parse_v2_response(json_response, return_dict=False, status=False, error_msg=False, dev_msg=False,
                      split_errors=False, http_code=False, data_id=False, data_url=False,
                      data_api_uri=False, v2_base=''):
    """This function parses an API response for a Community API v2 operation and returns parsed data.

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
    :type v2_base: str
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
        if split_errors:
            parsed_data['error_msg'] = (parsed_data.get('error_msg'), parsed_data.get('dev_msg'))
        else:
            if len(parsed_data.get('dev_msg')) > 0 and parsed_data.get('error_msg') != parsed_data.get('dev_msg'):
                parsed_data['error_msg'] = f"{parsed_data.get('error_msg')} - {parsed_data.get('dev_msg')}"
        del parsed_data['dev_msg']
    if not return_dict:
        parsed_data = tuple(list(parsed_data.values()))
        if len(parsed_data) == 1:
            parsed_data = parsed_data[0]
    return parsed_data


def _get_v2_return_values(_return_booleans, _api_response, _split_errors):
    """This function collects the relevant return values to be delivered for certain functions.

    .. versionadded:: 2.5.2

    :param _return_booleans: Dictionary of the return types with their associated Boolean value
    :type _return_booleans: dict
    :param _api_response: The Khoros Community API v2 response
    :type _api_response: dict
    :param _split_errors: Defines whether or not error messages should be merged when applicable
    :type _split_errors: bool
    :returns: A dictionary of the parsed return values for return types whose Boolean values are ``True``
    """
    _return_values = {}
    for _return_type, _return_boolean in _return_booleans.items():
        if _return_boolean:
            try:
                if _return_type == 'return_id':
                    _return_values[_return_type] = parse_v2_response(_api_response, data_id=True)
                elif _return_type == 'return_url':
                    _return_values[_return_type] = parse_v2_response(_api_response, data_url=True)
                elif _return_type == 'return_api_url':
                    _return_values[_return_type] = parse_v2_response(_api_response, data_api_uri=True)
                elif _return_type == 'return_http_code':
                    _return_values[_return_type] = parse_v2_response(_api_response, http_code=True)
                elif _return_type == 'return_status':
                    _return_values[_return_type] = parse_v2_response(_api_response, status=True)
                else:
                    _return_values[_return_type] = parse_v2_response(_api_response, error_msg=True,
                                                                     split_errors=_split_errors)
            except KeyError:
                pass
    return _return_values


def _confirm_field_supplied(_fields_dict):
    """This function checks to ensure that at least one field has been enabled to retrieve.

    .. versionchanged:: 2.5.0
       Moved from the :py:mod:`khoros.objects.messages` module to :py:mod:`khoros.api`.

    .. versionadded:: 2.3.0
    """
    _field_supplied = False
    for _field_value in _fields_dict.values():
        if _field_value[0]:
            _field_supplied = True
            break
    if not _field_supplied:
        raise errors.exceptions.MissingRequiredDataError("At least one field must be enabled to retrieve a response.")
    return
