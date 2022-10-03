# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_roles
:Synopsis:          This module is used by pytest to verify the :py:mod:`khoros.objects.roles` functionality.
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

import os
import sys

import pytest

from . import resources
from ...errors import exceptions

# Define a global variable to define when the package path has been set
package_path_defined = False

# Import the roles module
roles = resources.import_modules('khoros.objects.roles')


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionadded:: 5.0.0
    """
    global package_path_defined
    if not package_path_defined:
        sys.path.insert(0, os.path.abspath('../..'))
        package_path_defined = True


def test_get_role_id():
    """This function tests the :py:func:`khoros.objects.roles.get_role_id` function and corresponding method.

    .. versionchanged:: 5.1.2
       The function has been updated to support GitHub Workflows and to include a couple extra tests.

    .. versionadded:: 5.0.0
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Test the method and function
    role_id = khoros_object.roles.get_role_id('Administrator')
    assert role_id == 't:Administrator'                 # nosec
    role_id = khoros_object.roles.get_role_id('some_role', 'board', 'some-blog-node')
    assert role_id == 'b:some-blog-node:some_role'      # nosec

    # Test that the correct exception is raised for an invalid scope
    with pytest.raises(exceptions.InvalidRoleError):
        khoros_object.roles.get_role_id('Administrator', 'something_wrong')

    # Test that the correct exception is raised for a missing node ID
    with pytest.raises(exceptions.MissingRequiredDataError):
        khoros_object.roles.get_role_id('some_role', 'board')


def test_invalid_role_type():
    """This function tests passing an invalid role type to :py:func:`khoros.objects.roles.count_role_types`.

    .. versionadded:: 5.0.0
    """
    # Test that the appropriate exception is raised when an invalid role type is passed
    with pytest.raises(exceptions.InvalidRoleTypeError):
        roles.count_role_types('fake_role_type', {})


def test_total_role_type_counts():
    """This function tests the :py:meth:`khoros.core.Khoros.Role.get_total_role_count` method and related function.

    .. versionchanged:: 5.1.2
       The function has been updated to support GitHub Workflows.

    .. versionadded:: 5.0.0
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Ensure that the default result is an integer of the total count
    total_count = khoros_object.roles.get_total_role_count()
    assert isinstance(total_count, int)          # nosec

    # Ensure that adding another metric returns a tuple by default
    total_and_top_count = khoros_object.roles.get_total_role_count(top_level=True)
    assert isinstance(total_and_top_count, tuple)          # nosec

    # Ensure that disabling the total count and including another metric returns an integer
    only_top_count = khoros_object.roles.get_total_role_count(total=False, top_level=True)
    assert isinstance(only_top_count, int)          # nosec

    # Ensure that attempting to retrieve no metrics does not result in an exception
    no_metrics = khoros_object.roles.get_total_role_count(total=False)
    assert isinstance(no_metrics, tuple) and len(no_metrics) == 0          # nosec

    # Test the functionality to return a dictionary rather than a tuple
    counts_dict = khoros_object.roles.get_total_role_count(return_dict=True, top_level=True)
    assert isinstance(counts_dict, dict) and 'total' in counts_dict and 'top_level' in counts_dict          # nosec


def test_get_roles_for_user():
    """This function tests the :py:meth:`khoros.core.Khoros.Role.get_roles_for_user` method and related function.

    .. versionchanged:: 5.1.2
       The function has been updated to support GitHub Workflows.

    .. versionadded:: 5.0.0
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Test the method and function using an integer and a string as the User ID
    for user_id in [1, '1']:
        roles_for_user = khoros_object.roles.get_roles_for_user(user_id, 'id')
        assert isinstance(roles_for_user, list)          # nosec
        if len(roles_for_user) > 0:
            assert isinstance(roles_for_user[0], dict) and 'id' in roles_for_user[0]          # nosec
            assert 'href' not in roles_for_user[0]          # nosec


def test_get_users_with_role():
    """This function tests the :py:meth:`khoros.core.Khoros.Role.get_users_with_role` method and related function.

    .. versionchanged:: 5.1.2
       The function has been updated to support GitHub Workflows.

    .. versionadded:: 5.0.0
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Test the standard return mode
    users_with_role = khoros_object.roles.get_users_with_role(role_name='Administrator')
    assert isinstance(users_with_role, list)          # nosec
    if len(users_with_role) > 0:
        assert isinstance(users_with_role[0], dict) and 'login' in users_with_role[0]          # nosec

    # Test the simple return mode
    users_with_role = khoros_object.roles.get_users_with_role(role_name='Administrator', simple=True)
    assert isinstance(users_with_role, list)                # nosec
    if len(users_with_role) > 0:
        assert isinstance(users_with_role[0], str)          # nosec
