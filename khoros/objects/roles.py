# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.roles
:Synopsis:          This module includes functions that handle roles and permissions.
:Usage:             ``from khoros.objects import roles``
:Example:           ``count = roles.get_total_role_count()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     24 Sep 2021
"""

from . import users
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


def get_role_id(role_name, scope='community', node_id=None):
    """This function constructs and returns the Role ID associated with a given role name and scope.

    .. versionadded:: 4.0.0

    :param role_name: The name of the role (e.g. ``Administrator``, ``Moderator``, ``Owner``, etc.)
    :type role_name: str
    :param scope: The scope of the role (``community`` by default)
    :type scope: str
    :param node_id: The associated Node ID for any role that does not have a global/community scope.
    :type node_id: str, None
    :returns: The properly constructed Role ID where applicable
    :raises: :py:exc:`khoros.errors.exceptions.InvalidRoleError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if scope not in ROLE_TYPES:
        raise errors.exceptions.InvalidRoleError(f"The scope '{scope}' is not valid")
    prefix = _get_role_type_prefix(scope)
    if prefix == "t":
        role_id = f"{prefix}:{role_name}"
    else:
        if not node_id:
            raise errors.exceptions.MissingRequiredDataError(param='node_id')
        role_id = f"{prefix}:{node_id}:{role_name}"
    return role_id


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

    .. versionchanged:: 4.0.0
       The function now leverages a ``while`` loop instead of recursion in order to avoid raising a
       :py:exc:`RecursionError` exception with larger queries.

    .. versionadded:: 3.5.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
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

    # Perform the first LiQL query and add to the master users list
    user_data, cursor = _query_for_users(khoros_object, fields, where_clause, cursor)
    users_list.extend(user_data)

    # Continue looping as long as a cursor is present
    while cursor:
        user_data, cursor = _query_for_users(khoros_object, fields, where_clause, cursor)
        users_list.extend(user_data)

    # Convert to simple list when requested
    if simple:
        users_list = core_utils.convert_dict_list_to_simple_list(users_list, fields)

    # Return the populated users list
    return users_list


def _query_for_users(_khoros_object, _fields, _where_clause, _cursor):
    """This function performs a LiQL query to retrieve users with a specific role.

    .. versionadded:: 4.0.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _fields: One or more fields from the ``Users`` object to return (``login`` field by default)
    :type _fields: str, tuple, list, set
    :param _where_clause: Specifies an exact WHERE clause for the query to be performed
    :type _where_clause: str, None
    :param _cursor: Specifies a cursor to be referenced in a LiQL query
    :type _cursor: str, None
    :returns: The API response with the user data and the next LiQL cursor when applicable
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.LiQLParseError`
    """
    # Construct the entire LiQL query
    _cursor = '' if not _cursor else liql.structure_cursor_clause(_cursor)
    _query = f"SELECT {_fields} FROM users {_where_clause} {_cursor}"

    # Perform the API call and retrieve the data
    _response = liql.perform_query(_khoros_object, liql_query=_query)
    _user_data = liql.get_returned_items(_response)

    # Get the cursor when present
    _cursor = None
    if _response.get('data') and _response['data'].get('next_cursor'):
        _cursor = _response['data'].get('next_cursor')

    # Return the user data and cursor
    return _user_data, _cursor


def _validate_node_type(_node_type=None, _param_name='node_type'):
    """This function verifies that a provided node type (i.e. role scope) is valid for role-related functions.

    .. versionadded:: 4.0.0

    :param _node_type: The node type to be validated
    :type _node_type: str, None
    :param _param_name: The name of the parameter in the parent function in which the node type is stored
                        (Default: ``node_type``)

                        .. note:: This value is used when raising the
                                  :py:exc:`khoros.errors.exceptions.MissingRequiredDataError` exception.

    :type _param_name: str
    :returns: The validated node type
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    if not _node_type:
        raise errors.exceptions.MissingRequiredDataError(param=_param_name)
    if _node_type not in ROLE_TYPES:
        raise errors.exceptions.InvalidNodeTypeError()
    _node_type = 'grouphub' if _node_type == 'group_hub' else _node_type
    return _node_type


