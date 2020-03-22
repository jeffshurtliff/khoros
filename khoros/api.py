# -*- coding: utf-8 -*-
"""
:Module:            khoros.api
:Synopsis:          This module handles interactions with the Khoros Community REST APIs
:Usage:             ``import khoros.api``
:Example:           ``json_response = khoros.api.get_request_with_retries(url, auth_dict=khoros.auth)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Mar 2020
"""

import json
import requests

from . import errors


def define_headers(khoros_object=None, auth_dict=None, params=None, accept=None, content_type=None):
    """This function defines the headers to use in an API call.

    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros]
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict
    :param params: Header parameters in a dictionary format
    :type params: dict
    :param accept: The ``Accept`` header value (e.g. ``application/json``)
    :type accept: str, NoneType
    :param content_type: The ``Content-Type`` header value (e.g. ``application/json``)
    :type content_type: str, NoneType
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
    return headers


# Define function to perform a GET request with retries
def get_request_with_retries(query_url, return_json=True, khoros_object=None, auth_dict=None, headers=None):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

    :param query_url: The URI to be queried
    :type query_url: str
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros]
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, NoneType
    :returns: The API response from the GET request (optionally in JSON format)
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`, :py:exc:`ConnectionError`
    """
    # Define the request headers
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers)

    # Perform the GET request
    retries = 0
    while retries <= 5:
        try:
            response = requests.get(query_url, headers=headers)
            break
        except Exception as e:
            current_attempt = f"(Attempt {retries} of 5)"
            error_msg = f"The GET request failed with the exception below. {current_attempt}"
            print(f"{error_msg}\n{e}\n")
            retries += 1
            pass
    if retries == 6:
        failure_msg = "The API call was unable to complete successfully after five consecutive API timeouts " + \
                      "and/or failures. Please call the function again or contact Khoros Support."
        raise ConnectionError(failure_msg)

    # Convert to JSON if specified
    if return_json and type(response) != dict:
        response = response.json()
    return response


# Define internal function to perform API requests (PUT or POST) with JSON payload
def __api_request_with_payload(_url, _json_payload, _request_type, headers=None):
    """This function performs an API request while supplying a JSON payload."""
    if not headers:
        headers = {}
    _retries = 0
    while _retries <= 5:
        try:
            if _request_type.lower() == "put":
                _response = requests.put(_url, data=json.dumps(_json_payload, default=str), headers=headers)
            elif _request_type.lower() == "post":
                _response = requests.post(_url, data=json.dumps(_json_payload, default=str), headers=headers)
            else:
                raise errors.exceptions.InvalidRequestTypeError
            break
        except Exception as _api_exception:
            _current_attempt = f"(Attempt {_retries} of 5)"
            _error_msg = f"The {_request_type.upper()} request has failed with the following exception: " + \
                         f"{_api_exception} {_current_attempt}"
            print(_error_msg)
            _retries += 1
            pass
    if _retries == 6:
        _failure_msg = "The script was unable to complete successfully after five consecutive API timeouts. " + \
                       "Please run the script again or contact Khoros or Aurea Support for further assistance."
        raise errors.exceptions.APIConnectionError(_failure_msg)
    return _response


# Define function to perform a POST request with supplied JSON data
def post_request_with_retries(url, json_payload, return_json=True, khoros_object=None, auth_dict=None, headers=None):
    """This function performs a POST request with a total of 5 retries in case of timeouts or connection issues.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the POST request in JSON format
    :type json_payload: dict
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros]
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, NoneType
    :returns: The API response from the POST request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers)
    response = __api_request_with_payload(url, json_payload, 'post', headers)
    if return_json and type(response) != dict:
        response = response.json()
    return response


# Define function to perform a PUT request with supplied JSON data
def put_request_with_retries(url, json_payload, return_json=True, khoros_object=None, auth_dict=None, headers=None):
    """This function performs a PUT request with a total of 5 retries in case of timeouts or connection issues.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the PUT request in JSON format
    :type json_payload: dict
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``True``)
    :type return_json: bool
    :param khoros_object: The core Khoros object (Required if the ``auth_dict`` parameter is not supplied)
    :type khoros_object: class[khoros.Khoros]
    :param auth_dict: The ``auth`` dictionary within the :py:class:`khoros.Khoros` class object
    :type auth_dict: dict
    :param headers: Any header values (in dictionary format) to pass in the API call (optional)
    :type headers: dict, NoneType
    :returns: The API response from the PUT request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`
    """
    headers = define_headers(khoros_object=khoros_object, auth_dict=auth_dict, params=headers)
    response = __api_request_with_payload(url, json_payload, 'put', headers)
    if return_json and type(response) != dict:
        response = response.json()
    return response
