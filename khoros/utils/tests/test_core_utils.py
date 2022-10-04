# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_core_utils
:Synopsis:       This module is used by pytest to verify that the core package utilities work properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  09 Jun 2022
"""

import os
import sys
import importlib

import pytest


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    sys.path.insert(0, os.path.abspath('../..'))


def import_core_utils():
    """This function imports the :py:mod:`khoros.utils.core_utils` module.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    set_package_path()
    global core_utils
    core_utils = importlib.import_module('khoros.utils.core_utils')


def test_url_encoding():
    """This function tests the :py:func:`khoros.utils.core_utils.url_encode` and
       :py:func:`khoros.utils.core_utils.url_decode` functions.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    raw_url = "https://community.example.com/t5/bizapps/bizappspage/tab/community:studio:api-browser?searchString=select id from users where login = 'admin'"
    encoded_url = "https%3A%2F%2Fcommunity.example.com%2Ft5%2Fbizapps%2Fbizappspage%2Ftab%2Fcommunity%3Astudio%3Aapi-browser%3FsearchString%3Dselect+id+from+users+where+login+%3D+%27admin%27"
    assert core_utils.url_encode(raw_url) == encoded_url    # nosec
    assert core_utils.url_decode(encoded_url) == raw_url    # nosec


def test_query_string_encoding():
    """This function tests the :py:func:`khoros.utils.core_utils.encode_query_string` function.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    query_dict = {
        'user.login': 'exampleuser',
        'user.password': 'Ch@ngeM3!#$',
        'restapi.response_format': 'json',
    }
    encoded_string = 'user.login=exampleuser&user.password=Ch%40ngeM3%21%23%24&restapi.response_format=json'
    encoded_string_raw_pw = 'user.login=exampleuser&user.password=Ch@ngeM3!#$&restapi.response_format=json'
    assert core_utils.encode_query_string(query_dict) == encoded_string     # nosec
    assert core_utils.encode_query_string(query_dict, no_encode='user.password') == encoded_string_raw_pw   # nosec


def test_html_entity_convert():
    """This function tests the :py:func:`khoros.utils.core_utils.decode_html_entitles` function.

    .. versionadded:: 5.1.2
    """
    html_string = 'This &amp; That'
    converted_string = core_utils.decode_html_entities(html_string)
    assert converted_string == 'This & That'


def test_decode_binary():
    """This function tests the ability to decode binary into a string.

    .. versionadded:: 5.1.2
    """
    binary_text = b'This is binary text'
    decoded_text = core_utils.decode_binary(binary_text)
    assert isinstance(decoded_text, str) and decoded_text == 'This is binary text'


def test_base64_conversions():
    """This function tests various types of base64 string conversions.

    .. versionadded:: 5.1.2
    """
    # Test basic plain text to base64 conversion
    plain_text = 'This is my example text'
    base64_text = 'VGhpcyBpcyBteSBleGFtcGxlIHRleHQ='
    assert core_utils.encode_base64(plain_text) == base64_text

    # Test URL-encoded conversion
    url_encoded_base64_text = 'VGhpcyBpcyBteSBleGFtcGxlIHRleHQ%3D'
    assert core_utils.encode_base64(plain_text, url_encode_object=True) == url_encoded_base64_text

    # Test binary return value
    bytes_base64_text = b'VGhpcyBpcyBteSBleGFtcGxlIHRleHQ='
    assert core_utils.encode_base64(plain_text, return_bytes=True) == bytes_base64_text


def test_numeric_eval():
    """This function tests the :py:func:`khoros.utils.core_utils.is_numeric` function.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    numeric_string = '12345'
    integer = 12345
    non_numeric_string = 'ABcd1234'
    assert core_utils.is_numeric(numeric_string) and core_utils.is_numeric(integer)     # nosec
    assert not core_utils.is_numeric(non_numeric_string)    # nosec


def test_remove_tld():
    """This function tests to the :py:func:`khoros.utils.core_utils.remove_tld` function.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    url = 'https://community.khoros.com/t5/Developer-Discussion/Add-multiple-tags-to-a-message-with-a-' \
          'single-API-call/m-p/596532#M17061'
    control_data = {
        'with': '/t5/Developer-Discussion/Add-multiple-tags-to-a-message-with-a-single-API-call/m-p/596532#M17061',
        'without': '/t5/Developer-Discussion/Add-multiple-tags-to-a-message-with-a-single-API-call/m-p/596532'
    }
    assert core_utils.remove_tld(url, strip_anchors=False) == control_data.get('with')      # nosec
    assert core_utils.remove_tld(url, strip_anchors=True) == control_data.get('without')    # nosec


def test_merge_and_dedup():
    """This function tests the :py:func:`khoros.utils.core_utils.merge_and_dedup` function.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = ['one', 'two', 'three', 'four', 'five', 6]
    test_data = core_utils.merge_and_dedup('one', 'two', 'two', ('two', 'three'), ['four', 'four'],
                                           {'four', 'five'}, 6, {6})
    assert test_data == control_data    # nosec


def _check_type_and_items(_converted_item, _control_item, _new_type):
    """This function facilitates testing the :py:func:`khoros.utils.core_utils.convert_set` function."""
    _correct_type = True if isinstance(_converted_item, _new_type) else False
    _items_present = True
    for _item in _control_item:
        if _item not in _converted_item:
            _items_present = False
    return all((_correct_type, _items_present))


def test_convert_set():
    """This function tests the :py:func:`khoros.utils.core_utils.convert_set` function.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    some_set = {'test', 1, 'two', ('three', )}
    some_list = ['test', 1, 'two', ('three', )]
    some_tuple = ('test', 1, 'two', ('three',))
    assert _check_type_and_items(core_utils.convert_set(some_set), some_list, list)                 # nosec
    assert _check_type_and_items(core_utils.convert_set(some_set, 'tuple'), some_tuple, tuple)      # nosec
    assert _check_type_and_items(core_utils.convert_set(some_list), some_list, list)                # nosec
    assert _check_type_and_items(core_utils.convert_set(some_tuple), some_tuple, tuple)             # nosec
    assert _check_type_and_items(core_utils.convert_set('some string'), 'some string', str)         # nosec


def test_display_warning():
    """This function tests the ability to display a warning message.

    .. versionadded:: 5.1.2
    """
    with pytest.warns(UserWarning):
        core_utils.display_warning('This is a warning message')


# Import the khoros.utils.core_utils module
core_utils = None
import_core_utils()
