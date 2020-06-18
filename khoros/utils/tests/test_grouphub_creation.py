# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_grouphub_creation
:Synopsis:       This module is used by pytest to verify that the group hub creation process works properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  17 Jun 2020
"""

import os
import sys
import importlib

import pytest


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
    return


def import_grouphubs_module():
    """This function imports the :py:mod:`khoros.structures.boards` module."""
    set_package_path()
    global grouphubs
    grouphubs = importlib.import_module('khoros.structures.grouphubs')
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


def verify_data_fields(payload, data_fields):
    """This function checks a dictionary of data fields and values to ensure they match what is in the payload.

    :param payload: The payload for a new group hub
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


def test_no_arguments():
    """This function tests to ensure that a TypeError is raised if no arguments are passed to the function."""
    with pytest.raises(TypeError):
        grouphubs.structure_payload()
    return


def test_only_id():
    """This function tests to ensure passing only the ID references the ``group_title`` argument in the exception."""
    with pytest.raises(TypeError) as exc:
        grouphubs.structure_payload()
        assert 'group_title' in str(exc.value)
    return


# def test_required_fields():
#     """This function tests that the payload is structured properly with only the required fields supplied."""
#     payload = grouphubs.structure_payload(khoros, 'test-forum', 'Test Forum', 'forum')
#     data_fields_to_check = {
#         'conversation_style': 'forum',
#         'id': 'test-forum',
#         'title': 'Test Forum'
#     }
#     assert verify_data_fields(payload, data_fields_to_check) is True
#     return


# Import modules and initialize the core object
import_grouphubs_module()
import_exceptions_module()
initialize_khoros_object()
