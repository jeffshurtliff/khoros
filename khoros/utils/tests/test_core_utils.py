# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_core_utils
:Synopsis:       This module is used by pytest to verify that the core package utilities work properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  17 May 2020
"""

import os
import sys
import importlib


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
    return


def import_core_utils():
    """This function imports the :py:mod:`khoros.utils.core_utils` module."""
    set_package_path()
    global core_utils
    core_utils = importlib.import_module('khoros.utils.core_utils')
    return


def test_url_encoding():
    """This function tests the :py:func:`khoros.utils.core_utils.url_encode` and
       :py:func:`khoros.utils.core_utils.url_decode` functions.
    """
    raw_url = "https://community.example.com/t5/bizapps/bizappspage/tab/community:studio:api-browser?searchString=select id from users where login = 'admin'"
    encoded_url = "https%3A%2F%2Fcommunity.example.com%2Ft5%2Fbizapps%2Fbizappspage%2Ftab%2Fcommunity%3Astudio%3Aapi-browser%3FsearchString%3Dselect+id+from+users+where+login+%3D+%27admin%27"
    assert core_utils.url_encode(raw_url) == encoded_url
    assert core_utils.url_decode(encoded_url) == raw_url
    return


def test_query_string_encoding():
    """This function tests the :py:func:`khoros.utils.core_utils.encode_query_string` function."""
    query_dict = {
        'user.login': 'exampleuser',
        'user.password': 'Ch@ngeM3!#$',
        'restapi.response_format': 'json',
    }
    encoded_string = 'user.login=exampleuser&user.password=Ch%40ngeM3%21%23%24&restapi.response_format=json'
    encoded_string_raw_pw = 'user.login=exampleuser&user.password=Ch@ngeM3!#$&restapi.response_format=json'
    assert core_utils.encode_query_string(query_dict) == encoded_string
    assert core_utils.encode_query_string(query_dict, no_encode='user.password') == encoded_string_raw_pw
    return


def test_numeric_eval():
    """This function tests the :py:func:`khoros.utils.core_utils.is_numeric` function."""
    numeric_string = '12345'
    integer = 12345
    non_numeric_string = 'ABcd1234'
    assert core_utils.is_numeric(numeric_string) and core_utils.is_numeric(integer)
    assert not core_utils.is_numeric(non_numeric_string)
    return


def _check_type_and_items(_converted_item, _control_item, _new_type):
    """This function facilitates testing the :py:func:`khoros.utils.core_utils.convert_set` function."""
    _correct_type = True if isinstance(_converted_item, _new_type) else False
    _items_present = True
    for _item in _control_item:
        if _item not in _converted_item:
            _items_present = False
    return all((_correct_type, _items_present))


def test_convert_set():
    """This function tests the :py:func:`khoros.utils.core_utils.convert_set` function."""
    some_set = {'test', 1, 'two', ('three', )}
    some_list = ['test', 1, 'two', ('three', )]
    some_tuple = ('test', 1, 'two', ('three',))
    assert _check_type_and_items(core_utils.convert_set(some_set), some_list, list)
    assert _check_type_and_items(core_utils.convert_set(some_set, 'tuple'), some_tuple, tuple)
    assert _check_type_and_items(core_utils.convert_set(some_list), some_list, list)
    assert _check_type_and_items(core_utils.convert_set(some_tuple), some_tuple, tuple)
    assert _check_type_and_items(core_utils.convert_set('some string'), 'some string', str)
    return


# Import the khoros.utils.core_utils module
import_core_utils()
