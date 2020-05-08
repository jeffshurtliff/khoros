# -*- coding: utf-8 -*-
"""
:Module:            khoros.api
:Synopsis:          This module handles interactions with the Khoros Community REST APIs
:Usage:             ``import khoros.api``
:Example:           ``json_response = khoros.api.get_request_with_retries(url, auth_dict=khoros.auth)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 May 2020
"""

import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from . import errors
from .utils import core_utils


def define_headers(khoros_object=None, auth_dict=None, params=None, accept=None, content_type=None, multipart=False):
    """This function defines the headers to use in an API call.

    .. versionchanged:: 2.3.0
       Added the ``multipart`` Boolean argument to remove the ``Content-Type`` key value pair when appropriate.

    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros], None
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict, None
    :param params: Header parameters in a dictionary format
    :type params: dict, None
    :param accept: The ``Accept`` header value (e.g. ``application/json``)
    :type accept: str, None
    :param content_type: The ``Content-Type`` header value (e.g. ``application/json``)
    :type content_type: str, None
    :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
    :type multipart: bool
    :returns: A dictionary with the header fields and associated values
    """
    if not khoros_object and not auth_dict:
        raise errors.exceptions.MissingAuthDataError
    else:
        if auth_dict:
            headers = auth_dict['header']
        else:
            headers = khoros_object.auth['header']
    if params:
        headers.update(params)
    if accept:
        headers['Accept'] = accept
    if content_type:
        headers['Content-Type'] = content_type
    if multipart and 'Content-Type' in headers:
        del headers['Content-Type']
    return headers


def _get_json_query_string(_return_json, _include_ampersand_prefix=True):
    # TODO: Add a docstring for the function
    _query_strings = {True: 'restapi.response_format=json', False: ''}
    _prefixes = {True: '&', False: ''}
    _query_string = ''
    if _return_json:
        _query_string = f"{_prefixes.get(_include_ampersand_prefix)}{_query_strings.get(_return_json)}"
    return _query_string


def get_request_with_retries(query_url, return_json=True, khoros_object=None, auth_dict=None, headers=None):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

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
    # Define the request headers
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers)

    # Perform the GET request
    retries = 0
    while retries <= 5:
        try:
            response = requests.get(query_url, headers=headers)
            break
        except Exception as exc_msg:
            exc_name = type(exc_msg).__name__
            if 'connect' not in exc_name.lower():
                raise Exception(f"{exc_name}: {exc_msg}")
            current_attempt = f"(Attempt {retries} of 5)"
            error_msg = f"The GET request failed with the exception below. {current_attempt}"
            errors.handlers.eprint(f"{error_msg}\n{exc_name}: {exc_msg}\n")
            retries += 1
            pass
    if retries == 6:
        failure_msg = "The API call was unable to complete successfully after five consecutive API timeouts " + \
                      "and/or failures. Please call the function again or contact Khoros Support."
        raise errors.exceptions.APIConnectionError(failure_msg)

    # Convert to JSON if specified
    if return_json and type(response) != dict:
        response = response.json()
    return response


def _api_request_with_payload(_url, _payload, _request_type, _headers=None, _multipart=False):
    """This function performs an API request while supplying a JSON payload.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param _url: The URI to be queried
    :type _url: str
    :param _payload: The payload that accompanies the API call
    :type _payload: dict, str
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
                raise errors.exceptions.InvalidRequestTypeError
            break
        except Exception as _exc_msg:
            _exc_name = type(_exc_msg).__name__
            if 'connect' not in _exc_name.lower():
                raise Exception(f"{_exc_name}: {_exc_msg}")
            _current_attempt = f"(Attempt {_retries} of 5)"
            _error_msg = f"The {_request_type.upper()} request has failed with the following exception: " + \
                         f"{_exc_name}: {_exc_msg} {_current_attempt}"
            errors.handlers.eprint(f"{_error_msg}\n{_exc_name}: {_exc_msg}\n")
            _retries += 1
            pass
    if _retries == 6:
        _failure_msg = "The script was unable to complete successfully after five consecutive API timeouts. " + \
                       "Please run the script again or contact Khoros Support for further assistance."
        raise errors.exceptions.APIConnectionError(_failure_msg)
    return _response


def post_request_with_retries(url, json_payload, return_json=True, khoros_object=None, auth_dict=None,
                              headers=None, multipart=False):
    """This function performs a POST request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the POST request in JSON format
    :type json_payload: dict
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
    if return_json and type(response) != dict:
        try:
            response = response.json()
        except Exception as exc_msg:
            exc_name = type(exc_msg).__name__
            errors.handlers.eprint(f"Failed to convert to JSON due to the following exception: {exc_name}: {exc_msg}")
    return response


def put_request_with_retries(url, json_payload, return_json=True, khoros_object=None, auth_dict=None,
                             headers=None, multipart=False):
    """This function performs a PUT request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 2.3.0
       Added the ability to perform multipart/form-data queries.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the PUT request in JSON format
    :type json_payload: dict
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
    if return_json and type(response) != dict:
        try:
            response = response.json()
        except Exception as exc_msg:
            exc_name = type(exc_msg).__name__
            errors.handlers.eprint(f"Failed to convert to JSON due to the following exception: {exc_name}: {exc_msg}")
    return response


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
