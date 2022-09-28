# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_version
:Synopsis:          This module is used by pytest to verify that the version module functions correctly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Sep 2022
"""

import pytest

from . import resources


def test_full_version():
    """This function tests to verify that the full version is defined correctly.

    .. versionadded:: 5.1.0
    """
    assert khoros_object.version == version.get_full_version()


def test_major_minor_version():
    """This function tests to ensure that the major/minor version is getting defined correctly.

    .. versionadded:: 5.1.0
    """
    major_minor = ".".join(khoros_object.version.split(".")[:2])
    assert major_minor == version.get_major_minor_version()


def test_latest_stable():
    """This function tests to ensure that the latest stable version can be retrieved successfully.

    .. versionadded:: 5.1.0
    """
    latest_stable = version.get_latest_stable()
    assert latest_stable != '0.0.0'


def test_latest_version():
    """This function tests to ensure that the check to see if the version is the latest stable works properly.

    .. versionadded:: 5.1.0
    """
    is_latest = version.latest_version()
    assert isinstance(is_latest, bool)


# Initialize the core object
version, exceptions = resources.import_modules('khoros.utils.version', 'khoros.errors.exceptions')
khoros_object = resources.initialize_khoros_object()