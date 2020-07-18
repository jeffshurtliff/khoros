# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.roles
:Synopsis:          This module includes functions that handle roles and permissions.
:Usage:             ``from khoros.objects import roles``
:Example:           ``count = roles.get_total_role_count()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

from .. import api, liql, errors
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

ROLE_TYPES = {
    'board': 'b',
    'category': 'c',
    'group_hub': 'g',
    'top_level': 't'
}


def get_total_role_count(khoros_object, return_dict=False, total=True, top_level=False, board=False, category=False,
                         group_hub=False):
    """This function retrieves the total role count for one or more role type(s).

    .. versionadded:: 2.4.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param return_dict: Determines if the data should be returned as a dictionary (``False`` by default)
    :type return_dict: bool
    :param total: Indicates that the total overall role count should be returned (``True`` by default)
    :type total: bool
    :param top_level: Indicates that the total top-level role count should be returned (``False`` by default)
    :type top_level: bool
    :param board: Indicates that the total board-level role count should be returned (``False`` by default)
    :type board: bool
    :param category: Indicates that the total category-level role count should be returned (``False`` by default)
    :type category: bool
    :param group_hub: Indicates that the total group hub-level role count should be returned (``False`` by default)
    :type group_hub: bool
    :returns: The role count(s) as an integer, tuple or dictionary, depending on the arguments supplied
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRoleTypeError`
    """
    response = liql.perform_query(khoros_object, liql_query="SELECT id FROM roles", verify_success=True)
    counts = {
        'total': api.get_results_count(response)
    }
    if not total:
        del counts['total']
    if top_level or board or category or group_hub:
        roles_dict = api.get_items_list(response)
        count_types = {'top_level': top_level, 'board': board, 'category': category, 'group_hub': group_hub}
        for count_type, should_count in count_types.items():
            if should_count:
                counts[count_type] = count_role_types(count_type, roles_dict)
    if not return_dict:
        if len(counts) == 1:
            counts = counts.get(list(counts.keys())[0])
        else:
            counts = tuple(counts.values())
    return counts


def count_role_types(role_type, roles_dict):
    """This function returns the total count for a specific role type.

    .. versionadded:: 2.4.0

    :param role_type: The role type for which to return the count (e.g. ``board``, ``category``, etc.)
    :type role_type: str
    :param roles_dict: Dictionary of the roles for a given Khoros Community environment
    :type roles_dict: dict
    :returns: The total count for the role type as an integer
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRoleTypeError`
    """
    if role_type not in ROLE_TYPES.keys() and role_type not in ROLE_TYPES.values():
        raise errors.exceptions.InvalidRoleTypeError(role_type=role_type)
    elif role_type in ROLE_TYPES:
        role_type = ROLE_TYPES.get(role_type)
    count = 0
    for role in roles_dict:
        if role['id'].startswith(f"{role_type}:"):
            count += 1
    return count


def get_roles_for_user(khoros_object, user_id):
    """This function returns all roles associated with a given User ID.

    .. versionadded:: 2.4.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID for which to retrieve the roles data
    :returns: A dictionary with data for each role associated with the given User ID
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    response = liql.perform_query(khoros_object, liql_query=f"SELECT * FROM roles WHERE users.id = '{user_id}'",
                                  verify_success=True)
    return api.get_items_list(response)
