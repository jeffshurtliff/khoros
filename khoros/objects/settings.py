# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.settings
:Synopsis:          This module contains functions specific to settings for various structures and objects
:Usage:             ``from khoros.objects import settings``
:Example:           ``value = settings.get_node_settings(khoros_object, 'custom.purpose', 'my-board')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     06 Jan 2021
"""

from .. import api, liql, errors
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_node_setting(khoros_object, setting_name, node_id, node_type='board', v1=None):
    """This function retrieves the value of a specific node setting.

    .. versionadded:: 3.2.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param setting_name: The name of the setting field for which to retrieve the value
    :type setting_name: str
    :param node_id: The ID of the node associated with the setting to retrieve
    :type node_id: str
    :param node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
    :type node_type: str
    :param v1: Optionally defines a specific Community API version to use when retrieving the value
    :type v1: bool, None
    :returns: The value of the setting for the node
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.LiQLParseError`
    """
    # Determine which API version to utilize
    if v1 is None:
        # Leverage APIv2 if the setting name follows the standard v2 naming convention for custom metadata fields
        v1 = False if setting_name.startswith("c_") else True

    # Get the proper URI syntax for the given node type
    node_type = _validate_node_type(node_type)

    # Perform the appropriate API request based on required version
    if v1:
        setting_value = _get_v1_node_setting(khoros_object, setting_name, node_id, node_type)
    else:
        setting_value = _get_v2_node_setting(khoros_object, setting_name, node_id, node_type)
    return setting_value


def _validate_node_type(_node_type):
    """This function checks to ensure that a valid node type has been provided for viewing or defining node settings.

    .. versionadded:: 3.2.0

    :param _node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
    :type _node_type: str
    :returns: The node type value which may or may not have been updated
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    _node_type_map = {
        'board': 'boards',
        'category': 'categories',
        'grouphub': 'grouphubs'
    }
    if _node_type not in _node_type_map.keys() and _node_type not in _node_type_map.values():
        raise errors.exceptions.InvalidNodeTypeError(val=_node_type)
    elif _node_type in _node_type_map:
        _node_type = _node_type_map.get(_node_type)
    return _node_type


def _get_v1_node_setting(_khoros_object, _setting_name, _node_id, _node_type):
    """This function retrieves a node setting value using the Community API v1.

    .. versionchanged:: 3.3.1
       Fixed an issue with the :py:func:`khoros.api.make_v1_request` function call that was resulting
       in :py:exc:`IndexError` exceptions.

    .. versionadded:: 3.2.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _setting_name: The name of the setting field for which to retrieve the value
    :type _setting_name: str
    :param _node_id: The ID of the node associated with the setting to retrieve
    :type _node_id: str
    :param _node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
    :type _node_type: str
    :returns: The value of the setting in its original format
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    _uri = f"/{_node_type}/id/{_node_id}/settings/name/{_setting_name}"
    _settings_data = api.make_v1_request(_khoros_object, _uri, request_type='GET')['response']
    if _settings_data.get('status') == 'error':
        raise errors.exceptions.GETRequestError(status_code=_settings_data['error']['code'],
                                                message=_settings_data['error']['message'])
    return _settings_data['value']['$']


def _get_v2_node_setting(_khoros_object, _setting_name, _node_id, _node_type):
    """This function retrieves a node setting value using the Community API v2 and LiQL.

    .. versionchanged:: 3.3.1
       Error handling has been introduced to avoid an :py:exc:`KeyError` exception if the setting field
       is not found, and to return a ``None`` value in that situation.

    .. versionadded:: 3.2.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _setting_name: The name of the setting field for which to retrieve the value
    :type _setting_name: str
    :param _node_id: The ID of the node associated with the setting to retrieve
    :type _node_id: str
    :param _node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
    :type _node_type: str
    :returns: The value of the setting in its original format
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    _query = f"SELECT {_setting_name} FROM {_node_type} WHERE id = '{_node_id}'"
    _settings_data = liql.perform_query(_khoros_object, liql_query=_query)
    _returned_items = liql.get_returned_items(_settings_data, only_first=True)
    _setting_value = _returned_items.get(_setting_name) if _returned_items.get(_setting_name) else None
    return _setting_value


def define_node_setting(khoros_object, setting_name, setting_val, node_id, node_type='board'):
    """This function defines a particular setting value for a given node.

    .. versionchanged:: 3.3.0.post0
       A minor fix was made to the docstring to correct a Sphinx parsing issue. The function itself was not changed.

    .. versionadded:: 3.2.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param setting_name: The name of the setting field for which to retrieve the value
    :type setting_name: str
    :param setting_val: The value of the setting to be defined
    :type setting_val: str
    :param node_id: The ID of the node associated with the setting to retrieve
    :type node_id: str
    :param node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
    :type node_type: str
    :returns: None
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    node_type = _validate_node_type(node_type)
    uri = f'/{node_type}/id/{node_id}/settings/name/{setting_name}/set'
    payload = {'value': str(setting_val)}
    response = api.make_v1_request(khoros_object, uri, payload, 'POST')['response']
    if response.get('status') != "success":
        raise errors.exceptions.POSTRequestError(status_code=response['error']['code'],
                                                 message=response['error']['message'])
    return
