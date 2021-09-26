# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_messages
:Synopsis:       This module is used by pytest to verify that messages function properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  26 Sep 2021
"""

import pytest

from . import resources


def get_control_data(test_type):
    """This function retrieves control data to use in unit tests.

    :param test_type: Nickname of the test to be performed
    :type test_type: str
    :returns: Payload control data in dictionary format
    """
    control_data = {
        'node': {'data': {'type': 'message', 'board': {'id': 'my-board'}, 'subject': 'This is the subject line'}},
        'node_id': {'data': {'type': 'message', 'board': {'id': 'my-board'}, 'subject': 'This is the subject line'}},
        'node_url': {'data': {'type': 'message', 'board': {'id': 'studio'}, 'subject': 'This is the subject line'}},
        'body': {'data': {'type': 'message', 'board': {'id': 'my-board'},
                          'subject': 'Welcome', 'body': '<h1>Hello!</h1>'}},
        'welcome_tag': {'data': {'type': 'message', 'board': {'id': 'my-board'}, 'subject': 'Welcome',
                                 'tags': [{'type': 'tag', 'text': 'welcome'}]}},
        '12345_tag': {'data': {'type': 'message', 'board': {'id': 'my-board'}, 'subject': 'Welcome',
                               'tags': [{'type': 'tag', 'text': '12345'}]}},
        'hello_world_tags': {'data': {'type': 'message', 'board': {'id': 'my-board'}, 'subject': 'Welcome',
                                      'tags': [{'type': 'tag', 'text': 'hello'}, {'type': 'tag', 'text': 'world'}]}},
        'str_iter_int_tags': {'data': {'type': 'message', 'board': {'id': 'my-board'}, 'subject': 'Welcome',
                                       'tags': [{'type': 'tag', 'text': 'hello'}, {'type': 'tag', 'text': 'world'},
                                                {'type': 'tag', 'text': '12345'}]}},

    }
    return control_data.get(test_type)


def test_construct_only_subject():
    """This function tests to ensure that a :py:exc:`khoros.errors.exceptions.MissingRequiredDataError` exception
    gets raised when only a subject is passed to the :py:func:`khoros.objects.messages.construct_payload` function.
    """
    with pytest.raises(exceptions.MissingRequiredDataError):
        messages.construct_payload('This is the subject line')
    return


def test_construct_with_node():
    """This function tests constructing payload using properly formatted node data."""
    control_data = get_control_data('node')
    payload = messages.construct_payload('This is the subject line', node={"id": "my-board"})
    assert payload == control_data      # nosec
    return


def test_construct_with_node_id():
    """This function tests constructing payload using a Node ID."""
    control_data = get_control_data('node_id')
    payload = messages.construct_payload('This is the subject line', node_id='my-board')
    assert payload == control_data      # nosec
    return


def test_construct_with_node_url():
    """This function tests constructing payload using a Node URL."""
    node_url = 'https://community.khoros.com/t5/Developer-Discussion/bd-p/studio'
    control_data = get_control_data('node_url')
    payload = messages.construct_payload('This is the subject line', node_url=node_url)
    assert payload == control_data      # nosec
    return


def test_construct_with_body():
    """This function tests constructing payload using a message body."""
    control_data = get_control_data('body')
    payload = messages.construct_payload('Welcome', node_id='my-board', body='<h1>Hello!</h1>')
    assert payload == control_data      # nosec
    return


def test_construct_with_one_str_tag():
    """This function tests constructing payload using a single tag in string format."""
    control_data = get_control_data('welcome_tag')
    payload = messages.construct_payload('Welcome', node_id='my-board', tags='welcome')
    assert payload == control_data      # nosec
    return


def test_construct_with_one_int_tag():
    """This function tests constructing payload using a single tag in integer format."""
    control_data = get_control_data('12345_tag')
    payload = messages.construct_payload('Welcome', node_id='my-board', tags=12345)
    assert payload == control_data      # nosec
    return


def test_construct_with_str_iter_int_tags():
    """This function tests constructing payload providing tags in string, list and integer formats."""
    control_data = get_control_data('str_iter_int_tags')
    payload = messages.construct_payload('Welcome', node_id='my-board', tags=('hello', ['world'], 12345))
    try:
        assert payload == control_data      # nosec
    except AssertionError:
        assert_tags_present(payload, ['hello', 'world', '12345'])
    return


def test_construct_with_str_iter_int_tags_ignore():
    """This function tests constructing payload providing tags in string, list and integer formats, and with the
    ``ignore_non_string_tags`` argument set to ``True`` as well."""
    control_data = get_control_data('hello_world_tags')
    payload = messages.construct_payload('Welcome', node_id='my-board', tags=('hello', ['world'], 12345),
                                         ignore_non_string_tags=True)
    try:
        assert payload == control_data      # nosec
    except AssertionError:
        assert_tags_present(payload, ['hello', 'world'])
    return


def test_construct_with_tag_iterables():
    """This function tests constructing payload providing tags as a list containing two strings."""
    control_data = get_control_data('hello_world_tags')
    list_payload = messages.construct_payload('Welcome', node_id='my-board', tags=['hello', 'world'])
    tuple_payload = messages.construct_payload('Welcome', node_id='my-board', tags=('hello', 'world'))
    set_payload = messages.construct_payload('Welcome', node_id='my-board', tags={'hello', 'world'})
    for payload in (list_payload, tuple_payload, set_payload):
        try:
            assert payload == control_data      # nosec
        except AssertionError:
            assert_tags_present(payload, ['hello', 'world'])
    return


def test_payload_validation():
    """This function tests the validation of the message payload to ensure invalid data raises an exception.

    .. versionadded:: 4.3.0
    """
    # Test null payload
    with pytest.raises(exceptions.InvalidMessagePayloadError):
        messages.validate_message_payload(payload=None)

    # Test conversion to dictionary when JSON string
    payload = '{"data": {"type": "message", "subject": "This is a message subject"}}'
    payload = messages.validate_message_payload(payload)
    assert isinstance(payload, dict)

    # Test incorrect data type
    with pytest.raises(exceptions.InvalidMessagePayloadError):
        payload = [{'type': 'message'}, {'subject': 'This is a message subject'}]
        messages.validate_message_payload(payload)

    # Test payload that is not wrapped in the 'data' field
    with pytest.raises(exceptions.InvalidMessagePayloadError):
        payload = {'type': 'message', 'subject': 'This is a message subject'}
        messages.validate_message_payload(payload)

    # Test payload that is missing the 'type' sub-field
    with pytest.raises(exceptions.InvalidMessagePayloadError):
        payload = {'subject': 'This is a message subject'}
        messages.validate_message_payload(payload)

    # Test payload that has the incorrect 'type' value
    with pytest.raises(exceptions.InvalidMessagePayloadError):
        payload = {'type': 'article', 'subject': 'This is a message subject'}
        messages.validate_message_payload(payload)

    # Test valid payload
    payload = {'data': {'type': 'message', 'subject': 'This is a message subject'}}
    payload = messages.validate_message_payload(payload)
    assert payload.get('data').get('type') == 'message'
    return


def assert_tags_present(payload, tags_to_find):
    """This function asserts that specific tags are found within API payload.

    :param payload: The payload in which to search for tags
    :type payload: dict
    :param tags_to_find: A list or tuple of tags for which to search in the payload
    :type tags_to_find: list, tuple, set
    :returns: None
    :raises: :py:exc:`AssertionError`
    """
    tags_found = []
    for tag_dict in payload['data']['tags']:
        tags_found.append(tag_dict.get('text'))
    for tag in tags_to_find:
        assert tag in tags_found        # nosec
    return


# Import modules and initialize the core object
messages, exceptions = resources.import_modules('khoros.objects.messages', 'khoros.errors.exceptions')
khoros = resources.initialize_khoros_object()
