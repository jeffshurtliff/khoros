# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_board_creation
:Synopsis:       This module is used by pytest to verify that the board creation works properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  25 May 2020
"""

import os
import sys
import importlib

import pytest


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
    return


def import_boards_module():
    """This function imports the :py:mod:`khoros.structures.boards` module."""
    set_package_path()
    global boards
    boards = importlib.import_module('khoros.structures.boards')
    return


def import_exceptions_module():
    """This function imports the :py:mod:`khoros.errors.exceptions` module."""
    set_package_path()
    global exceptions
    exceptions = importlib.import_module('khoros.errors.exceptions')
    return


def initialize_khoros_object():
    """This function imports the :py:class:`khoros.core.Khoros` class and initializes an object."""
    set_package_path()
    global khoros
    core_module = importlib.import_module('khoros.core')
    khoros = core_module.Khoros(community_url='https://example.community.com', auto_connect=False,
                                tenant_id='example', auth_type='session_auth',
                                session_auth={'username': 'testuser', 'password': 'fakePassword123'})
    return


def get_required_fields(board_type='forum', all_types=False):
    """This function defines required fields that can be used in other tests.

    :param board_type: The type of board (e.g. ``forum``, ``blog``, etc.) to use
    :type board_type: str
    :param all_types: Defines if required fields for all board types should be returned
    :type all_types: bool
    :returns: A tuple or list of tuples with the required fields for one or more board types
    """
    board_id, board_title = 'test-board', 'Test Board'
    if all_types:
        field_data = []
        board_types = ['blog', 'contest', 'forum', 'idea', 'qanda', 'tkb']
        for board_type in board_types:
            field_data.append((board_id, board_title, board_type))
    else:
        field_data = (board_id, board_title, board_type)
    return field_data


def get_dict_for_required_fields(required_fields):
    """This function places the required fields in a properly formatted dictionary.

    :param required_fields: The board ID, title and type
    :type required_fields: tuple, list, set
    :returns: Dictionary containing the required fields
    """
    field_dict = {
        'id': required_fields[0],
        'title': required_fields[1],
        'conversation_style': required_fields[2]
    }
    return field_dict


def verify_data_fields(payload, data_fields):
    """This function checks a dictionary of data fields and values to ensure they match what is in the payload.

    :param payload: The payload for a new board
    :type payload: dict
    :param data_fields: The data fields and corresponding values to check
    :type data_fields: dict
    :returns: Boolean value indicating whether or not the verification checks out
    """
    verified = True
    for field, value in data_fields.items():
        if field not in payload['data']:
            verified = False
            break
        else:
            if payload['data'].get(field) != value:
                verified = False
                break
    return verified


def test_required_fields():
    """This function tests that the payload is structured properly with only the required fields supplied."""
    payload = boards.structure_payload(khoros, 'test-forum', 'Test Forum', 'forum')
    data_fields_to_check = {
        'conversation_style': 'forum',
        'id': 'test-forum',
        'title': 'Test Forum'
    }
    assert verify_data_fields(payload, data_fields_to_check) is True
    return


def test_valid_board_types():
    """This function tests to ensure that the payload for all valid board types gets formatted appropriately."""
    board_types = ['blog', 'contest', 'forum', 'idea', 'qanda', 'tkb']
    board_id, board_title = 'test-board', 'Test Board'
    for board_type in board_types:
        payload = boards.structure_payload(khoros, board_id, board_title, board_type)
        data_fields_to_check = {
            'conversation_style': board_type,
            'id': board_id,
            'title': board_title
        }
        assert verify_data_fields(payload, data_fields_to_check) is True
    return


def test_no_arguments():
    """This function tests to ensure that a TypeError is raised if no arguments are passed to the function."""
    with pytest.raises(TypeError):
        boards.structure_payload()
    return


def test_invalid_board_type():
    """This function tests to ensure an ``InvalidNodeTypeError`` exception is raised for an invalid board type."""
    with pytest.raises(exceptions.InvalidNodeTypeError):
        boards.structure_payload(khoros, 'test-board', 'Test Board', 'group-hub')
    return


def test_description():
    """This function tests the description argument to ensure it gets formatted properly for all board types."""
    description = "This is a description of the new board."
    required_fields = get_required_fields(all_types=True)
    for fields in required_fields:
        board_id, board_title, board_type = fields
        payload = boards.structure_payload(khoros, board_id, board_title, board_type, description)
        expected_fields = get_dict_for_required_fields(fields)
        expected_fields['description'] = description
        assert verify_data_fields(payload, expected_fields) is True
    return


# Import modules and initialize the core object
import_boards_module()
import_exceptions_module()
initialize_khoros_object()
