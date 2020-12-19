# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.settings
:Synopsis:          This module contains functions specific to settings for various structures and objects
:Usage:             ``from khoros.objects import settings``
:Example:           ``value = settings.get_node_settings(khoros_object, 'custom.purpose', 'my-board')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     19 Dec 2020
"""

from .. import api, liql, errors
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_node_setting(khoros_object, setting_name, node_id, node_type='board', v1=None):
    # Determine which API version to utilize
    if v1 is None:
        # Leverage APIv2 if the setting name follows the standard v2 naming convention for custom metadata fields
        v1 = False if setting_name.startswith("c_") else True

    # Get the proper URI syntax for the given node type
    node_type_map = {
        'board': 'boards',
        'category': 'categories',
        'grouphub': 'grouphubs'
    }
    if node_type not in node_type_map.keys() and node_type not in node_type_map.values():
        raise errors.exceptions.InvalidNodeTypeError(val=node_type)
    elif node_type in node_type_map:
        node_type = node_type_map.get(node_type)

    # Perform the appropriate API request based on required version
    if v1:
        setting_value = _get_v1_node_setting(khoros_object, setting_name, node_id, node_type)
    else:
        setting_value = _get_v2_node_setting(khoros_object, setting_name, node_id, node_type)
    return setting_value


def _get_v1_node_setting(_khoros_object, _setting_name, _node_id, _node_type):
    _uri = f"/{_node_type}/id/{_node_id}/settings/name/{_setting_name}"
    _settings_data = api.make_v1_request(_khoros_object, _uri, 'GET')['response']
    if _settings_data.get('status') == 'error':
        raise errors.exceptions.GETRequestError(status_code=_settings_data['error']['code'],
                                                message=_settings_data['error']['message'])
    return _settings_data['value']['$']


def _get_v2_node_setting(_khoros_object, _setting_name, _node_id, _node_type):
    _query = f"SELECT {_setting_name} FROM {_node_type} WHERE id = '{_node_id}'"
    _settings_data = liql.perform_query(_khoros_object, liql_query=_query)
    return liql.get_returned_items(_settings_data, only_first=True)[_setting_name]
