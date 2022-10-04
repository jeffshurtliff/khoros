# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_tags
:Synopsis:          This module is used by pytest to verify that tags function properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

import pytest
import requests

from . import resources


def test_single_tag_structure():
    """This function tests the :py:func:`khoros.objects.tags.test_single_tag_structure` function.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = {'data': {'type': 'tag', 'text': 'my tag'}}
    payload = tags.structure_single_tag_payload('my tag')
    assert payload == control_data      # nosec


def get_structure_control_data(test_type):
    """This function retrieves the control data to use in tag structure tests.

    :param test_type: The type of test for which to return control data
    :type test_type: str
    :returns: The control data for the given test type
    """
    control_data = {
        'one_tag': [{'type': 'tag', 'text': 'first tag'}],
        'two_tags': [{'type': 'tag', 'text': 'first tag'}, {'type': 'tag', 'text': 'second tag'}],
        'str_int': [{'type': 'tag', 'text': 'first tag'}, {'type': 'tag', 'text': '12345'}],
    }
    return control_data.get(test_type)


def test_message_structure_one_tag():
    """This function tests the :py:func:`khoros.objects.tags.structure_tags_for_message` function with
    a single tag in string format.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = get_structure_control_data('one_tag')
    data = tags.structure_tags_for_message('first tag')
    assert data == control_data     # nosec


def test_invalid_payload_for_single_tag():
    """This function tests the raising of the `InvalidPayloadValueError` exception for a wrong tag text type.

    .. versionadded:: 5.1.2
    """
    with pytest.raises(exceptions.InvalidPayloadValueError):
        tags.structure_single_tag_payload(['some_random_tag'])


def test_message_structure_two_tags():
    """This function tests the :py:func:`khoros.objects.tags.structure_tags_for_message` function with
    two tags in string format.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = get_structure_control_data('two_tags')
    data = tags.structure_tags_for_message('first tag', 'second tag')
    assert data == control_data     # nosec


def test_message_structure_one_string_tag_ignore():
    """This function tests the :py:func:`khoros.objects.tags.structure_tags_for_message` function with
    a single tag in string format and the ``ignore_non_strings`` keyword argument set to ``True``.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = get_structure_control_data('one_tag')
    data = tags.structure_tags_for_message('first tag', ignore_non_strings=True)
    assert data == control_data     # nosec


def test_message_structure_two_string_tags_ignore():
    """This function tests the :py:func:`khoros.objects.tags.structure_tags_for_message` function with
    two tags in string format and the ``ignore_non_strings`` keyword argument set to ``True``.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = get_structure_control_data('two_tags')
    data = tags.structure_tags_for_message('first tag', 'second tag', ignore_non_strings=True)
    assert data == control_data     # nosec


def test_message_structure_str_int():
    """This function tests the :py:func:`khoros.objects.tags.structure_tags_for_message` function with
    one tag in string format and another as an integer.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = get_structure_control_data('str_int')
    data = tags.structure_tags_for_message('first tag', 12345)
    assert data == control_data     # nosec


def test_message_structure_str_int_ignore():
    """This function tests the :py:func:`khoros.objects.tags.structure_tags_for_message` function with
    one tag in string format and another as an integer and with ``ignore_non_strings`` set to ``True``.

    .. versionchanged:: 5.0.0
       Removed the redundant return statement.
    """
    control_data = get_structure_control_data('one_tag')
    data = tags.structure_tags_for_message('first tag', 12345, ignore_non_strings=True)
    assert data == control_data     # nosec


def test_add_single_tag_to_message(monkeypatch):
    """This function tests the ability to add a single tag to a message.

    .. versionadded:: 5.1.2
    """
    # Instantiate the Khoros object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_success_post)

    # Perform the API call
    tags.add_single_tag_to_message(khoros_object, 'testing', '12345')


def test_failed_add_single_tag_to_message(monkeypatch):
    """This function tests to ensure that an exception is raised properly for failed tag additions.

    .. versionadded:: 5.1.2
    """
    # Instantiate the Khoros object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'post', resources.mock_error_post)

    # Perform the API call
    with pytest.raises(exceptions.POSTRequestError):
        tags.add_single_tag_to_message(khoros_object, 'testing', '12345', allow_exceptions=True)
    tags.add_single_tag_to_message(khoros_object, 'testing', '12345', allow_exceptions=False)


# Import modules
tags, exceptions = resources.import_modules('khoros.objects.tags', 'khoros.errors.exceptions')
