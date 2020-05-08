# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Usage:             ``from khoros.utils import core_utils``
:Example:           ``encoded_string = core_utils.encode_url(decoded_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Apr 2020
"""

import os
import random
import string
import warnings
import urllib.parse
from html import unescape

from .. import errors


def url_encode(raw_string):
    """This function encodes a string for use in URLs.

    :param raw_string: The raw string to be encoded
    :type raw_string: str
    :returns: The encoded string
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string):
    """This function decodes a url-encoded string.

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    """
    return urllib.parse.unquote_plus(encoded_string)


def decode_html_entities(html_string):
    """This function converts HTML entities (e.g. ``&amp;``, ``&apos;``, etc.) back to their original characters.

    :param html_string: The string containing HTML entities to be decoded
    :type html_string: str
    :returns: The string with decoded HTML entities
    """
    return unescape(html_string)


def __is_zero_length(_element):
    return True if len(_element) == 0 else False


def __structure_query_string(_url_dict, _no_encode):
    """This function constructs a query string where one or more fields must not be URL-encoded.

    :param _url_dict: Dictionary of URL query string keys and values
    :type _url_dict: dict
    :param _no_encode: Designates any dictionary keys (i.e. field names) whose values should not be URL-encoded
    :type _no_encode: list, tuple, set, str, None
    :returns: The URL query string in string format
    """
    if type(_no_encode) == str:
        _no_encode = (_no_encode, )
    _delimiters = {True: "", False: "&"}
    _query_string = ""
    for _field_name, _field_value in _url_dict.items():
        if _field_name not in _no_encode:
            _field_value = url_encode(_field_value)
        _delimiter = _delimiters.get(__is_zero_length(_query_string))
        _query_string = f"{_query_string}{_delimiter}{_field_name}={_field_value}"
    return _query_string


def encode_query_string(url_dict, no_encode=None):
    """This function compiles a URL query string from a dictionary of parameters.

    :param url_dict: Dictionary of URL query string keys and values
    :type url_dict: dict
    :param no_encode: Designates any dictionary keys (i.e. field names) whose values should not be URL-encoded
    :type no_encode: list, tuple, set, str, None
    :returns: The URL query string in string format
    """
    if no_encode:
        query_string = __structure_query_string(url_dict, no_encode)
    else:
        query_string = urllib.parse.urlencode(url_dict)
    return query_string


def is_numeric(value):
    """This function checks whether or not a value is numeric either as an integer or a numeric string.

    .. versionadded:: 2.3.0

    :param value: The value to be examined
    :type value: str, int
    :returns: Boolean value indicating if the examined value is numeric
    """
    return True if type(value) == int or (type(value) == str and value.isnumeric()) else False


def convert_set(iterable, convert_to='list'):
    """This function casts a ``set`` variable to be a ``list`` instead so that it can be scriptable.

    :param iterable: The iterable to be evaluated to see if it has a ``set`` type
    :param convert_to: Defines if the iterable should be cast to a ``list`` (default) or a ``tuple``
    :type convert_to: str
    :returns: The converted variable as a ``list`` or ``tuple`` (or untouched if not a ``set``)
    """
    if type(iterable) == set:
        if convert_to == 'tuple':
            iterable = tuple(iterable)
        else:
            iterable = list(iterable)
    return iterable


def convert_single_value_to_tuple(value):
    """This function converts a single value of nearly any type into a tuple.

    .. versionadded:: 2.3.0

    :param value: The value to convert into a tuple
    """
    return (value, )


def convert_string_to_tuple(value):
    """THis function converts a value to a tuple if in string format.

    .. versionadded:: 2.3.0

    :param value: The potential string to convert
    :returns: The tuple (if original value was in string format) or the original value/type
    """
    if type(value) == str:
        value = convert_single_value_to_tuple(value)
    return value


def get_random_string(length=32, prefix_string=""):
    """This function returns a random alphanumeric string to use as a salt or password.

    :param length: The length of the string (``32`` by default)
    :type length: int
    :param prefix_string: A string to which the salt should be appended (optional)
    :type prefix_string: str
    :returns: The alphanumeric string
    """
    return f"{prefix_string}{''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])}"


def display_warning(warn_msg):
    """This function displays a :py:exc:`UserWarning` message via the :py:mod:`warnings` module.

    .. versionadded:: 2.1.0

    :param warn_msg: The message to be displayed
    :type warn_msg: str
    :returns: None
    """
    warnings.warn(warn_msg, UserWarning)
    return


def get_file_type(file_path):
    """This function attempts to identify if a given file path is for a YAML or JSON file.

    .. versionadded:: 2.2.0

    :param file_path: The full path to the file
    :type file_path: str
    :returns: The file type in string format (e.g. ``yaml`` or ``json``)
    :raises: :py:exc:`FileNotFoundError`, :py:exc:`khoros.errors.exceptions.UnknownFileTypeError`
    """
    file_type = 'unknown'
    if os.path.isfile(file_path):
        if file_path.endswith('.json'):
            file_type = 'json'
        elif file_path.endswith('.yml') or file_path.endswith('.yaml'):
            file_type = 'yaml'
        else:
            display_warning(f"Unable to recognize the file type of '{file_path}' by its extension.")
            with open(file_path) as cfg_file:
                for line in cfg_file:
                    if line.startswith('#'):
                        continue
                    else:
                        if '{' in line:
                            file_type = 'json'
                            break
        if file_type == 'unknown':
            raise errors.exceptions.UnknownFileTypeError(file=file_path)
    else:
        raise FileNotFoundError(f"Unable to locate the following file: {file_path}")
    return file_type
