# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.roles
:Synopsis:          This module includes functions that handle roles and permissions.
:Usage:             ``from khoros.objects import roles``
:Example:           ``count = roles.get_total_role_count()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     14 Mar 2021
"""

from .. import api, liql, errors
from ..utils import log_utils, core_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

ROLE_TYPES = {
    'board': 'b',
    'category': 'c',
    'community': 't',
    'global': 't',
    'grouphub': 'g',
    'group_hub': 'g',
    'top_level': 't'
}
NODE_SPECIFIC_ROLES = {'b', 'board', 'c', 'category', 'g', 'grouphub', 'group_hub'}


def _get_role_type_prefix(_role_type=None):
    """This function identifies the appropriate prefix for a given role type. (Top-level prefix returned by default)

    .. versionadded:: 3.5.0

    :param _role_type: The role type associated with a role (e.g. ``board``, ``category``, etc.)
    :type _role_type: str, None
    :returns: The prefix associated with the role type (e.g. ``b``, ``c``, etc.)
    :raises: :py:exc:`TypeError`
    """
    _prefix = 't'
    if _role_type in ROLE_TYPES.values():
        _prefix = _role_type
    elif _role_type in ROLE_TYPES:
        _prefix = ROLE_TYPES.get(_role_type)
    return _prefix


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


def get_roles_for_user(khoros_object, user_id, fields=None):
    """This function returns all roles associated with a given User ID.

    .. versionchanged:: 3.5.0
       Fields to return in the LiQL query can now be explicitly defined.

    .. versionadded:: 2.4.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID for which to retrieve the roles data
    :type user_id: str, int
    :param fields: The field(s) to retrieve from the LiQL query as a string or list

                   .. note:: All fields (i.e. ``SELECT *``) are returned unless fields are explicitly defined.

    :type fields: str, list, tuple, set, None
    :returns: A dictionary with data for each role associated with the given User ID
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    fields = "*" if not fields else liql.parse_select_fields(fields)
    response = liql.perform_query(khoros_object, liql_query=f"SELECT {fields} FROM roles WHERE users.id = '{user_id}'",
                                  verify_success=True)
    return api.get_items_list(response)


def get_users_with_role(khoros_object, fields='login', role_id=None, role_name=None, scope=None, node_id=None,
                        limit_per_query=1000, cursor=None, where_clause=None, users_list=None, simple=False):
    """This function retrieves a list of all users that have a specific role.

    .. versionadded:: 3.5.0

    :param khoros_object: he core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param fields: One or more fields from the ``Users`` object to return (``login`` field by default)
    :type fields: str, tuple, list, set
    :param role_id: The identifier for the role in ``node_type:node_id:role_name`` format
    :type role_id: str, None
    :param role_name: The simple role name (e.g. ``Administrator``)

                      .. caution:: This option should only be used when the role name is unique within the community.

    :type role_name: str, None
    :param scope: The scope of the role (e.g. ``board``, ``category``, ``community``, ``grouphub``)

                  .. note:: If a value is not supplied and only a role name is defined then the role scope is
                            assumed to be at the ``community`` level. (i.e. global)

    :type scope: str, None
    :param node_id: The Node ID associated with the role (where applicable)

                    .. note:: If a value is not supplied and only a role name is defined then the role scope is
                              assumed to be at the ``community`` level. (i.e. global)

    :type node_id: str, None
    :param limit_per_query: Defines a ``LIMIT`` constraint other than the default ``1000`` limit per LiQL query

                            .. note:: Unless modified by Khoros Support or Professional Services, ``1000`` is the
                                      maximum number of entries that can be returned in a single LiQL query.

    :type limit_per_query: int, str
    :param cursor: Specifies a cursor to be referenced in a LiQL query

                   .. note:: This parameter is intended for use by the function when calling itself recursively to
                             retrieve users that exceed the ``limit_per_query`` value and will not be leveraged
                             directly in standalone function calls.

    :type cursor: str, None
    :param where_clause: Specifies an exact WHERE clause for the query to be performed

                         .. note:: While technically possible to leverage this parameter in function calls, its
                                   primary use is by the function when calling itself recursively to retrieve users
                                   that exceed the ``limit_per_query`` value.

    :type where_clause: str, None
    :param users_list: Provides an existing list of users that is leveraged when the function is called recursively
    :type users_list: list, None
    :param simple: Returns a simple list of the strings or tuples of the value(s) for each user (``False`` by default)
    :type simple: bool
    :returns: A list of users as strings, tuples or dictionaries depending if ``simple`` mode is enabled
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    # Initialize the users list if not provided
    users_list = [] if not users_list else users_list

    # Define the WHERE clause if not already defined
    if not where_clause:
        # Ensure appropriate data has been provided
        if not role_id and not role_name:
            raise errors.exceptions.MissingRequiredDataError('A role ID or role name must be provided')
        elif role_id and role_name:
            raise errors.exceptions.DataMismatchError('Only a role ID or role name should be provided and not both')
        elif not node_id and scope in NODE_SPECIFIC_ROLES:
            raise errors.exceptions.MissingRequiredDataError('A node ID must be supplied with node-specific roles')

        # Define the constraint
        prefix = _get_role_type_prefix(scope)
        if role_name:
            if scope in NODE_SPECIFIC_ROLES:
                constraint = f"roles.id = '{prefix}:{node_id}:{role_name}'"
            elif scope is not None:
                constraint = f"roles.id = '{prefix}:{role_name}'"
            else:
                constraint = f"roles.name = '{role_name}'"
        elif ':' not in role_id and scope not in NODE_SPECIFIC_ROLES:
            constraint = f"roles.name = '{role_name}'"
        else:
            constraint = f"roles.id = '{role_id}'"

        # Define the full WHERE clause if not already define4d
        if not any((isinstance(limit_per_query, int), isinstance(limit_per_query, str))):
            raise errors.exceptions.InvalidFieldError('Limit per query value must be a number (integer or string)')
        elif int(limit_per_query) < 0:
            raise errors.exceptions.InvalidFieldError('Limit per query value must be a positive number')
        where_clause = f"WHERE {constraint} LIMIT {limit_per_query}"

    # Properly parse the SELECT statement
    fields = liql.parse_select_fields(fields)

    # Construct the entire LiQL query
    cursor = '' if not cursor else liql.structure_cursor_clause(cursor)
    query = f"SELECT {fields} FROM users {where_clause} {cursor}"

    # Perform the API call and retrieve the data
    response = liql.perform_query(khoros_object, liql_query=query)
    users_list.extend(liql.get_returned_items(response))

    # Call the function recursively if a cursor is found
    has_cursor = True if response.get('data') and response['data'].get('next_cursor') else False
    if has_cursor:
        users_list = get_users_with_role(khoros_object, fields, cursor=cursor, where_clause=where_clause,
                                         users_list=users_list)

    # Convert to simple list when requested
    if simple and not has_cursor:
        users_list = core_utils.convert_dict_list_to_simple_list(users_list, fields)

    # Return the populated users list
    return users_list
