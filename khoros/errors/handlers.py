# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.handlers
:Synopsis:          Functions that handle various error situations within the namespace
:Usage:             ``from khoros.errors import handlers``
:Example:           ``error_msg = handlers.get_error_from_html(html_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Apr 2020
"""

import re
import sys
import importlib

from ..utils import core_utils


def eprint(*args, **kwargs):
    """This function behaves the same as the ``print()`` function but is leveraged to print errors to ``sys.stderr``."""
    print(*args, file=sys.stderr, **kwargs)
    return


def _exceptions_module_imported():
    """This function checks to see whether or not the ``exceptions`` global variable is defined."""
    try:
        exceptions
        _module_found = True
    except NameError:
        _module_found = False
    return _module_found


def _import_exceptions_module():
    """This function imports :py:func:`khoros.errors.exceptions` as a global variable using :py:mod:`importlib`."""
    global exceptions
    exceptions = importlib.import_module('khoros.errors.exceptions')
    return


def _import_exception_classes():
    """This function imports the :py:func:`khoros.errors.exceptions` module if not already imported."""
    if not _exceptions_module_imported():
        _import_exceptions_module()
    return


def get_error_from_html(html_error, v1=False):
    """This function parses an error message from Khoros displayed in HTML format.

    .. versionchanged:: 2.0.0
       Added the ``v1`` Boolean argument

    :param html_error: The raw HTML returned via the :py:mod:`requests` module
    :type html_error: str
    :param v1: Determines if the error is from a Community API v1 call (``False`` by default)
    :type v1: bool
    :returns: The concise error message parsed from the HTML
    """
    error_title = re.sub(r'</h1>.*$', r'', re.sub(r'^.*<body><h1>', r'', html_error))
    error_description = re.sub(r'</u>.*$', r'', re.sub(r'^.*description</b>\s*<u>', r'', html_error))
    error_msg = f"{error_title}{error_description}"
    if v1:
        error_msg = f"The Community API v1 call failed with the following error:\n\t{error_msg}"
    return error_msg


def get_error_from_xml(xml_error, endpoint='', fail_on_no_results=True):
    """This function retrieves any API errors returned from one of the Community APIs in XML format.

    :param xml_error: The API response in JSON format
    :type xml_error: str
    :param endpoint: The endpoint being queried by the API call (optional)
    :type endpoint: str
    :param fail_on_no_results: Defines if an exception should be raised if no results are returned (``True`` by default)
    :type fail_on_no_results: bool
    :returns: A Boolean value stating if an error was found (optional) and the error details in a tuple
    """
    error_code, error_msg, exc_msg = 0, '', ''
    no_results_pattern = re.compile(r'<response status="success">\s{2,}<\w*/></response>')
    if endpoint:
        if f'<response status="success">\n  <{endpoint}/>\n</response>' in xml_error:
            error_found = fail_on_no_results
            error_code = 404
            error_msg = f"The Community API v1 call against the '{endpoint}' endpoint returned no results."
            exc_msg = error_msg
        else:
            error_found = False
    elif no_results_pattern.search(xml_error.replace('\n', '')):
        error_found = fail_on_no_results
        error_code = 404
        error_msg = f"The Community API v1 call returned no results."
        exc_msg = error_msg
    elif '<response status="error">' in xml_error:
        error_found = True
        try:
            error_code = int(re.sub(r'.*code="', '', xml_error.replace('\n', '')).split('"')[0])
        except (ValueError, TypeError):
            error_code = 0
        error_msg = re.sub(r'\s{2,}</message>.*', '',
                           re.sub(r'.*<message>\s{2,}', '', xml_error.replace('\n', '')))
        error_msg = core_utils.decode_html_entities(error_msg)
        exc_msg = f"The Community API v1 call failed with the error code '{error_code}' and the following " + \
                  f"message: {error_msg}"
    else:
        error_found = False
    return error_found, (error_code, error_msg, exc_msg)


def _get_v1_error_from_json(_json_error, _fail_on_no_results):
    """This function extracts error details (if present) from a Community API v1 response.

    :param _json_error: The API response in JSON format
    :type _json_error: dict
    :param _fail_on_no_results: Defines if an exception should be raised if no results are returned
    :type _fail_on_no_results: bool
    :returns: A Boolean stating if an error was found and a tuple with the error code and error/exception messages
    """
    _error_code, _error_msg, _exc_msg = 0, '', ''
    _error_found = True if _json_error['status'] == 'error' else False
    if _error_found:
        _error_code = _json_error['error']['code']
        _error_msg = _json_error['error']['message']
        _exc_msg = f"The Community API v1 call failed with the error code '{_error_code}' and the following " + \
                   f"message: {_error_msg}"
    _inner_response = _json_error[list(_json_error.keys())[1]]
    if len(_inner_response[list(_inner_response.keys())[0]]) == 0:
        _error_found = _fail_on_no_results
        _error_code = 404
        _error_msg = f"The Community API v1 call returned no results."
        _exc_msg = _error_msg
    return _error_found, (_error_code, _error_msg, _exc_msg)


def _get_v2_error_from_json(_json_error):
    """This function extracts error details (if present) from a Community API v2 response.

    :param _json_error: The API response in JSON format
    :type _json_error: dict
    :returns: A Boolean stating if an error was found and a tuple with the error code and error/exception messages
    """
    _error_code, _error_msg, _exc_msg = 0, '', ''
    _error_found = True if _json_error['status'] == 'error' else False
    if _error_found:
        _error_code = _json_error['data']['code']
        _error_type = _json_error['data']['type']
        _error_msg = f"{_json_error['message']} (Error Type: {_error_type})"
        _exc_msg = f"The Community API v2 call failed with the error code '{_error_code}' and the following " + \
                   f"message: {_error_msg}"
    return _error_found, (_error_code, _error_msg, _exc_msg)


def get_error_from_json(json_error, v1=False, include_error_bool=True, fail_on_no_results=True):
    """This function retrieves any API errors returned from one of the Community APIs in JSON format.

    :param json_error: The API response in JSON format
    :type json_error: dict
    :param v1: Determines if the error is from a Community API v1 call (``False`` by default)
    :type v1: bool
    :param include_error_bool: Returns a Boolean as well that defines if an error was found (``True`` by default)
    :type include_error_bool: bool
    :param fail_on_no_results: Defines if an exception should be raised if no results are returned (``True`` by default)
    :type fail_on_no_results: bool
    :returns: A Boolean value stating if an error was found (optional) and the error details in a tuple
    """
    if 'response' in json_error or 'error' in json_error:
        v1 = True
        if 'response' in json_error:
            json_error = json_error['response']
    if v1:
        error_found, error_details = _get_v1_error_from_json(json_error, fail_on_no_results)
    else:
        # TODO: Handle v2 responses with no results similar to what is being done with v1
        error_found, error_details = _get_v2_error_from_json(json_error)
    if include_error_bool:
        return error_found, error_details
    return error_details


def verify_core_object_present(khoros_object):
    """This function verifies whether or not the core object was supposed and raises an exception if not.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not khoros_object:
        _import_exception_classes()
        raise exceptions.MissingRequiredDataError('The core object must be provided in order to perform the action')
    return


def verify_v1_response(api_response, query_type='get', endpoint='', fail_on_no_results=False):
    """This function evaluates a Community API v1 response to identify any failures.

    :param api_response: The response from the API call
    :param query_type: The type of API call that was made, such as ``get`` (default), ``post``, ``put``, etc.
    :type query_type: str
    :param endpoint: The endpoint being queried by the API call (optional)
    :type endpoint: str
    :param fail_on_no_results: Raises an exception if no results are returned (``False`` by default)
    :type fail_on_no_results: bool
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.APIRequestError`, :py:exc:`khoros.errors.exceptions.DELETERequestError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`, :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`
    """
    _import_exception_classes()
    valid_query_types = ['get', 'post', 'put', 'delete']
    query_type = 'other' if query_type not in valid_query_types else query_type
    exception_classes = {
        'get': exceptions.GETRequestError,
        'post': exceptions.POSTRequestError,
        'put': exceptions.PUTRequestError,
        'delete': exceptions.DELETERequestError,
        'other': exceptions.APIRequestError
    }
    if type(api_response) == dict:
        error_found, error_details = get_error_from_json(api_response, v1=True, fail_on_no_results=fail_on_no_results)
    elif api_response.status_code != 200:
        if type(api_response.text) == str and api_response.text.startswith('<html>'):
            error_msg = get_error_from_html(api_response.text, v1=True)
            raise exception_classes.get(query_type)(error_msg)
        else:
            raise exception_classes.get(query_type)
    elif type(api_response.text) == str and api_response.text.startswith('<response'):
        error_found, error_details = get_error_from_xml(api_response.text, endpoint, fail_on_no_results)
    else:
        error_found, error_details = False, None
    if error_found:
        error_code, error_msg, exc_msg = error_details
        if error_code == 404 and fail_on_no_results:
            raise exceptions.NotFoundResponseError(exc_msg)
        else:
            raise exception_classes.get(query_type)(exc_msg)
    return
