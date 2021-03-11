# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_http_headers
:Synopsis:       This module is used by pytest to verify that HTTP headers are formatted appropriately
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  11 Mar 2021
"""

import pytest

from . import resources


def compare_headers(headers):
    """This function compares two HTTP headers to ensure they are the same.

    .. versionadded:: 2.7.4
    """
    control_dict = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'some-list': ['something', 'something-else'],
        'some-integer': 234
    }
    return True if control_dict == headers else False


def test_normalize_headers():
    """This function tests the :py:func:`khoros.api._normalize_headers` function to ensure it works properly.

    .. versionadded:: 2.7.4
    """
    headers = {
        'Content-Type': 'Application/JSON',
        'Accept': 'application/json',
        'Some-List': ['Something', 'Something-Else'],
        'Some-Integer': 234
    }
    headers = api._normalize_headers(headers)
    assert compare_headers(headers) is True     # nosec
    return


def test_normalize_empty_headers():
    """This function verifies that passing an empty dictionary to :py:func:`khoros.api._normalize_headers`
       returns the same empty dictionary.

    .. versionadded:: 2.7.4
    """
    headers = api._normalize_headers({})
    assert headers == {}        # nosec
    return


def test_normalize_type_error():
    """This function verifies that passing no arguments to :py:func:`khoros.api._normalize_headers` raises
       a :py:exc:`TypeError` exception.

    .. versionadded:: 2.7.4
    """
    with pytest.raises(TypeError):
        api._normalize_headers()
    return


# Import modules and initialize the core object
api, exceptions = resources.import_modules('khoros.api', 'khoros.errors.exceptions')
khoros = resources.initialize_khoros_object()