def _assign_role_with_v1(_khoros_object, _user, _lookup_type, _role, _node=None, _node_type='board', _return_json=True):
    """This function assigns a role to a user via REST API call using the Community API v1.

    .. versionadded:: 4.0.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _user: The identifier (i.e. ID, login or email) of the user to be assigned to the role
    :type _user: str
    :param _lookup_type: The lookup type for the user identifier (``id``, ``login`` or ``email``)
    :type _lookup_type: str
    :param _role: The name of the role to which the user will be assigned
    :type _role: str, tuple, list, set
    :param _node: The Node ID of the node to which the role is scoped when applicable
    :type _node: str, None
    :param _node_type: The type of node to which the role is scoped (e.g. ``board`` (default), ``category``, etc.)
    :type _node_type: str
    :param _return_json: Determines if the response should be returned as JSON rather than XML (``True`` by default)
    :type _return_json: bool
    :returns: The response of the API call to assign the user to the role
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.UnsupportedNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    # Ensure the role has been supplied properly
    if not isinstance(_role, str) and len(_role) > 1:
        raise errors.exceptions.CurrentlyUnsupportedError('Only individual roles can currently be assigned with API v1')
    _role = _role[0] if not isinstance(_role, str) else _role

    # Define the API URI
    _user_path = api.get_v1_user_path(user_and_type=(_user, _lookup_type))
    _uri_role_portion = f"/roles/name/{_role}/users/add?role.user={_user_path}"
    if not _node:
        _uri = f"{_khoros_object.core.get('v1_base')}/{_uri_role_portion}"
    else:
        # TODO: Identify the appropriate URI for grouphub membership additions
        if _node_type == 'grouphub':
            raise errors.exceptions.CurrentlyUnsupportedError('Group hub membership should be added via API v2 calls')
        _collection = api.get_v1_node_collection(_node_type)
        _uri = f"{_khoros_object.core.get('v1_base')}/{_collection}/id/{_node}/{_uri_role_portion}"

    # Perform the POST request and return the response
    return api.post_request_with_retries(_uri, return_json=_return_json, khoros_object=_khoros_object)


def _assign_role_with_v2(_khoros_object, _user, _lookup_type, _roles, _node=None, _node_type='board'):
    """This function assigns one or more roles to a user via REST API call using the Community API v2.

    :param _khoros_object:The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _user: The identifier (i.e. ID, login or email) of the user to be assigned to the role
    :type _user: str
    :param _lookup_type: The lookup type for the user identifier (``id``, ``login`` or ``email``)
    :type _lookup_type: str
    :param _roles: The name of the role(s) to which the user will be assigned
    :type _roles: str, tuple, list, set
    :param _node: The Node ID of the node to which the role is scoped when applicable
    :type _node: str, None
    :param _node_type: The type of node to which the role is scoped (e.g. ``board`` (default), ``category``, etc.)
    :type _node_type: str
    :returns: The response of the API call to assign the user to the role
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.UnsupportedNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`
    """
    # Get the User ID if not already provided
    _user_id = _user if _lookup_type == 'id' else None
    if not _user_id:
        if _lookup_type == 'email':
            _user_id = users.get_user_id(_khoros_object, email=_user)
        else:
            _user_id = users.get_user_id(_khoros_object, login=_user)

    # Construct the URI for the API call
    _uri = f"{_khoros_object.core.get('v2_base')}/users/{_user_id}"

    # Define the roles_to_add list within the payload
    _roles_to_add = []
    if isinstance(_roles, str):
        _roles = [_roles]
    for _role in _roles:
        _role_id = _role if ":" in _role else None
        if not _role_id:
            if _node and _node_type:
                _role_id = get_role_id(_role, _node_type, _node)
            else:
                _role_id = get_role_id(_role)
        _roles_to_add.append(_role_id)

    # Construct the full payload
    _payload = {
        "data": {
            "type": "user",
            "roles_to_add": _roles_to_add
        }
    }

    # Perform and return the API call
    return api.put_request_with_retries(_uri, _payload, khoros_object=_khoros_object, content_type='application/json')


def assign_roles_to_user(khoros_object, user, lookup_type='id', roles_to_add=None, node=None, node_type='board',
                         v1=False, return_json=True):
    """This function assigns a user to one or more roles.

    .. versionadded:: 4.0.0

    :param khoros_object:_khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user: The identifier (i.e. ID, login or email) of the user to be assigned to the role
    :type user: str
    :param lookup_type: The lookup type for the user identifier (``id``, ``login`` or ``email``)
    :type lookup_type: str
    :param roles_to_add: One or more roles (Role IDs or Role Names) to which the user will be assigned
    :type roles_to_add: str, list, tuple, set
    :param node: The Node ID of the node to which the role is scoped when applicable
    :type node: str, None
    :param node_type: The type of node to which the role is scoped (e.g. ``board`` (default), ``category``, etc.)
    :type node_type: str
    :param v1: Determines if the Community API v1 should be used to perform the operation (``False`` by default)
    :type v1: bool
    :param return_json: Determines if the response should be returned as JSON rather than XML (``True`` by default)
    :type return_json: bool
    :returns: The response from the API request
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.UnsupportedNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PUTRequestError`
    """
    # Validate the parameters
    if not roles_to_add:
        raise errors.exceptions.MissingRequiredDataError(param='roles_to_add')
    if lookup_type not in ['id', 'login', 'email']:
        raise errors.exceptions.InvalidLookupTypeError()
    node_type = _validate_node_type(node_type) if node else node_type

    # Call sub-functions depending on API version needed
    if v1:
        response = _assign_role_with_v1(khoros_object, user, lookup_type, roles_to_add, node, node_type, return_json)
    else:
        response = _assign_role_with_v2(khoros_object, user, lookup_type, roles_to_add, node, node_type)
    return response
