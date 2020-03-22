# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Usage:             ``from khoros.utils import core_utils``
:Example:           ``encoded_string = core_utils.encode_url(decoded_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Mar 2020
"""

import random
import string
import urllib.parse


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


def __is_zero_length(_element):
    return True if len(_element) == 0 else False


def __structure_query_string(_url_dict, _no_encode):
    """This function constructs a query string where one or more fields must not be URL-encoded.

    :param _url_dict: Dictionary of URL query string keys and values
    :type _url_dict: dict
    :param _no_encode: Designates any dictionary keys (i.e. field names) whose values should not be URL-encoded
    :type _no_encode: list, tuple, set, str, NoneType
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
    :type no_encode: list, tuple, set, str, NoneType
    :returns: The URL query string in string format
    """
    if no_encode:
        query_string = __structure_query_string(url_dict, no_encode)
    else:
        query_string = urllib.parse.urlencode(url_dict)
    return query_string


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


def get_random_string(length=32, prefix_string=""):
    """This function returns a random alphanumeric string to use as a salt or password.

    :param length: The length of the string (``32`` by default)
    :type length: int
    :param prefix_string: A string to which the salt should be appended (optional)
    :type prefix_string: str
    :returns: The alphanumeric string
    """
    return f"{prefix_string}{''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])}"
