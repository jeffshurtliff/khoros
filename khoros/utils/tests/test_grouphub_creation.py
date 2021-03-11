# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_grouphub_creation
:Synopsis:       This module is used by pytest to verify that the group hub creation process works properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  11 Mar 2021
"""

import pytest

from . import resources


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
        assert 'group_title' in str(exc.value)      # nosec
    return


# Import modules and initialize the core object
grouphubs, exceptions = resources.import_modules('khoros.structures.grouphubs', 'khoros.errors.exceptions')
khoros = resources.initialize_khoros_object()
